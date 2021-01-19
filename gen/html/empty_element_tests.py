import unittest

from html import Br


class BrTestCase(unittest.TestCase):
    def test_markup(self):
        br = Br()
        self.assertEqual('<br>', br.markup(width=80))


if __name__ == '__main__':
    unittest.main()
