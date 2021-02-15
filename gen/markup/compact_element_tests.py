import unittest
from textwrap import dedent

from markup import Title, Li, Ul, Text
from markup.comment import Comment


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


class LiTestCase(unittest.TestCase):
    def test_markup(self):
        ul = Ul()
        with ul:
            with Li():
                Text('First Item')
            with Li():
                Text('Second Item')
        self.assertEqual(
            dedent(
                """\
                <ul>
                    <li>First Item
                    <li>Second Item
                </ul>
                """
            ),
            ul.markup(width=80)
        )

    def test_markup_when_sibling_is_a_comment(self):
        ul = Ul()
        with ul:
            with Li():
                Text('First Item')
            Comment('foobar')
            with Li():
                Text('Second Item')
        self.assertEqual(
            dedent(
                """\
                <ul>
                    <li>First Item</li>
                    <!-- foobar -->
                    <li>Second Item
                </ul>
                """
            ),
            ul.markup(width=80)
        )

    def test_markup_for_long_content_when_sibling_is_a_comment(self):
        lorem = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
        ul = Ul()
        with ul:
            with Li():
                Text(lorem)
            Comment('foobar')
            with Li():
                Text(lorem)
        self.assertEqual(
            dedent(
                """\
                <ul>
                    <li>
                        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
                        tempor incididunt ut labore et dolore magna aliqua.
                    </li>
                    <!-- foobar -->
                    <li>
                        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
                        tempor incididunt ut labore et dolore magna aliqua.
                </ul>
                """
            ),
            ul.markup(width=80)
        )


if __name__ == '__main__':
    unittest.main()
