import contextlib
import importlib.util
import io
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('check_catalog', ROOT / 'scripts/check_catalog.py')
catalog = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(catalog)


def table(*rows):
    return '| Project | What it verifies |\n| --- | --- |\n' + '\n'.join(rows)


class CatalogTests(unittest.TestCase):
    def test_actual_catalog(self):
        count, errors = catalog.check_catalog((ROOT / 'README.md').read_text(encoding='utf-8'))
        self.assertGreater(count, 0)
        self.assertEqual(errors, [])

    def test_valid_entry(self):
        self.assertEqual(catalog.check_catalog(table('| [Example](https://github.com/a/b) | Analytic reference |')), (1, []))

    def test_duplicate_case_and_trailing_slash(self):
        _, errors = catalog.check_catalog(table(
            '| [One](https://github.com/A/B) | Analytic reference |',
            '| [Two](https://github.com/a/b/) | Independent calculation |'))
        self.assertTrue(any('duplicate' in error for error in errors))

    def test_duplicate_across_sections(self):
        text = table('| [One](https://github.com/a/b) | Reference |')
        text += '\n\n## Another section\n' + text
        self.assertTrue(any('duplicate' in error for error in catalog.check_catalog(text)[1]))

    def test_noncanonical_urls(self):
        for url in ['http://github.com/a/b', 'https://github.com/a/b/tree/main',
                    'https://github.com/a/b#readme', 'https://github.com/a/b?q=1',
                    'https://github.com.evil.example/a/b', 'https://user@github.com/a/b',
                    'https://github.com/a', 'https://github.com/a/..', 'https://[broken']:
            with self.subTest(url=url):
                self.assertTrue(catalog.check_catalog(table(f'| [Name]({url}) | Reference |'))[1])

    def test_missing_description(self):
        for description in ['', '  ', 'TODO', 'tbd']:
            with self.subTest(description=description):
                self.assertTrue(catalog.check_catalog(table(f'| [Name](https://github.com/a/b) | {description} |'))[1])

    def test_malformed_or_unnamed_link(self):
        for name in ['Example', '[](https://github.com/a/b)', '[Name](broken link)']:
            with self.subTest(name=name):
                self.assertTrue(catalog.check_catalog(table(f'| {name} | Reference |'))[1])

    def test_unescaped_pipe(self):
        self.assertTrue(catalog.check_catalog(table('| [Name](https://github.com/a/b) | A | B |'))[1])

    def test_escaped_pipe(self):
        self.assertEqual(catalog.check_catalog(table(r'| [Name](https://github.com/a/b) | Checks A \| B |'))[1], [])

    def test_empty_catalog(self):
        self.assertTrue(catalog.check_catalog('# Nothing listed')[1])

    def test_unrelated_tables_ignored(self):
        text = '| Other | Thing |\n| --- | --- |\n| x | y |\n\n'
        text += table('| [Name](https://github.com/a/b) | Reference |')
        self.assertEqual(catalog.check_catalog(text), (1, []))

    def test_cli_errors(self):
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(catalog.main(['a', 'b']), 2)
            with tempfile.TemporaryDirectory() as folder:
                self.assertEqual(catalog.main([str(Path(folder) / 'absent.md')]), 2)

    def test_cli_invalid_file_and_utf8_bom(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'catalog.md'
            path.write_text('# Empty', encoding='utf-8')
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(catalog.main([str(path)]), 1)
            path.write_text(table('| [Name](https://github.com/a/b) | Reference |'), encoding='utf-8-sig')
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(catalog.main([str(path)]), 0)


if __name__ == '__main__':
    unittest.main()
