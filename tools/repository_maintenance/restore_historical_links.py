"""Restore reviewed missing companions without modifying an existing file.

Only the checked-in, hash-pinned plan is used. Downloaded code is copied as
historical evidence, never imported or executed by this helper.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import tempfile
from urllib.parse import urlsplit
from urllib.request import Request, urlopen
import zipfile

ALLOWED_ROOTS = {'docs', 'workbench', 'THIRD_PARTY_NOTICES', 'research',
                 'examples', 'archive', 'hardware'}
REPOSITORY = 'hbanks87/praycg-open'


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verified(data: bytes, spec: dict, label: str) -> bytes:
    if len(data) != spec['bytes'] or digest(data) != spec['sha256']:
        raise ValueError(f'Identity mismatch: {label}')
    return data


def destination(root: Path, name: str) -> Path:
    path = PurePosixPath(name)
    if (not name or '\\' in name or ':' in name or any(ord(c) < 32 for c in name)
            or path.is_absolute() or path.as_posix() != name
            or any(p in {'.', '..', '.git'} for p in path.parts)
            or path.parts[0] not in ALLOWED_ROOTS):
        raise ValueError(f'Unsafe restoration path: {name}')
    result = root.joinpath(*path.parts)
    cursor = result
    while cursor != root:
        if cursor.is_symlink():
            raise ValueError(f'Symlink in restoration path: {name}')
        cursor = cursor.parent
    if not result.resolve().is_relative_to(root.resolve()):
        raise ValueError(f'Path outside repository: {name}')
    return result


def validate_source(spec: dict) -> None:
    parsed = urlsplit(spec['url'])
    if (parsed.scheme != 'https' or parsed.query or parsed.fragment
            or parsed.username or parsed.password or parsed.port):
        raise ValueError('Only canonical public HTTPS sources are allowed')
    release = parsed.netloc == 'github.com' and parsed.path.startswith(
        '/' + REPOSITORY + '/releases/download/')
    raw = parsed.netloc == 'raw.githubusercontent.com' and re.fullmatch(
        '/' + REPOSITORY + r'/[0-9a-f]{40}/[^?#]+', parsed.path)
    if not (release or raw):
        raise ValueError('Source must be this public repository release or immutable commit')
    if spec['kind'] not in {'zip', 'raw'} or not 0 < spec['bytes'] < 1_000_000_000:
        raise ValueError('Invalid source kind or size')
    if not re.fullmatch(r'[0-9a-f]{64}', spec['sha256']):
        raise ValueError('A complete source SHA-256 is required')


def download(spec: dict, cache: Path) -> bytes:
    validate_source(spec)
    cached = cache / spec['sha256']
    if cached.exists():
        return verified(cached.read_bytes(), spec, 'cached ' + spec['url'])
    request = Request(spec['url'], headers={'User-Agent': 'PRAYCG-companion-restoration/1.0'})
    parts, count = [], 0
    with urlopen(request, timeout=90) as response:
        while chunk := response.read(1024 * 1024):
            count += len(chunk)
            if count > spec['bytes']:
                raise ValueError('Source exceeds pinned size: ' + spec['url'])
            parts.append(chunk)
    data = verified(b''.join(parts), spec, spec['url'])
    cache.mkdir(parents=True, exist_ok=True)
    with cached.open('xb') as stream:
        stream.write(data)
    return data


def prepare(plan: dict, root: Path, cache: Path, loader=download) -> list:
    root = root.resolve()
    sources, prepared, seen = {}, [], set()
    for row in plan['files']:
        name = row['path']
        if name in seen:
            raise ValueError('Duplicate restoration target: ' + name)
        seen.add(name)
        target = destination(root, name)
        if 'inline_utf8' in row:
            data = row['inline_utf8'].encode('utf-8')
        else:
            key = row['source']
            spec = plan['sources'][key]
            validate_source(spec)
            if key not in sources:
                sources[key] = verified(loader(spec, cache), spec, key)
            if spec['kind'] == 'zip':
                import io
                with zipfile.ZipFile(io.BytesIO(sources[key])) as archive:
                    matches = [i for i in archive.infolist() if i.filename == row['member']]
                    if len(matches) != 1 or matches[0].is_dir() or matches[0].file_size != row['bytes']:
                        raise ValueError('Missing, duplicated or wrong-size ZIP member: ' + name)
                    data = archive.read(matches[0])
            else:
                data = sources[key]
        verified(data, row, name)
        exists = target.exists()
        if exists and (not target.is_file() or target.read_bytes() != data):
            raise ValueError('Refusing to change existing target: ' + name)
        prepared.append((name, target, data, exists))
    return prepared


def apply(prepared: list) -> dict:
    added, identical = [], []
    for name, target, data, exists in prepared:
        if exists:
            identical.append(name)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('xb') as stream:
            stream.write(data)
        added.append(name)
    return {'added': added, 'already_identical': identical, 'existing_files_modified': 0}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan', type=Path, default=Path(__file__).with_name('RESTORATION_PLAN.json'))
    parser.add_argument('--root', type=Path, default=Path.cwd())
    parser.add_argument('--source-cache', type=Path)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text(encoding='utf-8'))
    with tempfile.TemporaryDirectory(prefix='praycg-recovery-') as temporary:
        prepared = prepare(plan, args.root, args.source_cache or Path(temporary))
        result = apply(prepared) if args.apply else {
            'verified_files': len(prepared), 'missing_targets': sum(not r[3] for r in prepared),
            'existing_files_modified': 0, 'mode': 'check_only'}
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
