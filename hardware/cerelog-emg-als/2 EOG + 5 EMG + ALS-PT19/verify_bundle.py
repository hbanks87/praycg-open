"""Verify all distributed bundle files offline; never imports a serial library."""
from pathlib import Path, PurePosixPath
import hashlib
import json


def main():
    root = Path(__file__).resolve().parent
    entries = {}
    for line in (root / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines():
        expected, name = line.split("  ", 1)
        path = PurePosixPath(name)
        if (path.is_absolute() or ".." in path.parts or "\\" in name
                or name in entries or len(expected) != 64
                or any(char not in "0123456789abcdef" for char in expected)):
            raise SystemExit(f"Invalid checksum entry: {name}")
        target = root.joinpath(*path.parts)
        if not target.is_file() or target.is_symlink():
            raise SystemExit(f"Missing or unsafe file: {name}")
        if not target.resolve().is_relative_to(root):
            raise SystemExit(f"Path escapes bundle: {name}")
        content = target.read_bytes()
        if hashlib.sha256(content).hexdigest() != expected:
            raise SystemExit(f"Checksum mismatch: {name}")
        entries[name] = content
    manifest = json.loads(entries["MANIFEST.json"])
    listed = set()
    for item in manifest["files"]:
        name = item["path"]
        if name in listed or name not in entries:
            raise SystemExit(f"Invalid manifest entry: {name}")
        content = entries[name]
        if len(content) != item["bytes"] or hashlib.sha256(content).hexdigest() != item["sha256"]:
            raise SystemExit(f"Manifest mismatch: {name}")
        listed.add(name)
    if listed != set(entries) - {"MANIFEST.json"}:
        raise SystemExit("Manifest and checksum inventory disagree")
    actual = {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()}
    extras = actual - set(entries) - {"SHA256SUMS.txt"}
    print(f"PASS: {len(entries)} distributed files verified; {manifest['firmware_identifier']}")
    if extras:
        print("Additional local files are not verified: " + ", ".join(sorted(extras)))
    print("Integrity only; this is not authentication, electrical safety, or physiological validation.")


if __name__ == "__main__":
    main()
