import unittest
from textwrap import dedent

from html import Title


class CompactElementTestCase(unittest.TestCase):
    def test_markup_for_short_line(self):
        title = Title('This is a short title.')
        self.assertEqual(
            '<title>This is a short title.</title>\n',
            title.markup(width=40)
        )

    def test_markup_for_long_line(self):
        title = Title('This is a very very very extremely long title.')
        self.assertEqual(
            dedent(
                """\
                <title>
                    This is a very very very extremely
                    long title.
                </title>
                """
              # 0123456789012345678901234567890123456789
            ),
            title.markup(width=40)
        )


if __name__ == '__main__':
    unittest.main()
