import unittest
from textwrap import dedent

from file_formats.page_file.lexer import lexer, Token, TokenType, Location


class LexerTestCase(unittest.TestCase):

    def test_empty_source(self):
        tokens = list(lexer(''))
        self.assertEqual([], tokens)

    def test_white_space_source(self):
        tokens = list(lexer('    \n\t  \n'))
        self.assertEqual([], tokens)

    def test_directive(self):
        tokens = list(lexer('.checked'))
        self.assertEqual(
            [Token(TokenType.DIRECTIVE, 'checked', Location(1))],
            tokens
        )

    def test_indented_directive(self):
        tokens = list(lexer(' .checked'))
        self.assertEqual(
            [Token(TokenType.PARAGRAPH, ' .checked', Location(1))],
            tokens
        )

    def test_directive_modifier(self):
        tokens = list(lexer('.section links'))
        self.assertEqual(
            [
                Token(TokenType.DIRECTIVE, 'section', Location(1)),
                Token(TokenType.MODIFIER, 'links', Location(1))
             ],
            tokens
        )

    def test_directive_invalid_modifier(self):
        tokens = list(lexer('.section invalid'))
        self.assertEqual(
            [
                Token(TokenType.DIRECTIVE, 'section', Location(1)),
                Token(TokenType.DATA, 'invalid', Location(1))
             ],
            tokens
        )

    def test_directive_modifier_data(self):
        tokens = list(lexer('.section links More Links'))
        self.assertEqual(
            [
                Token(TokenType.DIRECTIVE, 'section', Location(1)),
                Token(TokenType.MODIFIER, 'links', Location(1)),
                Token(TokenType.DATA, 'More Links', Location(1)),
             ],
            tokens
        )

    def test_directive_invalid_modifier_data(self):
        tokens = list(lexer('.section invalid    More Links'))
        self.assertEqual(
            [
                Token(TokenType.DIRECTIVE, 'section', Location(1)),
                Token(TokenType.DATA, 'invalid    More Links', Location(1)),
             ],
            tokens
        )

    def test_directive_modifier_data_trims_whitespace(self):
        tokens = list(lexer('.section   links   More Links \t'))
        self.assertEqual(
            [
                Token(TokenType.DIRECTIVE, 'section', Location(1)),
                Token(TokenType.MODIFIER, 'links', Location(1)),
                Token(TokenType.DATA, 'More Links', Location(1)),
             ],
            tokens
        )

    def test_directive_data(self):
        tokens = list(lexer('.url https://example.com'))
        self.assertEqual(
            [
                Token(TokenType.DIRECTIVE, 'url', Location(1)),
                Token(TokenType.DATA, 'https://example.com', Location(1)),
             ],
            tokens
        )

    def test_directive_data_trims_whitespace(self):
        tokens = list(lexer('.url \t https://example.com   '))
        self.assertEqual(
            [
                Token(TokenType.DIRECTIVE, 'url', Location(1)),
                Token(TokenType.DATA, 'https://example.com', Location(1)),
             ],
            tokens
        )

    def test_paragraph(self):
        source = dedent("""
        Hello, world!
        """)
        tokens = list(lexer(source))
        self.assertEqual(
            [
                Token(TokenType.PARAGRAPH, 'Hello, world!', Location(2)),
             ],
            tokens
        )

    def test_paragraph_trims_trailing_whitespace(self):
        source = 'Hello, world!   '
        tokens = list(lexer(source))
        self.assertEqual(
            [
                Token(TokenType.PARAGRAPH, 'Hello, world!', Location(1)),
             ],
            tokens
        )

    def test_multi_line_paragraph(self):
        source = dedent("""
        Now is the time for
        all good men to come
        to the aid of the party.
        """)
        tokens = list(lexer(source))
        self.assertEqual(
            [
                Token(
                    TokenType.PARAGRAPH,
                    'Now is the time for\nall good men to come\nto the aid of the party.',
                    Location(2)
                ),
             ],
            tokens
        )

    def test_multi_line_paragraph_with_indent(self):
        source = dedent("""
            Now is the time for
        all good men to come
        to the aid of the party.
        """)
        tokens = list(lexer(source))
        self.assertEqual(
            [
                Token(
                    TokenType.PARAGRAPH,
                    '    Now is the time for\nall good men to come\nto the aid of the party.',
                    Location(2)
                ),
             ],
            tokens
        )

    def test_multiple_paragraphs(self):
        source = dedent("""
        This is a paragraph.
        
        This is another paragraph.
        
        And this is a paragraph that
        spans multiple lines.
        """)
        tokens = list(lexer(source))
        self.assertEqual(
            [
                Token(
                    TokenType.PARAGRAPH, 'This is a paragraph.', Location(2)
                ),
                Token(
                    TokenType.PARAGRAPH,
                    'This is another paragraph.',
                    Location(4)
                ),
                Token(
                    TokenType.PARAGRAPH,
                    'And this is a paragraph that\nspans multiple lines.',
                    Location(6)
                ),
             ],
            tokens
        )

    def test_whitespace_lines_separate_paragraphs(self):
        source = 'This is a paragraph.\n    \nThis is another paragraph.'
        tokens = list(lexer(source))
        self.assertEqual(
            [
                Token(TokenType.PARAGRAPH, 'This is a paragraph.', Location(1)),
                Token(
                    TokenType.PARAGRAPH,
                    'This is another paragraph.',
                    Location(3)
                ),
             ],
            tokens
        )

    def test_unescape_leading_dot(self):
        source = r'\.directive'
        tokens = list(lexer(source))
        self.assertEqual(
            [
                Token(TokenType.PARAGRAPH, '.directive', Location(1)),
             ],
            tokens
        )

    def test_unescape_backslash(self):
        source = r'\\. for a literal backslash'
        tokens = list(lexer(source))
        self.assertEqual(
            [
                Token(
                    TokenType.PARAGRAPH,
                    r'\. for a literal backslash',
                    Location(1)
                ),
             ],
            tokens
        )

    def test_paragraph_directive(self):
        source = dedent("""
        This is a paragraph that
        spans multiple lines.
        .section links More Links
        """)
        tokens = list(lexer(source))
        self.assertEqual(
            [
                Token(TokenType.PARAGRAPH,
                      'This is a paragraph that\nspans multiple lines.',
                      Location(2)
                      ),
                Token(TokenType.DIRECTIVE, 'section', Location(4)),
                Token(TokenType.MODIFIER, 'links', Location(4)),
                Token(TokenType.DATA, 'More Links', Location(4)),
            ],
            tokens
        )


if __name__ == '__main__':
    unittest.main()
