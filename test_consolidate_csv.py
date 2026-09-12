import csv
import tempfile
import unittest
from pathlib import Path
from consolidate_csv import consolidate


class ConsolidationTests(unittest.TestCase):
    def test_roundtrip_preserves_quotes_accents_and_duplicates(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'one.csv'
            source.write_text('nombre,nota\nJosé,"hola, mundo"\nJosé,"hola, mundo"\n', encoding='utf-8-sig')
            out, report = root / 'out.csv', root / 'report.html'
            self.assertEqual(consolidate([source], out, report), 2)
            with out.open(encoding='utf-8-sig', newline='') as stream:
                self.assertEqual(list(csv.reader(stream))[1:], [['José', 'hola, mundo']] * 2)

    def test_mismatch_does_not_create_outputs(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            a, b = root/'a.csv', root/'b.csv'
            a.write_text('a,b\n1,2\n'); b.write_text('b,a\n2,1\n')
            with self.assertRaises(ValueError):
                consolidate([a,b], root/'out.csv', root/'report.html')
            self.assertFalse((root/'out.csv').exists())

    def test_protects_original_and_existing_output(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); a = root/'a.csv'
            original = 'a;b\n1;2\n'; a.write_text(original)
            with self.assertRaises(ValueError):
                consolidate([a], a, root/'report.html', ';')
            self.assertEqual(a.read_text(), original)
            self.assertEqual(consolidate([a], root/'out.csv', root/'report.html', ';'), 1)
            with self.assertRaises(ValueError):
                consolidate([a], root/'out.csv', root/'another.html', ';')

if __name__ == '__main__':
    unittest.main()
