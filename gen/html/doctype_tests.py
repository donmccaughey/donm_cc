import unittest

from html import DocType


class DocTypeTestCase(unittest.TestCase):
    def test_markup(self):
        doc_type = DocType()
        self.assertEqual('<!doctype html>\n', doc_type.markup(width=80))


if __name__ == '__main__':
    unittest.main()
