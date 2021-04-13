import unittest

from website.links import join_authors


class JoinAuthorsTestCase(unittest.TestCase):
    def test_one_author(self):
        authors = ['Alice Author']
        expected = 'Alice Author'
        self.assertEqual(expected, join_authors(authors))

    def test_two_author(self):
        authors = ['Alice Author', 'Bob Booker']
        expected = 'Alice Author and Bob Booker'
        self.assertEqual(expected, join_authors(authors))

    def test_three_author(self):
        authors = ['Alice Author', 'Bob Booker', 'Carlos Card']
        expected = 'Alice Author, Bob Booker and Carlos Card'
        self.assertEqual(expected, join_authors(authors))


if __name__ == '__main__':
    unittest.main()
