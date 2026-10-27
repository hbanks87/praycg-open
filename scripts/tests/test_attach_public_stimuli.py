"""Offline failure-path tests: no network, credentials, or GitHub writes."""
import copy
import hashlib
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import attach_public_stimuli as subject


TAG = "PRAYCG_Workbench_Public_A11.9.2"


class FakeGitHub:
    def __init__(self, payloads):
        self.payloads = dict(payloads)
        self.source = {name: self.asset(name, data, subject.SOURCE_TAG) for name, data in payloads.items()}
        self.target = {}
        self.uploads = []
        self.downloads = []
        self.corrupt = set()
        self.draft = False
        self.private = False
        self.fail_upload_number = None

    def asset(self, name, data, tag):
        return {"name": name, "size": len(data), "digest": "sha256:" + hashlib.sha256(data).hexdigest(),
                "state": "uploaded", "browser_download_url": subject.asset_url(tag, name)}

    def repository(self):
        return {"full_name": subject.REPOSITORY, "private": self.private}

    def release(self, tag):
        source = tag == subject.SOURCE_TAG
        return {"id": 1 if source else 2, "tag_name": tag, "draft": self.draft,
                "published_at": "2026-10-23T11:21:33Z", "assets": copy.deepcopy(list((self.source if source else self.target).values()))}

    def download(self, url, destination, expected):
        self.downloads.append(expected.name)
        data = self.payloads[expected.name]
        if expected.name in self.corrupt:
            data = b"x" * len(data)
        destination.write_bytes(data)

    def upload(self, tag, path):
        if self.fail_upload_number == len(self.uploads) + 1:
            raise RuntimeError("simulated upload interruption")
        if path.name in self.target:
            raise RuntimeError("refuse same-name overwrite")
        self.uploads.append(path.name)
        self.target[path.name] = self.asset(path.name, path.read_bytes(), tag)


class AttachmentTests(unittest.TestCase):
    def setUp(self):
        self.data = {"pack.zip": b"fixture archive", "pack.manifest.json": b'{"fixture":true}',
                     "pack.zip.sha256": b"fixture checksum"}
        self.assets = tuple(subject.Asset(name, len(data), hashlib.sha256(data).hexdigest())
                            for name, data in self.data.items())
        self.api = FakeGitHub(self.data)

    def run_attach(self, **kwargs):
        return subject.attach(self.api, TAG, assets=self.assets, **kwargs)

    def test_rejects_last_download_hash_mismatch_before_any_upload(self):
        self.api.corrupt.add(self.assets[-1].name)
        with self.assertRaisesRegex(subject.VerificationError, "SHA-256 mismatch"):
            self.run_attach(apply=True)
        self.assertEqual(self.api.uploads, [])

    def test_existing_digest_conflict_stops_before_download_or_upload(self):
        name = self.assets[-1].name
        self.api.target[name] = self.api.asset(name, b"x" * len(self.data[name]), TAG)
        with self.assertRaisesRegex(subject.VerificationError, "digest conflict"):
            self.run_attach(apply=True)
        self.assertEqual(self.api.uploads, [])
        self.assertEqual(self.api.downloads, [])

    def test_source_metadata_conflict_uploads_nothing(self):
        self.api.source[self.assets[-1].name]["size"] += 1
        with self.assertRaisesRegex(subject.VerificationError, "size conflict"):
            self.run_attach(apply=True)
        self.assertEqual(self.api.uploads, [])

    def test_partial_existing_set_resumes_and_repeat_is_idempotent(self):
        first = self.assets[0].name
        self.api.target[first] = self.api.asset(first, self.data[first], TAG)
        result = self.run_attach(apply=True)
        self.assertEqual(result["already_present"], [first])
        self.assertEqual(self.api.uploads, [a.name for a in self.assets[1:]])
        second = self.run_attach(apply=True)
        self.assertEqual(second["uploaded"], [])
        self.assertEqual(len(second["already_present"]), len(self.assets))

    def test_interrupted_upload_can_resume_without_replacing_completed_asset(self):
        self.api.fail_upload_number = 2
        with self.assertRaisesRegex(RuntimeError, "interruption"):
            self.run_attach(apply=True)
        self.assertEqual(self.api.uploads, [self.assets[0].name])
        self.api.fail_upload_number = None
        self.run_attach(apply=True)
        self.assertEqual(self.api.uploads, [a.name for a in self.assets])

    def test_missing_digest_uses_bytes_and_rejects_corruption(self):
        name = self.assets[0].name
        self.api.target[name] = self.api.asset(name, self.data[name], TAG)
        self.api.target[name]["digest"] = None
        self.api.corrupt.add(name)
        with self.assertRaisesRegex(subject.VerificationError, "SHA-256 mismatch"):
            self.run_attach(apply=True)
        self.assertEqual(self.api.uploads, [])

    def test_verification_mode_validates_downloads_without_uploading(self):
        result = self.run_attach()
        self.assertEqual(len(result["missing"]), len(self.assets))
        self.assertEqual(len(self.api.downloads), len(self.assets))
        self.assertEqual(self.api.uploads, [])

    def test_tag_and_repository_boundaries(self):
        for tag in ("PRAYCG_Workbench_AUL_A1.8.2", "PRAYCG_Workbench_Public_A11.9.2-extra",
                    "PRAYCG_Workbench_Public_A11.9", "../main", "PRAYCG_Workbench_Public_A11.9.2\n"):
            with self.subTest(tag=tag), self.assertRaises(subject.VerificationError):
                subject.attach(self.api, tag, assets=self.assets, apply=True)
        with self.assertRaises(subject.VerificationError):
            subject.attach(self.api, TAG, "someone/else", assets=self.assets, apply=True)
        self.assertEqual(self.api.uploads, [])

    def test_draft_or_private_repository_is_rejected(self):
        self.api.draft = True
        with self.assertRaises(subject.VerificationError):
            self.run_attach(apply=True)
        self.api.draft = False
        self.api.private = True
        with self.assertRaises(subject.VerificationError):
            self.run_attach(apply=True)
        self.assertEqual(self.api.uploads, [])

    def test_allowlist_is_exactly_two_packs_with_companions(self):
        self.assertEqual(len(subject.ASSETS), 6)
        self.assertEqual(len({a.name for a in subject.ASSETS}), 6)
        self.assertEqual(sum(a.name.endswith(".zip") for a in subject.ASSETS), 2)
        self.assertEqual(sum(a.name.endswith(".manifest.json") for a in subject.ASSETS), 2)
        self.assertEqual(sum(a.name.endswith(".zip.sha256") for a in subject.ASSETS), 2)


if __name__ == "__main__":
    unittest.main()
