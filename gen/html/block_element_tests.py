import unittest
from textwrap import dedent

from html import Body, Div, P, Text, Strong, Em, HTML, Head, Title, Document, \
    Script
from html.comment import Comment


class BodyTestCase(unittest.TestCase):
    def test_markup_for_empty_body(self):
        body = Body()
        self.assertEqual(
            '',
            body.markup(width=80)
        )

    def test_markup(self):
        body = Body()
        with body:
            Div()
        self.assertEqual(
            dedent(
                """\
                <div>
                </div>
                """
            ),
            body.markup(width=80)
        )

    def test_markup_when_followed_by_comment(self):
        html = HTML()
        with html:
            with Head():
                Title('Hello')
            with Body():
                Div()
            Comment('foobar')
        self.assertEqual(
            dedent(
                """\
                <html>
                <title>Hello</title>
                <body>
                    <div>
                    </div>
                </body>
                <!-- foobar -->
                """
            ),
            html.markup(width=80)
        )

    def test_markup_when_first_child_is_comment(self):
        html = HTML()
        with html:
            with Head():
                Title('Hello')
            with Body():
                Comment('foobar')
                Div()
        self.assertEqual(
            dedent(
                """\
                <html>
                <title>Hello</title>
                <body>
                    <!-- foobar -->
                    <div>
                    </div>
                """
            ),
            html.markup(width=80)
        )

    def test_markup_when_first_child_is_script(self):
        html = HTML()
        with html:
            with Head():
                Title('Hello')
            with Body():
                Script(src='foo.js')
        self.assertEqual(
            dedent(
                """\
                <html>
                <title>Hello</title>
                <body>
                    <script src=foo.js type=text/javascript></script>
                """
            ),
            html.markup(width=80)
        )


class DivTestCase(unittest.TestCase):
    def test_markup_for_empty_body(self):
        div = Div()
        self.assertEqual(
            dedent(
                """\
                <div>
                </div>
                """
            ),
            div.markup(width=80)
        )

    def test_markup(self):
        div = Div()
        with div:
            Div()
        self.assertEqual(
            dedent(
                """\
                <div>
                    <div>
                    </div>
                </div>
                """
            ),
            div.markup(width=80)
        )


class HeadTestCase(unittest.TestCase):
    def test_markup(self):
        head = Head()
        with head:
            Title('Hello')
        self.assertEqual(
            dedent(
                """\
                <title>Hello</title>
                """
            ),
            head.markup(width=80)
        )

    def test_markup_when_first_child_is_a_comment(self):
        head = Head()
        with head:
            Comment('foobar')
            Title('Hello')
        self.assertEqual(
            dedent(
                """\
                <head>
                    <!-- foobar -->
                    <title>Hello</title>
                """
            ),
            head.markup(width=80)
        )

    def test_markup_when_followed_by_comment(self):
        html = HTML()
        with html:
            with Head():
                Title('Hello')
            Comment('foobar')
        self.assertEqual(
            dedent(
                """\
                <html>
                <head>
                    <title>Hello</title>
                </head>
                <!-- foobar -->
                """
            ),
            html.markup(width=80)
        )

    def test_markup_when_empty(self):
        html = HTML()
        with html:
            Head()
            Body()
        self.assertEqual(
            dedent(
                """\
                <html>
                """
            ),
            html.markup(width=80)
        )


class HTMLTestCase(unittest.TestCase):
    def test_markup(self):
        html = HTML()
        with html:
            with Head():
                Title('Hello')
            with Body():
                Div()
        self.assertEqual(
            dedent(
                """\
                <html>
                <title>Hello</title>
                <div>
                </div>
                """
            ),
            html.markup(width=80)
        )

    def test_markup_when_followed_by_a_comment(self):
        document = Document()
        with document:
            with HTML():
                with Head():
                    Title('Hello')
                Body()
            Comment('foobar')
        self.assertEqual(
            dedent(
                """\
                <html>
                <title>Hello</title>
                </html>
                <!-- foobar -->
                """
            ),
            document.markup(width=80)
        )


class PTestCase(unittest.TestCase):
    def test_markup_for_empty_body(self):
        p = P()
        self.assertEqual(
            dedent(
                """\
                <p>
                """
            ),
            p.markup(width=80)
        )

    def test_markup(self):
        p = P('A sentence.')
        self.assertEqual(
            dedent(
                """\
                <p>
                    A sentence.
                """
            ),
            p.markup(width=80)
        )

    def test_markup_for_a_sentence_with_leading_and_trailing_space(self):
        p = P(
            dedent("""
            A sentence.
            """)
        )
        self.assertEqual(
            dedent(
                """\
                <p>
                    A sentence.
                """
            ),
            p.markup(width=80)
        )

    def test_markup_for_a_long_sentence(self):
        sentence = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
        p = P(sentence)
        self.assertEqual(
            dedent(
                """\
                <p>
                    Lorem ipsum dolor sit amet,
                    consectetur adipiscing elit, sed do
                    eiusmod tempor incididunt ut labore
                    et dolore magna aliqua.
                """
            ),
            p.markup(width=40)
        )

    def test_markup_for_a_long_sentence_with_phrasing_content(self):
        p = P()
        with p:
            Text('Lorem ipsum dolor sit amet, ')
            Strong('consectetur')
            Text(' adipiscing elit, ')
            Em('sed')
            Text(' do eiusmod tempor incididunt ut ')
            Strong('labore')
            Text(' et dolore magna aliqua.')
        self.assertEqual(
            dedent(
                """\
                <p>
                    Lorem ipsum dolor sit amet,
                    <strong>consectetur</strong>
                    adipiscing elit, <em>sed</em> do
                    eiusmod tempor incididunt ut
                    <strong>labore</strong> et dolore
                    magna aliqua.
                """
            ),
            p.markup(width=40)
        )

    def test_markup_for_a_long_block_with_mixed_flow_and_phrasing_content(self):
        div = Div()
        with div:
            Text('Lorem ipsum dolor sit amet, ')
            Strong('consectetur')
            Text(' adipiscing elit, ')
            with P():
                Em('sed')
                Text(' do eiusmod tempor incididunt ut ')
            Strong('labore')
            Text(' et dolore magna aliqua.')
        self.assertEqual(
            dedent(
                """\
                <div>
                    Lorem ipsum dolor sit amet,
                    <strong>consectetur</strong>
                    adipiscing elit,
                    <p>
                        <em>sed</em> do eiusmod tempor
                        incididunt ut
                    </p>
                    <strong>labore</strong> et dolore
                    magna aliqua.
                </div>
                """
            ),
            div.markup(width=40)
        )


if __name__ == '__main__':
    unittest.main()
