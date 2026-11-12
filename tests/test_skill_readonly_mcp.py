import importlib.util
import asyncio
import json
import os
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('skill_readonly_mcp', ROOT / 'scripts/skill_readonly_mcp.py')
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


@pytest.fixture
def granted(tmp_path, monkeypatch):
    root = tmp_path / 'primary'
    workspace = tmp_path / 'workspace'
    root.mkdir()
    workspace.mkdir()
    (root / 'contract.md').write_text('alpha\nbeta\n', encoding='utf-8')
    (root / 'private.md').write_text('PRIVATE-CONTENT-SENTINEL', encoding='utf-8')
    grant_path = tmp_path / 'grant.json'
    grant = {'version': 1, 'enabled': True, 'grant_id': 'test-grant', 'workspace': str(workspace), 'skill_root': str(root), 'files': ['contract.md']}
    grant_path.write_text(json.dumps(grant), encoding='utf-8')
    monkeypatch.chdir(workspace)
    return MODULE.SkillReadGrant(grant_path), grant_path, grant, root


def test_granted_read_returns_primary_text_and_provenance(granted):
    reader, _, _, root = granted
    result = reader.read_file('contract.md', start_line=2, max_lines=1)
    assert result['text'] == '2\tbeta'
    assert Path(result['source']) == root / 'contract.md'
    assert result['total_lines'] == 2
    assert result['grant_id'] == 'test-grant'


@pytest.mark.parametrize('path', ['../private.md', '/contract.md', 'C:/contract.md', 'contract.md:stream', 'dir\\contract.md', 'private.md', './contract.md', 'dir//contract.md'])
def test_path_not_explicitly_granted_is_denied(granted, path):
    with pytest.raises((PermissionError, ValueError)):
        granted[0].read_file(path)


def test_wrong_workspace_and_revocation_are_immediate(granted, monkeypatch, tmp_path):
    reader, grant_path, grant, _ = granted
    monkeypatch.chdir(tmp_path)
    with pytest.raises(PermissionError):
        reader.read_file('contract.md')
    monkeypatch.chdir(grant['workspace'])
    grant['enabled'] = False
    grant_path.write_text(json.dumps(grant), encoding='utf-8')
    with pytest.raises(PermissionError):
        reader.read_file('contract.md')


def test_symlink_escape_and_open_race_are_denied(granted, tmp_path, monkeypatch):
    reader, _, _, root = granted
    outside = tmp_path / 'outside.md'
    outside.write_text('outside secret', encoding='utf-8')
    target = root / 'contract.md'
    target.unlink()
    try:
        target.symlink_to(outside)
    except OSError as exc:
        pytest.skip(f'OS cannot create test symlink: {exc}')
    with pytest.raises(PermissionError):
        reader.read_file('contract.md')
    target.unlink()
    target.write_text('alpha', encoding='utf-8')
    original_open = Path.open
    def swapped_open(self, *args, **kwargs):
        if self == target and args == ('rb',):
            return original_open(outside, *args, **kwargs)
        return original_open(self, *args, **kwargs)
    monkeypatch.setattr(Path, 'open', swapped_open)
    with pytest.raises(PermissionError):
        reader.read_file('contract.md')


def test_invalid_grant_and_limits_fail_closed(granted):
    reader, grant_path, grant, root = granted
    grant_path.write_text('{broken', encoding='utf-8')
    with pytest.raises((ValueError, PermissionError)):
        reader.read_file('contract.md')
    grant_path.write_text(json.dumps(grant), encoding='utf-8')
    (root / 'contract.md').write_bytes(b'x' * (1024 * 1024 + 1))
    with pytest.raises(ValueError):
        reader.read_file('contract.md')


def test_open_race_is_denied_even_without_symlink_support(granted, tmp_path, monkeypatch):
    reader, _, _, root = granted
    outside = tmp_path / 'outside.md'
    outside.write_text('not authorized', encoding='utf-8')
    original_open = Path.open
    def swapped(self, *args, **kwargs):
        return original_open(outside if self == root / 'contract.md' and args == ('rb',) else self, *args, **kwargs)
    monkeypatch.setattr(Path, 'open', swapped)
    with pytest.raises(PermissionError):
        reader.read_file('contract.md')


@pytest.mark.parametrize('start,count', [(0, 1), (True, 1), (1, 0), (1, 401), (1, True)])
def test_line_limits(granted, start, count):
    with pytest.raises(ValueError):
        granted[0].read_file('contract.md', start, count)


def test_real_stdio_tool_surface_and_workspace_boundary(granted, tmp_path):
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    _, grant_path, grant, _ = granted
    async def probe(cwd, allowed):
        parameters = StdioServerParameters(command=sys.executable,
            args=['-B', str(ROOT / 'scripts/skill_readonly_mcp.py'), '--grant', str(grant_path)], cwd=str(cwd))
        async with stdio_client(parameters) as (read, write):
            async with ClientSession(read, write) as client:
                await client.initialize()
                listing = await client.list_tools()
                assert [tool.name for tool in listing.tools] == ['read_skill_file']
                assert listing.tools[0].annotations.readOnlyHint is True
                result = await client.call_tool('read_skill_file', {'relative_path': 'contract.md'})
                assert bool(result.isError) is not allowed
                if allowed:
                    body = json.loads(result.content[0].text)
                    assert body['text'] == '1\talpha\n2\tbeta'
                    assert body['grant_id'] == 'test-grant'
                    assert body['access'] == 'read-only'
                denied = await client.call_tool('read_skill_file', {'relative_path': 'private.md'})
                assert denied.isError
                assert 'PRIVATE-CONTENT-SENTINEL' not in denied.content[0].text
                missing = await client.call_tool('write_file', {'path': 'contract.md', 'content': 'changed'})
                assert missing.isError
    asyncio.run(probe(grant['workspace'], True))
    asyncio.run(probe(tmp_path, False))
