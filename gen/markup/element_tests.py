import unittest

from markup.element import Element


class ElementTestCase(unittest.TestCase):
    def test_attribute_ends_with_slash(self):
        element = Element('a')
        element.attributes['href'] = '/'

        self.assertEqual(
            '<a href=/ >',
            element.start_tag()
        )


if __name__ == '__main__':
    unittest.main()
