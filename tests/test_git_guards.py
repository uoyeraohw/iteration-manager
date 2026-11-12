import sys
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from iter_sync import verify_todos_committed, generate_review_package

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/iter_sync.py"


def test_non_git_is_not_committed(tmp_path):
    result = verify_todos_committed(tmp_path)
    assert result["committed"] is False
    assert result.get("error")
    cli = subprocess.run([sys.executable, "-B", str(SCRIPT), "--verify-committed", str(tmp_path)],
                         capture_output=True, text=True, encoding="utf-8")
    assert cli.returncode != 0
    assert "PASSED" not in cli.stdout
    assert "fatal" in cli.stderr


def test_review_package_invalid_refs_does_not_create_package(tmp_path):
    subprocess.run(["git", "init", "-b", "main", str(tmp_path)], check=True, capture_output=True)
    error = None
    try:
        generate_review_package("missing-base", "HEAD", "01", tmp_path)
    except (ValueError, RuntimeError) as e:
        error = str(e)
    assert error, "Invalid refs must fail, not produce a successful review package"
    assert not list((tmp_path / ".git/iter_reviews").glob("*.md"))
