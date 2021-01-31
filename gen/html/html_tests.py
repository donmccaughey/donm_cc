import unittest
from textwrap import dedent
from html import format_tags, Img, Input, P, Div, Text, A
from html.comment import Comment
from html.block_element import BlockA, Body, HTML


class FormatTagsTestCase(unittest.TestCase):
    def test_img_element(self):
        img = Img(src='mypic.jpg', alt='Me!')
        tags = img.tags()

        self.assertEqual(2, len(tags))
        self.assertEqual(
            dedent(
                """
                <img src=mypic.jpg alt=Me!>
                """
            ),
            format_tags(tags)
        )

    def test_input_element(self):
        input = Input(id='count', type='number', value='0')
        tags = input.tags()

        self.assertEqual(2, len(tags))
        self.assertEqual(
            dedent(
                """
                <input id=count name=count type=number value=0>
                """
            ),
            format_tags(tags)
        )


class FormatTagsBodyTestCase(unittest.TestCase):
    def test_body_omits_end_tag_when_no_next_sibling(self):
        html = HTML(lang='en')
        with html:
            Body()

        self.assertEqual(
            dedent(
                """
                <html lang=en>
                <body>
                </html>
                """
            ),
            format_tags(html.tags())
        )

    def test_body_keeps_end_tag_when_next_sibling_is_comment(self):
        html = HTML(lang='en')
        with html:
            Body()
            Comment('a comment')

        self.assertEqual(
            dedent(
                """
                <html lang=en>
                <body>
                </body>
                <!-- a comment -->
                </html>
                """
            ),
            format_tags(html.tags())
        )


class FormatTagsParagraphTestCase(unittest.TestCase):
    def test_omits_end_tag_when_no_parent(self):
        p = P('text')
        self.assertEqual(
            dedent(
                """
                <p>
                    text
                """
            ),
            format_tags(p.tags())
        )

    def test_omits_end_tag_when_last_sibling(self):
        d = Div()
        with d:
            P('text')

        self.assertEqual(
            dedent(
                """
                <div>
                    <p>
                        text
                </div>
                """
            ),
            format_tags(d.tags())
        )

    def test_keeps_end_tag_when_last_sibling_and_parent_is_a(self):
        a = BlockA(href='/')
        with a:
            P('text')

        self.assertEqual(
            dedent(
                """
                <a href=/>
                    <p>
                        text
                    </p>
                </a>
                """
            ),
            format_tags(a.tags())
        )

    def test_omits_end_tag_when_next_sibling_is_p(self):
        d = Div()
        with d:
            P('text')
            P('more text')

        self.assertEqual(
            dedent(
                """
                <div>
                    <p>
                        text
                    <p>
                        more text
                </div>
                """
            ),
            format_tags(d.tags())
        )

    def test_keeps_end_tag_when_next_sibling_is_text(self):
        d = Div()
        with d:
            P('text')
            Text('more text')

        self.assertEqual(
            dedent(
                """
                <div>
                    <p>
                        text
                    </p>
                    more text
                </div>
                """
            ),
            format_tags(d.tags())
        )


if __name__ == '__main__':
    unittest.main()
