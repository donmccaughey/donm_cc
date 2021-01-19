import unittest
from textwrap import dedent

from html import Text


class TextTestCase(unittest.TestCase):
    def test_markup_for_short_line(self):
        text = Text('This is some text.')
        self.assertEqual(
            'This is some text.',
            text.markup(width=80)
        )

    def test_markup_for_long_line(self):
        line = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
        assert len(line) > 40
        text = Text(line)
        self.assertEqual(
            dedent(
                """\
                Lorem ipsum dolor sit amet, consectetur
                adipiscing elit, sed do eiusmod tempor
                incididunt ut labore et dolore magna
                aliqua."""
            ),
            text.markup(width=40)
        )

    def test_tokens_single_space(self):
        text = Text(' ')
        expected = [' ']
        self.assertEqual(expected, text.tokens())

    def test_tokens_multiple_spaces(self):
        text = Text(' \r\n\t')
        expected = [' ']
        self.assertEqual(expected, text.tokens())

    def test_tokens_single_word(self):
        text = Text('foobar')
        expected = ['foobar']
        self.assertEqual(expected, text.tokens())

    def test_tokens_short_sentence(self):
        text = Text('This is some text.')
        expected = ['This', ' ', 'is', ' ', 'some', ' ', 'text.']
        self.assertEqual(expected, text.tokens())

    def test_tokens_with_leading_whitespace(self):
        text = Text('    This is some text.')
        expected = [' ', 'This', ' ', 'is', ' ', 'some', ' ', 'text.']
        self.assertEqual(expected, text.tokens())

    def test_tokens_with_trailing_whitespace(self):
        text = Text('This is some text. \r\n')
        expected = ['This', ' ', 'is', ' ', 'some', ' ', 'text.', ' ']
        self.assertEqual(expected, text.tokens())

    def test_tokens_with_internal_whitespace(self):
        text = Text('This is \r\n \tsome text.')
        expected = ['This', ' ', 'is', ' ', 'some', ' ', 'text.']
        self.assertEqual(expected, text.tokens())


if __name__ == '__main__':
    unittest.main()
