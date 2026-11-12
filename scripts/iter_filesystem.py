"""Filesystem delivery mode profile loader and manifest binding validator."""
import json
import os
import re
from pathlib import Path
from iter_contracts import (
    contained,
    scope_paths,
    matches_scope,
    section,
    parse_card,
    MUTABLE_METADATA,
)


def load_profile(iter_dir: Path) -> Path | None:
    """Load filesystem delivery profile or return None for default Git mode.

    Enforces <root>/docs/todos/<digits>-<name>/iteration-delivery.json layout.
    Raises ValueError on invalid profile, corrupt symlink, or wrong schema/mode.
    """
    profile_candidate = iter_dir / "iteration-delivery.json"
    if not os.path.lexists(profile_candidate):
        return None

    resolved_iter = iter_dir.resolve()
    name = resolved_iter.name
    if not re.match(r"^\d+-[^/\\]+$", name):
        raise ValueError(f"Invalid iteration directory layout name: {name}")
    todos_dir = resolved_iter.parent
    if todos_dir.name != "todos":
        raise ValueError("Iteration directory must be under docs/todos")
    docs_dir = todos_dir.parent
    if docs_dir.name != "docs":
        raise ValueError("todos directory must be under docs")

    root = docs_dir.parent.resolve()

    profile_rel = (resolved_iter.relative_to(root) / "iteration-delivery.json").as_posix()
    try:
        profile_path = contained(root, profile_rel)
    except (OSError, ValueError) as exc:
        raise ValueError(f"Invalid iteration-delivery.json path: {exc}") from exc

    if not profile_path.is_file():
        raise ValueError("iteration-delivery.json must be an existing regular file")

    try:
        raw = profile_path.read_text(encoding="utf-8")
        data = json.loads(raw)
    except Exception as exc:
        raise ValueError(f"Corrupt iteration-delivery.json: {exc}") from exc

    if not isinstance(data, dict):
        raise ValueError("Profile JSON must be an object")

    if set(data.keys()) != {"schema_version", "mode"}:
        raise ValueError("Unsupported delivery profile schema keys")

    schema_version = data.get("schema_version")
    if type(schema_version) is not int or schema_version != 1:
        raise ValueError("Unsupported delivery profile schema_version")

    if data.get("mode") != "filesystem":
        raise ValueError("Unsupported delivery mode profile")

    return root


def _canon_path(path: Path) -> str:
    return os.path.normcase(os.path.normpath(str(path.resolve())))


def _fs_contract_projection(content: str):
    meta, body, errors = parse_card(content)
    if errors:
        raise ValueError("Invalid frozen task card: " + "; ".join(errors))
    for name in ("scope", "acceptance", "ledger"):
        if section(body, name, r"(?!)") is None:
            raise ValueError(f"schema1 requires paired iter:{name} markers")
    return {k: v for k, v in meta.items() if k not in MUTABLE_METADATA}, body


def validate_filesystem_binding(meta: dict, receipt: dict, root: Path, task_path: str, content: str) -> list[str]:
    """Validate candidate manifest and frozen snapshot bindings under filesystem mode."""
    errors = []

    # 1. Manifest file existence and json schema
    manifest_rel = receipt.get("candidate_manifest")
    try:
        manifest_path = contained(root, manifest_rel)
    except (OSError, ValueError) as e:
        return [f"Invalid candidate_manifest path: {e}"]

    try:
        manifest_raw = manifest_path.read_text(encoding="utf-8")
        manifest_data = json.loads(manifest_raw)
    except Exception as e:
        return [f"Failed to read candidate_manifest: {e}"]

    if not isinstance(manifest_data, dict):
        return ["candidate_manifest must be a JSON object"]

    expected_candidate = meta.get("candidate_id")
    if manifest_data.get("candidate_id") != expected_candidate:
        errors.append("candidate_manifest candidate_id mismatch")

    files = manifest_data.get("files")
    if not isinstance(files, list) or not files:
        errors.append("candidate_manifest requires non-empty files array")
        return errors

    # 2. Scope parsing and missing files check
    scopes, scope_errors = scope_paths(content)
    errors.extend(scope_errors)

    # 3. Resolve file mappings, check overlaps and bitwise byte equality
    source_map: dict[str, Path] = {}
    snapshot_map: dict[str, Path] = {}

    for idx, item in enumerate(files):
        if not isinstance(item, dict) or "path" not in item or "snapshot" not in item:
            errors.append(f"Invalid file entry at index {idx}")
            continue

        try:
            s_path = contained(root, item["path"], allow_empty=True)
            snap_path = contained(root, item["snapshot"], allow_empty=True)
        except (OSError, ValueError) as e:
            errors.append(f"File mapping error at index {idx}: {e}")
            continue

        s_canon = _canon_path(s_path)
        snap_canon = _canon_path(snap_path)

        if s_canon in source_map:
            errors.append(f"Duplicate source in manifest: {item['path']}")
        source_map[s_canon] = s_path

        if snap_canon in snapshot_map:
            errors.append(f"Duplicate snapshot in manifest: {item['snapshot']}")
        snapshot_map[snap_canon] = snap_path

        try:
            if s_path.read_bytes() != snap_path.read_bytes():
                errors.append(f"Source and snapshot content mismatch: {item['path']}")
        except OSError as e:
            errors.append(f"Unable to compare source and snapshot bytes for {item['path']}: {e}")

    # No overlap across source and snapshot sets
    overlap = set(source_map.keys()) & set(snapshot_map.keys())
    if overlap:
        errors.append("Source and snapshot paths must not overlap")

    # 4. Manifest and snapshots must be outside scope
    manifest_rel_norm = manifest_path.resolve().relative_to(root).as_posix()
    if matches_scope(manifest_rel_norm, scopes):
        errors.append("candidate_manifest must be outside scopes")

    for snap_canon, snap_path in snapshot_map.items():
        snap_rel = snap_path.resolve().relative_to(root).as_posix()
        if matches_scope(snap_rel, scopes):
            errors.append(f"Snapshot must be outside scopes: {snap_rel}")

    # 5. Check outputs and excluded receipt/report
    checks = receipt.get("checks") or []
    check_outputs = set()
    for check in checks:
        if isinstance(check, dict) and check.get("output"):
            try:
                out_p = contained(root, check["output"])
                check_outputs.add(_canon_path(out_p))
            except (OSError, ValueError):
                pass

    excluded = set()
    for ex_key in (meta.get("review_receipt"), receipt.get("review_report")):
        if ex_key:
            try:
                excluded.add(_canon_path(contained(root, ex_key)))
            except (OSError, ValueError):
                pass

    # 6. Actual existing files under scopes must be covered
    required_sources = set(check_outputs)
    for sc in scopes:
        is_dir_scope = sc.endswith("/")
        scope_clean = sc.rstrip("/") if is_dir_scope else sc
        try:
            target_path = contained(root, scope_clean, directory=is_dir_scope, allow_empty=True)
        except (OSError, ValueError) as e:
            errors.append(f"Scope path validation error {sc}: {e}")
            continue

        if is_dir_scope:
            if not target_path.is_dir():
                errors.append(f"Declared scope directory missing or not a directory: {sc}")
                continue
            for p in target_path.rglob("*"):
                if os.path.islink(p) or p.is_file():
                    try:
                        p_rel = p.relative_to(root).as_posix()
                        verified_p = contained(root, p_rel, allow_empty=True)
                        if not verified_p.is_file():
                            errors.append(f"Scope entry is not a regular file: {p_rel}")
                            continue
                        canon = _canon_path(verified_p)
                        if canon not in excluded:
                            required_sources.add(canon)
                    except (OSError, ValueError) as e:
                        errors.append(f"Invalid file or symlink in scope directory {sc}: {e}")
        else:
            if not target_path.exists():
                errors.append(f"Declared scope file missing: {sc}")
            elif not target_path.is_file():
                errors.append(f"Declared scope file is not a regular file: {sc}")
            else:
                try:
                    sc_rel = target_path.relative_to(root).as_posix()
                    verified_p = contained(root, sc_rel, allow_empty=True)
                    canon = _canon_path(verified_p)
                    if canon not in excluded:
                        required_sources.add(canon)
                except (OSError, ValueError) as e:
                    errors.append(f"Invalid scope file {sc}: {e}")

    uncovered = required_sources - set(source_map.keys())
    if uncovered:
        errors.append(f"Manifest missing required scope/output files: {len(uncovered)} uncovered")

    # Every manifest source must be within scope or check.output
    for s_canon, s_path in source_map.items():
        s_rel = s_path.resolve().relative_to(root).as_posix()
        if not (matches_scope(s_rel, scopes) or s_canon in check_outputs):
            errors.append(f"Manifest source not authorized by scopes or check output: {s_rel}")

    # 7. Contract snapshot verification
    try:
        current_card_path = contained(root, task_path)
        contract_snap_path = contained(root, receipt.get("contract_snapshot"))
        if _canon_path(contract_snap_path) == _canon_path(current_card_path):
            errors.append("contract_snapshot cannot be current task card")
        else:
            snap_text = contract_snap_path.read_text(encoding="utf-8")
            if _fs_contract_projection(snap_text) != _fs_contract_projection(content):
                errors.append("contract_snapshot projection mismatch")
    except (OSError, ValueError) as e:
        errors.append(f"Invalid contract_snapshot: {e}")

    # 8. Goal snapshot verification (must use task directory README)
    try:
        task_p = contained(root, task_path)
        iter_readme_rel = (task_p.parent.relative_to(root) / "README.md").as_posix()
        iter_readme_path = contained(root, iter_readme_rel)
        goal_snap_path = contained(root, receipt.get("goal_snapshot"))
        if _canon_path(goal_snap_path) == _canon_path(iter_readme_path):
            errors.append("goal_snapshot cannot be iteration README itself")
        else:
            if not iter_readme_path.is_file():
                errors.append("Iteration README missing in task directory")
            else:
                legacy_regex = "迭代核心目标与全局约束|Iteration Goal.*Global Constraints"
                readme_text = iter_readme_path.read_text(encoding="utf-8")
                snap_text = goal_snap_path.read_text(encoding="utf-8")
                readme_goal = section(readme_text, "goal", legacy_regex)
                snap_goal = section(snap_text, "goal", legacy_regex)
                if readme_goal is None or snap_goal is None or snap_goal != readme_goal:
                    errors.append("goal_snapshot content mismatch with iteration README goal section")
    except (OSError, ValueError) as e:
        errors.append(f"Invalid goal_snapshot: {e}")

    return errors
