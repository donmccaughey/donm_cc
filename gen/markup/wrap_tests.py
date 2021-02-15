import unittest
from markup.wrap import wrap_tokens


class WrapTokensTestCase(unittest.TestCase):
    def test_wrap_tokens_for_empty_list(self):
        tokens = []
        self.assertEqual(
            [],
            wrap_tokens(tokens, 10)
        )

    def test_wrap_single_word(self):
        tokens = ['foobar']
        self.assertEqual(
            ['foobar'],
            wrap_tokens(tokens, 10)
        )

    def test_wrap_single_word_exact_width(self):
        tokens = ['1234567890']
        self.assertEqual(
            ['1234567890'],
            wrap_tokens(tokens, 10)
        )

    def test_wrap_single_long_word(self):
        tokens = ['1234567890FOOBAR']
        self.assertEqual(
            ['1234567890FOOBAR'],
            wrap_tokens(tokens, 10)
        )

    def test_wrap_tokens_for_short_sentence(self):
        tokens = ['This', ' ', 'is']
        self.assertEqual(
            ['This', ' ', 'is'],
            wrap_tokens(tokens, 10)
        )

    def test_wrap_tokens_for_long_sentence(self):
        tokens = [
            'This', ' ', 'is', ' ',
            'some', ' ', 'text.'
        ]
        self.assertEqual(
            [
                'This', ' ', 'is', '\n',
                'some', ' ', 'text.'
            ],
            wrap_tokens(tokens, 10)
        )

    def test_wrap_tokens_for_lines_breaking_before_width(self):
        tokens = [
            '1234', ' ', '1234', ' ',
            '1234', ' ', '1234',
            ]
        self.assertEqual(
            [
                '1234', ' ', '1234', '\n',
                '1234', ' ', '1234',
            ],
            wrap_tokens(tokens, 10)
        )

    def test_wrap_tokens_for_lines_breaking_at_width(self):
        tokens = [
            '1234', ' ', '12345', ' ',
            '1234', ' ', '12345',
            ]
        self.assertEqual(
            [
                '1234', ' ', '12345', '\n',
                '1234', ' ', '12345',
            ],
            wrap_tokens(tokens, 10)
        )

    def test_wrap_tokens_for_sentence_with_long_word(self):
        tokens = [
            '1234', ' ', '1234', ' ',
            '1234567890FOOBAR', ' ',
            '1234', ' ', '1234',
            ]
        self.assertEqual(
            [
                '1234', ' ', '1234', '\n',
                '1234567890FOOBAR', '\n',
                '1234', ' ', '1234',
            ],
            wrap_tokens(tokens, 10)
        )

    def test_wrap_tokens_for_sentence_that_starts_with_long_word(self):
        tokens = [
            '1234567890FOOBAR', ' ',
            '1234', ' ', '1234',
            ]
        self.assertEqual(
            [
                '1234567890FOOBAR', '\n',
                '1234', ' ', '1234',
            ],
            wrap_tokens(tokens, 10)
        )

    def test_wrap_tokens_for_sentence_that_ends_with_long_word(self):
        tokens = [
            '1234', ' ', '1234', ' ',
            '1234567890FOOBAR',
            ]
        self.assertEqual(
            [
                '1234', ' ', '1234', '\n',
                '1234567890FOOBAR',
            ],
            wrap_tokens(tokens, 10)
        )

    def test_wrap_tokens_for_starting_space(self):
        tokens = [
            ' ', 'This', ' ', 'is', ' ',
            'some', ' ', 'text.'
        ]
        self.assertEqual(
            [
                ' ', 'This', ' ', 'is', '\n',
                'some', ' ', 'text.'
            ],
            wrap_tokens(tokens, 10)
        )

    def test_wrap_tokens_for_ending_space(self):
        tokens = [
            'This', ' ', 'is', ' ',
            'some', ' '
        ]
        self.assertEqual(
            [
                'This', ' ', 'is', '\n',
                'some', ' '
            ],
            wrap_tokens(tokens, 10)
        )

    def test_wrap_tokens_for_ending_space_at_width(self):
        tokens = [
            'This', ' ', 'is', ' ',
            'some', ' ', 'text.', ' '
        ]
        self.assertEqual(
            [
                'This', ' ', 'is', '\n',
                'some', ' ', 'text.', '\n'
            ],
            wrap_tokens(tokens, 10)
        )

    def test_wrap_tokens_for_ending_space_beyond_width(self):
        tokens = [
            'This', ' ', 'is', ' ',
            'a_really_long_word.', ' '
        ]
        self.assertEqual(
            [
                'This', ' ', 'is', '\n',
                'a_really_long_word.', '\n'
            ],
            wrap_tokens(tokens, 10)
        )

    def test_wrap_tokens_adjacent_words(self):
        tokens = [
            '<em>', 'This', '</em>', ' ',
            'is', ' ', 'some', ' ',
            'text.'
        ]
        self.assertEqual(
            [
                '<em>', 'This', '</em>', '\n',
                'is', ' ', 'some', '\n',
                'text.'
            ],
            wrap_tokens(tokens, 10)
        )

    def test_wrap_tokens_walks_back_to_break_for_adjacent_words(self):
        tokens = [
            'Find', ' ', 'a', ' ',
            '<i>', '<strong>', 'needle', '</strong>', '</i>', ' ',
            'in', ' ', 'a', ' ',
            'haystack.'
        ]
        self.assertEqual(
            [
                'Find', ' ', 'a', '\n',
                '<i>', '<strong>', 'needle', '</strong>', '</i>', '\n',
                'in', ' ', 'a', '\n',
                'haystack.'
            ],
            wrap_tokens(tokens, 10)
        )

    def test_wrap_tokens_wont_break_on_initial_space(self):
        tokens = [
            ' ', '<i>', '<strong>', 'needle', '</strong>', '</i>', ' ',
            'in', ' ', 'a', ' ',
            'haystack.'
        ]
        self.assertEqual(
            [
                ' ', '<i>', '<strong>', 'needle', '</strong>', '</i>', '\n',
                'in', ' ', 'a', '\n',
                'haystack.'
            ],
            wrap_tokens(tokens, 10)
        )

    def test_wrap_adds_two_spaces_after_a_period(self):
        tokens = [
            'This', ' ', 'is', ' ', 'a', ' ', 'sentence.', ' ',
            'And', ' ', 'so', ' ', 'is', ' ', 'this.'
        ]
        self.assertEqual(
            [
                'This', ' ', 'is', ' ', 'a', ' ', 'sentence.', '  ',
                'And', ' ', 'so', ' ', 'is', ' ', 'this.'
            ],
            wrap_tokens(tokens, 80)
        )

    def test_wrap_adds_two_spaces_after_a_period_inside_markup(self):
        tokens = [
            '<em>', 'This', ' ', 'is', ' ', 'a', ' ', 'sentence.', '</em>', ' ',
            'And', ' ', 'so', ' ', 'is', ' ', 'this.'
        ]
        self.assertEqual(
            [
                '<em>', 'This', ' ', 'is', ' ', 'a', ' ', 'sentence.', '</em>', '  ',
                'And', ' ', 'so', ' ', 'is', ' ', 'this.'
            ],
            wrap_tokens(tokens, 80)
        )

    def test_wrap_breaks_line_after_a_period(self):
        tokens = [
            'This', ' ', 'is', ' ', 'a', ' ', 'sentence.', ' ',
            'And', ' ', 'so', ' ', 'is', ' ', 'this.'
        ]
        self.assertEqual(
            [
                'This', ' ', 'is', ' ', 'a', ' ', 'sentence.', '\n',
                'And', ' ', 'so', ' ', 'is', ' ', 'this.'
            ],
            wrap_tokens(tokens, 20)
        )


if __name__ == '__main__':
    unittest.main()
