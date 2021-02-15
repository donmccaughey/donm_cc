import unittest
from textwrap import dedent

from markup import Span


class SpanTestCase(unittest.TestCase):
    def test_markup_for_short_line(self):
        span = Span('This is some text.')
        self.assertEqual(
            '<span>This is some text.</span>',
            span.markup(width=80)
        )

    def test_markup_for_long_line(self):
        line = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
        assert len(line) > 40
        span = Span(line)
        self.assertEqual(
            dedent(
                """\
                <span>Lorem ipsum dolor sit amet,
                consectetur adipiscing elit, sed do
                eiusmod tempor incididunt ut labore et
                dolore magna aliqua.</span>"""
            ),
            span.markup(width=40)
        )


if __name__ == '__main__':
    unittest.main()
