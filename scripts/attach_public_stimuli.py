"""Attach the six pinned public stimulus assets to an existing public release.

Defaults to verification only. --apply uploads missing verified assets, never
replaces an asset, creates a release, changes a tag, or changes an installer.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from urllib.parse import quote
from urllib.request import Request, urlopen


REPOSITORY = "hbanks87/praycg-open"
SOURCE_TAG = "PRAYCG_Workbench_Public_A11.2.2"
PUBLIC_TAG = re.compile(r"PRAYCG_Workbench_Public_A[0-9]+\.[0-9]+\.[0-9]+\Z")


@dataclass(frozen=True)
class Asset:
    name: str
    size: int
    sha256: str


ASSETS = (
    Asset("PRAYCG_OPTIONAL_MASTER_STIMULI_7_20261013.zip", 691949836,
          "e851f0a6bea03ea381efe4c96c9a93685e6afdbfc9ecf05bdfd29741e6ca0a4b"),
    Asset("PRAYCG_OPTIONAL_MASTER_STIMULI_7_20261013.manifest.json", 5576,
          "c077cccb38fc3c3284c6adbe00c22a8dfc9d1ff4821cec6ef14cf0a7cedea7cd"),
    Asset("PRAYCG_OPTIONAL_MASTER_STIMULI_7_20261013.zip.sha256", 113,
          "bbde8c0d6b86d2a8701050dc2aae2a52fc3da6112b3dca38baff297f1bed68da"),
    Asset("PRAYCG_ORIGINAL_LANTERN_INSTALLER_20261014.zip", 106117274,
          "52ce56874fac1e4320822e8d71e3668836e6744a434c9e96508466081ea84280"),
    Asset("PRAYCG_ORIGINAL_LANTERN_INSTALLER_20261014.manifest.json", 36389,
          "455aa455b1061e219ef575384d1731e16ce2937158bfc3a7cd23dc125b94170b"),
    Asset("PRAYCG_ORIGINAL_LANTERN_INSTALLER_20261014.zip.sha256", 114,
          "400b5b4e6d6f233245daaa8d10f898867615548d1d4ae04bca4c7ecd2ae20fe8"),
)


class VerificationError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise VerificationError(message)


def verify_file(path: Path, expected: Asset) -> None:
    require(path.stat().st_size == expected.size, "Byte count mismatch: " + expected.name)
    with path.open("rb") as source:
        actual = hashlib.file_digest(source, "sha256").hexdigest()
    require(actual == expected.sha256, "SHA-256 mismatch: " + expected.name)


def asset_url(tag: str, name: str) -> str:
    return f"https://github.com/{REPOSITORY}/releases/download/{quote(tag, safe='')}/{quote(name, safe='')}"


class GitHub:
    """GitHub CLI handles authentication; public asset downloads carry no token."""

    def api(self, endpoint):
        result = subprocess.run(["gh", "api", "--hostname", "github.com", "--method", "GET", endpoint],
                                check=True, capture_output=True, text=True)
        return json.loads(result.stdout)

    def repository(self):
        return self.api("repos/" + REPOSITORY)

    def release(self, tag):
        release = self.api(f"repos/{REPOSITORY}/releases/tags/{quote(tag, safe='')}")
        assets = []
        page = 1
        while True:
            batch = self.api(f"repos/{REPOSITORY}/releases/{release['id']}/assets?per_page=100&page={page}")
            assets.extend(batch)
            if len(batch) < 100:
                break
            page += 1
        release["assets"] = assets
        return release

    def download(self, url, destination, expected):
        request = Request(url, headers={"User-Agent": "PRAYCG-public-stimulus-attachment/1.0"})
        count = 0
        with urlopen(request, timeout=60) as response, destination.open("xb") as output:
            while chunk := response.read(1024 * 1024):
                count += len(chunk)
                require(count <= expected.size, "Download exceeds pinned size: " + expected.name)
                output.write(chunk)

    def upload(self, tag, path):
        # Deliberately no --clobber: GitHub must refuse a same-name race.
        subprocess.run(["gh", "release", "upload", tag, str(path),
                        "--repo", "github.com/" + REPOSITORY], check=True)


def checked_release(transport, tag):
    release = transport.release(tag)
    require(release.get("tag_name") == tag, "Release tag identity differs")
    require(release.get("draft") is False and bool(release.get("published_at")),
            "An existing published, non-draft release is required")
    return release


def asset_map(release):
    assets = {}
    for asset in release["assets"]:
        name = asset["name"]
        require(name not in assets, "Duplicate release asset name: " + name)
        assets[name] = asset
    return assets


def verify_remote(transport, observed, expected, tag, directory):
    require(observed.get("name") == expected.name and observed.get("size") == expected.size,
            "Existing asset identity/size conflict: " + expected.name)
    require(observed.get("state") == "uploaded", "Asset is not completely uploaded: " + expected.name)
    require(observed.get("browser_download_url") == asset_url(tag, expected.name),
            "Asset download URL differs from its release: " + expected.name)
    digest = observed.get("digest")
    if digest:
        require(digest == "sha256:" + expected.sha256, "Existing asset digest conflict: " + expected.name)
    else:
        # Older assets can lack GitHub's digest. Verify their actual bytes.
        directory.mkdir(parents=True, exist_ok=True)
        local = directory / expected.name
        transport.download(asset_url(tag, expected.name), local, expected)
        verify_file(local, expected)


def attach(transport, tag, repository=REPOSITORY, *, apply=False, assets=ASSETS):
    require(repository == REPOSITORY, "Only hbanks87/praycg-open is allowed")
    require(isinstance(tag, str) and PUBLIC_TAG.fullmatch(tag), "Only numeric public Workbench tags are allowed")
    repo = transport.repository()
    require(repo.get("full_name") == REPOSITORY and repo.get("private") is False,
            "Repository identity/public visibility check failed")
    target = checked_release(transport, tag)
    target_id = target["id"]
    observed = asset_map(target)
    result = {"repository": repository, "tag": tag, "source_tag": SOURCE_TAG,
              "mode": "apply" if apply else "verify-only", "uploaded": [], "already_present": [], "missing": []}
    with tempfile.TemporaryDirectory(prefix="praycg-public-stimuli-") as temporary:
        directory = Path(temporary)
        missing = []
        for expected in assets:
            if expected.name in observed:
                verify_remote(transport, observed[expected.name], expected, tag, directory / "existing")
                result["already_present"].append(expected.name)
            else:
                missing.append(expected)
        result["missing"] = [asset.name for asset in missing]
        if not missing:
            return result

        # Resolve conflicts and verify EVERY missing source before the first write.
        source = asset_map(checked_release(transport, SOURCE_TAG))
        for expected in missing:
            require(expected.name in source, "Pinned source asset is missing: " + expected.name)
            verify_remote(transport, source[expected.name], expected, SOURCE_TAG, directory / "source-check")
            staged = directory / expected.name
            transport.download(asset_url(SOURCE_TAG, expected.name), staged, expected)
            verify_file(staged, expected)
        if not apply:
            return result

        for expected in missing:
            fresh = checked_release(transport, tag)
            require(fresh["id"] == target_id, "Target release was replaced during verification")
            current = asset_map(fresh)
            if expected.name in current:
                verify_remote(transport, current[expected.name], expected, tag, directory / "races")
                result["already_present"].append(expected.name)
                continue
            verify_file(directory / expected.name, expected)
            transport.upload(tag, directory / expected.name)
            result["uploaded"].append(expected.name)

        final_release = checked_release(transport, tag)
        require(final_release["id"] == target_id, "Target release identity changed after upload")
        final = asset_map(final_release)
        for expected in assets:
            require(expected.name in final, "Final asset is missing: " + expected.name)
            verify_remote(transport, final[expected.name], expected, tag, directory / "final-check")
        result["missing"] = []
        return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--repo", default=REPOSITORY)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    if os.environ.get("GITHUB_REPOSITORY"):
        require(os.environ["GITHUB_REPOSITORY"] == REPOSITORY, "Workflow repository is outside the public boundary")
    result = attach(GitHub(), args.tag, args.repo, apply=args.apply)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
