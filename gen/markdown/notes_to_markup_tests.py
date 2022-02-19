import unittest

from markdown import note_to_markup
from markup import Text, Code, P, Em, A, Strong


class NotesToMarkupTestCase(unittest.TestCase):

    def test_empty(self):
        p = note_to_markup('')
        self.assertIsInstance(p, P)
        self.assertEqual(0, len(p.children))

    def test_codeinline(self):
        p = note_to_markup('`foobar`')
        self.assertIsInstance(p, P)
        self.assertEqual(1, len(p.children))
        self.assertIsInstance(p.children[0], Code)
        code: Code = p.children[0]

        self.assertEqual(1, len(code.children))
        self.assertIsInstance(code.children[0], Text)

        text: Text = code.children[0]
        self.assertEqual('foobar', text.text)

    def test_em(self):
        p = note_to_markup('_foobar_')
        self.assertIsInstance(p, P)
        self.assertEqual(1, len(p.children))
        self.assertIsInstance(p.children[0], Em)

        em: Em = p.children[0]
        self.assertEqual(1, len(em.children))
        self.assertIsInstance(em.children[0], Text)

        text: Text = em.children[0]
        self.assertEqual('foobar', text.text)

    def test_link(self):
        p = note_to_markup('[foobar](https://example.com/)')
        self.assertIsInstance(p, P)
        self.assertEqual(1, len(p.children))
        self.assertIsInstance(p.children[0], A)

        a: A = p.children[0]
        self.assertEqual('https://example.com/', a.attributes['href'])
        self.assertEqual(1, len(a.children))
        self.assertIsInstance(a.children[0], Text)

        text: Text = a.children[0]
        self.assertEqual('foobar', text.text)

    def test_softbreak(self):
        p = note_to_markup('Line 1\nLine 2')
        self.assertIsInstance(p, P)
        self.assertEqual(3, len(p.children))

        self.assertIsInstance(p.children[0], Text)
        text1: Text = p.children[0]
        self.assertEqual('Line 1', text1.text)

        self.assertIsInstance(p.children[1], Text)
        text2: Text = p.children[1]
        self.assertEqual(' ', text2.text)

        self.assertIsInstance(p.children[2], Text)
        text3: Text = p.children[2]
        self.assertEqual('Line 2', text3.text)

    def test_text(self):
        p = note_to_markup('This is a test.')
        self.assertIsInstance(p, P)
        self.assertEqual(1, len(p.children))
        self.assertIsInstance(p.children[0], Text)

        text: Text = p.children[0]
        self.assertEqual('This is a test.', text.text)

    def test_strong(self):
        # The markdown snipped '**foobar**' parses as "text", not "strong",
        # so pad with spaces for this test.
        p = note_to_markup(' **foobar** ')
        self.assertIsInstance(p, P)
        self.assertEqual(3, len(p.children))

        self.assertIsInstance(p.children[0], Text)
        text1: Text = p.children[0]
        self.assertEqual(' ', text1.text)

        strong: Strong = p.children[1]
        self.assertEqual(1, len(strong.children))
        self.assertIsInstance(strong.children[0], Text)

        text: Text = strong.children[0]
        self.assertEqual('foobar', text.text)

        self.assertIsInstance(p.children[2], Text)
        text2: Text = p.children[2]
        self.assertEqual(' ', text2.text)


if __name__ == '__main__':
    unittest.main()
