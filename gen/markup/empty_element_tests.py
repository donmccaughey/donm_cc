import unittest

from markup import Br


class BrTestCase(unittest.TestCase):
    def test_markup(self):
        br = Br()
        self.assertEqual('<br>\n', br.markup(width=80))


if __name__ == '__main__':
    unittest.main()
