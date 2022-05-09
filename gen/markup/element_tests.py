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

    def test_matches_element_selector(self):
        element = Element('p', id='foo', class_names=['bar', 'baz'])
        self.assertTrue(element.matches('p'))
        self.assertFalse(element.matches('a'))

    def test_matches_element_with_pseudo_selector(self):
        element = Element('a', id='foo', class_names=['bar', 'baz'])
        self.assertTrue(element.matches('a'))
        self.assertTrue(element.matches('a:visited'))
        self.assertFalse(element.matches('p'))

    def test_matches_element_plus_class_selector(self):
        element = Element('a', id='foo', class_names=['bar', 'baz'])
        self.assertTrue(element.matches('a'))
        self.assertTrue(element.matches('a:visited'))
        self.assertTrue(element.matches('a.bar'))
        self.assertTrue(element.matches('a.baz'))
        self.assertTrue(element.matches('a.bar.baz'))
        self.assertTrue(element.matches('a.baz:before'))
        self.assertFalse(element.matches('p'))
        self.assertFalse(element.matches('a.foo'))
        self.assertFalse(element.matches('a.bar.foo'))

    def test_matches_id_selector(self):
        element = Element('p', id='foo', class_names=['bar', 'baz'])
        self.assertTrue(element.matches('#foo'))
        self.assertFalse(element.matches('#bar'))

    def test_matches_class_selector(self):
        element = Element('p', id='foo', class_names=['bar', 'baz'])
        self.assertTrue(element.matches('.bar'))
        self.assertTrue(element.matches('.baz'))
        self.assertFalse(element.matches('.foo'))

    def test_matches_empty_selector(self):
        element = Element('p', id='foo', class_names=['bar', 'baz'])
        self.assertRaises(AssertionError, element.matches, '')
        self.assertRaises(AssertionError, element.matches, '#')
        self.assertRaises(AssertionError, element.matches, '.')

    def test_matches_compound_selector(self):
        element = Element('p', id='foo', class_names=['bar', 'baz'])
        self.assertRaises(AssertionError, element.matches, 'p a')


if __name__ == '__main__':
    unittest.main()
