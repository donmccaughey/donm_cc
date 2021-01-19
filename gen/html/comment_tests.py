import unittest

from html.comment import Comment


class CommentTestCase(unittest.TestCase):
    def test_markup(self):
        comment = Comment('a comment')
        self.assertEqual('<!-- a comment -->\n', comment.markup(width=80))


if __name__ == '__main__':
    unittest.main()
