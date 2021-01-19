import unittest
from textwrap import dedent
from html import Document, DocType, HTML
from html.comment import Comment


class DocumentTestCase(unittest.TestCase):
    def test_markup_for_empty_document(self):
        document = Document()
        self.assertEqual('', document.markup(width=80))

    def test_markup(self):
        document = Document()
        with document:
            DocType()
            HTML(lang='en')
            Comment('a comment')
        self.assertEqual(
            dedent(
                """\
                <!doctype html>
                <html lang=en>
                </html>
                <!-- a comment -->
                """
            ),
            document.markup(width=80)
        )


if __name__ == '__main__':
    unittest.main()
