import unittest

from html.attributes import format_attribute


class AttributesTestCase(unittest.TestCase):
    def test_format_attribute(self):
        self.assertEqual(
            "alt=hello",
            format_attribute('alt', 'hello')
        )

    def test_format_attribute_with_no_value(self):
        self.assertEqual(
            "checked",
            format_attribute('checked', None)
        )

    def test_format_attribute_for_empty_value(self):
        self.assertEqual(
            "href=''",
            format_attribute('href', '')
        )

    def test_format_attribute_for_value_containing_space(self):
        self.assertEqual(
            "alt='Hello, world!'",
            format_attribute('alt', 'Hello, world!')
        )

    def test_format_attribute_for_value_containing_double_quote(self):
        self.assertEqual(
            """alt='"foobar"'""",
            format_attribute('alt', '"foobar"')
        )

    def test_format_attribute_for_value_containing_equals(self):
        self.assertEqual(
            "alt='e=mc^2'",
            format_attribute('alt', 'e=mc^2')
        )

    def test_format_attribute_for_value_containing_less_than(self):
        self.assertEqual(
            "alt='1<2'",
            format_attribute('alt', '1<2')
        )

    def test_format_attribute_for_value_containing_greater_than(self):
        self.assertEqual(
            "alt='2>1'",
            format_attribute('alt', '2>1')
        )

    def test_format_attribute_for_value_containing_backtick(self):
        self.assertEqual(
            "alt='`foobar`'",
            format_attribute('alt', '`foobar`')
        )

    def test_format_attribute_for_value_containing_single_quote(self):
        self.assertEqual(
            '''alt="It's"''',
            format_attribute('alt', "It's")
        )

    def test_format_attribute_for_value_containing_both_quotes(self):
        self.assertEqual(
            '''alt="&quot;It's&quot;"''',
            format_attribute('alt', '''"It's"''')
        )


if __name__ == '__main__':
    unittest.main()
