import io
import tempfile
import unittest
from pathlib import Path
import zipfile

import restore_historical_links as restore


class RestorationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.addCleanup(self.temp.cleanup)
        self.data = b'Exact historical notice\r\n'
        self.row = {'path': 'docs/snapshot/LICENSE.txt', 'source': 'archive',
                    'member': 'package/LICENSE.txt', 'bytes': len(self.data),
                    'sha256': restore.digest(self.data)}
        stream = io.BytesIO()
        with zipfile.ZipFile(stream, 'w') as archive:
            archive.writestr(self.row['member'], self.data)
        self.zip = stream.getvalue()
        self.spec = {'url': 'https://github.com/hbanks87/praycg-open/releases/download/v1/package.zip',
                     'kind': 'zip', 'bytes': len(self.zip), 'sha256': restore.digest(self.zip)}
        self.plan = {'sources': {'archive': self.spec}, 'files': [self.row]}

    def prepare(self, loader=None):
        return restore.prepare(self.plan, self.root, self.root/'cache',
                               loader or (lambda spec, cache: self.zip))

    def test_exact_restoration_and_idempotent_second_run(self):
        (self.root/'original.md').write_bytes(b'Original remains untouched')
        result = restore.apply(self.prepare())
        self.assertEqual(result['added'], [self.row['path']])
        self.assertEqual((self.root/self.row['path']).read_bytes(), self.data)
        self.assertEqual((self.root/'original.md').read_bytes(), b'Original remains untouched')
        self.assertEqual(restore.apply(self.prepare())['already_identical'], [self.row['path']])

    def test_archive_mismatch_refuses_before_writes(self):
        with self.assertRaisesRegex(ValueError, 'Identity mismatch'):
            self.prepare(lambda spec, cache: b'wrong archive')
        self.assertFalse((self.root/'docs').exists())

    def test_member_mismatch_refuses_before_writes(self):
        self.row['sha256'] = '0'*64
        with self.assertRaisesRegex(ValueError, 'Identity mismatch'):
            self.prepare()
        self.assertFalse((self.root/'docs').exists())

    def test_late_conflict_cannot_change_any_existing_or_missing_target(self):
        original = self.root/'docs/untouched.md'
        original.parent.mkdir()
        original.write_bytes(b'Original')
        self.plan['files'].append({'path': 'docs/untouched.md', 'inline_utf8': 'Replacement',
                                  'bytes': 11, 'sha256': restore.digest(b'Replacement')})
        with self.assertRaisesRegex(ValueError, 'Refusing to change existing'):
            self.prepare()
        self.assertEqual(original.read_bytes(), b'Original')
        self.assertFalse((self.root/self.row['path']).exists())

    def test_unsafe_paths_are_rejected(self):
        for path in ['../escape', '/absolute', 'docs/../escape', '.git/config',
                     '.github/workflows/change.yml', 'docs\\escape', 'docs/a:stream']:
            with self.subTest(path=path), self.assertRaises(ValueError):
                restore.destination(self.root, path)

    def test_unpinned_or_unrelated_sources_are_rejected(self):
        for url in ['http://github.com/hbanks87/praycg-open/releases/download/v1/x',
                    'https://raw.githubusercontent.com/hbanks87/praycg-open/main/x',
                    'https://github.com/other/repo/releases/download/v1/x']:
            spec = dict(self.spec, url=url)
            with self.subTest(url=url), self.assertRaises(ValueError):
                restore.validate_source(spec)

    def test_duplicate_target_is_rejected_before_any_write(self):
        self.plan['files'].append(dict(self.row))
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            self.prepare()
        self.assertFalse((self.root/'docs').exists())

    def test_raw_commit_source_and_labelled_locator_preserve_exact_bytes(self):
        self.spec.update(kind='raw', bytes=len(self.data), sha256=restore.digest(self.data),
                         url='https://raw.githubusercontent.com/hbanks87/praycg-open/'+'a'*40+'/LICENSE')
        text = '# Historical path recovery\n\nUse the preserved original.\n'
        self.plan['files'].append({'path':'docs/old-guide.md','inline_utf8':text,
                                  'bytes':len(text.encode()),'sha256':restore.digest(text.encode())})
        result = restore.apply(self.prepare(lambda spec, cache: self.data))
        self.assertEqual(len(result['added']), 2)
        self.assertEqual((self.root/'docs/old-guide.md').read_bytes(), text.encode())


if __name__ == '__main__':
    unittest.main()
