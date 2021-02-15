import unittest
from textwrap import dedent
from markup import Document, DocType, HTML
from markup.comment import Comment


class DocumentTestCase(unittest.TestCase):
    def test_markup_for_empty_document(self):
        document = Document()
        self.assertEqual('', document.markup(width=80))

    def test_markup(self):
        document = Document()
        with document:
            DocType()
            HTML()
            Comment('a comment')
        self.assertEqual(
            dedent(
                """\
                <!doctype html>
                <html>
                </html>
                <!-- a comment -->
                """
            ),
            document.markup(width=80)
        )


if __name__ == '__main__':
    unittest.main()
