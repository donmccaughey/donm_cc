import unittest

from html import format_tags, Img, Input


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


if __name__ == '__main__':
    unittest.main()
