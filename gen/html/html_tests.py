import unittest

from html import format_tags, Img, Input, P, Div, Text, A
from html.elements import as_block


class FormatTagsTestCase(unittest.TestCase):
    def test_img_element(self):
        img = Img(src='mypic.jpg', alt='Me!')
        tags = img.tags()

        self.assertEqual(2, len(tags))
        self.assertEqual(
            '\n<img src=mypic.jpg alt=Me!>\n',
            format_tags(tags)
        )

    def test_input_element(self):
        input = Input(id='count', type='number', value='0')
        tags = input.tags()

        self.assertEqual(2, len(tags))
        self.assertEqual(
            '\n<input id=count name=count type=number value=0>\n',
            format_tags(tags)
        )


class FormatTagsParagraphTestCase(unittest.TestCase):
    def test_omits_end_tag_when_no_parent(self):
        p = P('text')
        self.assertEqual(
            '\n' +
            '<p>\n' +
            '    text\n',
            format_tags(p.tags())
        )

    def test_omits_end_tag_when_last_sibling(self):
        d = Div()
        with d:
            P('text')

        self.assertEqual(
            '\n' +
            '<div>\n' +
            '    <p>\n' +
            '        text\n' +
            '</div>' +
            '\n',
            format_tags(d.tags())
        )
        self.assertEqual(
            '\n' +
            '<div>\n' +
            '    <p>\n' +
            '        text\n' +
            '</div>' +
            '\n',
            format_tags(d.tags())
        )

    def test_keeps_end_tag_when_last_sibling_and_parent_is_a(self):
        a = as_block(A(href='/'))
        with a:
            P('text')

        self.assertEqual(
            '\n' +
            '<a href=/>\n' +
            '    <p>\n' +
            '        text\n' +
            '    </p>\n' +
            '</a>' +
            '\n',
            format_tags(a.tags())
        )

    def test_omits_end_tag_when_next_sibling_is_p(self):
        d = Div()
        with d:
            P('text')
            P('more text')

        self.assertEqual(
            '\n' +
            '<div>\n' +
            '    <p>\n' +
            '        text\n' +
            '    <p>\n' +
            '        more text\n' +
            '</div>' +
            '\n',
            format_tags(d.tags())
        )

    def test_keeps_end_tag_when_next_sibling_is_text(self):
        d = Div()
        with d:
            P('text')
            Text('more text')

        self.assertEqual(
            '\n' +
            '<div>\n' +
            '    <p>\n' +
            '        text\n' +
            '    </p>\n' +
            '    more text\n' +
            '</div>' +
            '\n',
            format_tags(d.tags())
        )


if __name__ == '__main__':
    unittest.main()
