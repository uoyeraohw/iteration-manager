"""Explicit, workspace-bound read grants for the maintained Skill (stdio MCP)."""
import argparse
import json
import os
import stat
import sys
from pathlib import Path

MAX_BYTES = 1024 * 1024


def _relative(value):
    if (not isinstance(value, str) or not value or
            any(char in value for char in ('\\', ':', '\x00')) or
            any(part in ('', '.', '..') for part in value.split('/'))):
        raise ValueError('Expected a canonical relative POSIX file path')
    return value


def _directory(value):
    if not isinstance(value, str) or not Path(value).is_absolute():
        raise PermissionError('Grant directories must be absolute')
    path = Path(value)
    resolved = path.resolve(strict=True)
    if resolved == Path(resolved.anchor) or not resolved.is_dir() or path != resolved:
        raise PermissionError('Grant directories must be real non-root directories')
    return resolved


def _opened_path(stream):
    """Inspect the opened object, not a second resolution of its original name."""
    if sys.platform == 'win32':
        import ctypes
        import msvcrt
        from ctypes import wintypes
        function = ctypes.WinDLL('kernel32', use_last_error=True).GetFinalPathNameByHandleW
        function.argtypes = [wintypes.HANDLE, wintypes.LPWSTR, wintypes.DWORD, wintypes.DWORD]
        function.restype = wintypes.DWORD
        handle = msvcrt.get_osfhandle(stream.fileno())
        size = function(handle, None, 0, 0)
        if not size:
            raise PermissionError('Cannot verify opened file identity')
        buffer = ctypes.create_unicode_buffer(size + 1)
        written = function(handle, buffer, len(buffer), 0)
        if not written or written >= len(buffer):
            raise PermissionError('Cannot verify opened file identity')
        value = buffer.value
        if value.startswith('\\\\?\\UNC\\'):
            value = '\\\\' + value[8:]
        elif value.startswith('\\\\?\\'):
            value = value[4:]
        return Path(value)
    if sys.platform.startswith('linux'):
        return Path(os.readlink(f'/proc/self/fd/{stream.fileno()}'))
    raise PermissionError('Opened-file verification is unsupported on this platform')


class SkillReadGrant:
    def __init__(self, grant_path):
        self.grant_path = Path(grant_path).absolute()

    def read_file(self, relative_path, start_line=1, max_lines=200):
        relative_path = _relative(relative_path)
        if (type(start_line) is not int or start_line < 1 or
                type(max_lines) is not int or not 1 <= max_lines <= 400):
            raise ValueError('start_line must be positive; max_lines must be 1..400')
        with self.grant_path.open('rb') as stream:
            raw = stream.read(65537)
        if len(raw) > 65536:
            raise ValueError('Grant exceeds size limit')
        grant = json.loads(raw)
        if (not isinstance(grant, dict) or type(grant.get('version')) is not int or
                grant['version'] != 1 or grant.get('enabled') is not True or
                not isinstance(grant.get('grant_id'), str) or not grant['grant_id'].strip()):
            raise PermissionError('Grant is invalid or disabled')
        workspace = _directory(grant.get('workspace'))
        root = _directory(grant.get('skill_root'))
        if Path.cwd().resolve(strict=True) != workspace:
            raise PermissionError('Workspace is not authorized')
        files = grant.get('files')
        if not isinstance(files, list) or not files or any(_relative(item) != item for item in files):
            raise PermissionError('Grant requires an explicit file allowlist')
        if relative_path not in files:
            raise PermissionError('File is not authorized')
        target = root.joinpath(*relative_path.split('/'))
        expected = target.resolve(strict=True)
        if not expected.is_relative_to(root) or expected != target:
            raise PermissionError('Linked or escaping files are not authorized')
        with target.open('rb') as stream:
            opened = _opened_path(stream)
            if opened != expected or not opened.is_relative_to(root):
                raise PermissionError('Opened file does not match authorization')
            info = os.fstat(stream.fileno())
            if not stat.S_ISREG(info.st_mode) or info.st_size > MAX_BYTES:
                raise ValueError('Only regular files up to 1 MiB are supported')
            data = stream.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES:
            raise ValueError('File exceeds 1 MiB')
        lines = data.decode('utf-8-sig').splitlines()
        selected = lines[start_line - 1:start_line - 1 + max_lines]
        return {'text': '\n'.join(f'{number}\t{line}' for number, line in enumerate(selected, start_line)),
                'source': str(expected), 'file': relative_path, 'total_lines': len(lines),
                'start_line': start_line, 'end_line': start_line + len(selected) - 1,
                'grant_id': grant['grant_id'], 'workspace': str(workspace), 'access': 'read-only'}


def create_server(grant_path):
    # The existing iteration CLI does not acquire an MCP dependency.
    from mcp.server.fastmcp import FastMCP
    from mcp.types import ToolAnnotations
    server = FastMCP('iteration-skill-readonly')
    reader = SkillReadGrant(grant_path)

    @server.tool(annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False,
                                           idempotentHint=True, openWorldHint=False))
    def read_skill_file(relative_path: str, start_line: int = 1, max_lines: int = 200) -> dict:
        """Read an explicitly granted primary Skill file, with line numbers and provenance."""
        return reader.read_file(relative_path, start_line, max_lines)

    return server


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--grant', required=True, type=Path)
    create_server(parser.parse_args().grant).run(transport='stdio')
