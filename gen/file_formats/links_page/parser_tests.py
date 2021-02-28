import unittest
from textwrap import dedent

from file_formats.links_page import LinksPage
from file_formats.links_page.parser import Parser, ParserError, \
    MissingDirectiveError, MissingModifierError, MissingDataError, \
    UnexpectedTokenError


class ParserTestCase(unittest.TestCase):

    def test_empty_file(self):
        source = ''
        parser = Parser(source)
        result = parser.parse()
        self.assertIsInstance(result, MissingDirectiveError)
        self.assertEqual('page', result.directive)

    def test_page_directive_missing_modifier(self):
        source = '.page'
        parser = Parser(source)
        result = parser.parse()
        self.assertIsInstance(result, MissingModifierError)
        self.assertEqual('links', result.modifier)

    def test_page_directive_missing_title(self):
        source = '.page links'
        parser = Parser(source)
        result = parser.parse()
        self.assertIsInstance(result, MissingDataError)
        self.assertEqual('page title', result.data_description)

    def test_page_directive_only(self):
        source = '.page links My Links'
        parser = Parser(source)
        result = parser.parse()
        self.assertIsInstance(result, LinksPage)
        self.assertEqual('My Links', result.title)
        self.assertEqual([], result.notes)
        self.assertEqual([], result.sections)

    def test_page_directive_invalid_modifier(self):
        source = '.page invalid My Links'
        parser = Parser(source)
        result = parser.parse()
        self.assertIsInstance(result, MissingModifierError)
        self.assertEqual('links', result.modifier)

    def test_page_directive_invalid_data(self):
        source = dedent('''
        .page links 
        
        This is a paragraph.
        ''')
        parser = Parser(source)
        result = parser.parse()
        self.assertIsInstance(result, MissingDataError)
        self.assertEqual('page title', result.data_description)

    def test_page_directive_with_one_paragraph(self):
        source = dedent('''
        .page links My Links
        
        This is a paragraph.
        ''')
        parser = Parser(source)
        result = parser.parse()
        self.assertIsInstance(result, LinksPage)
        self.assertEqual('My Links', result.title)
        self.assertEqual(['This is a paragraph.'], result.notes)
        self.assertEqual([], result.sections)

    def test_page_directive_with_paragraphs(self):
        source = dedent('''
        .page links My Links
        This is the first paragraph.
        
        This is the second paragraph.
        
        This is the third paragraph.
        ''')
        parser = Parser(source)
        result = parser.parse()
        self.assertIsInstance(result, LinksPage)
        self.assertEqual('My Links', result.title)
        self.assertEqual(
            [
                'This is the first paragraph.',
                'This is the second paragraph.',
                'This is the third paragraph.',
            ],
            result.notes
        )
        self.assertEqual([], result.sections)

    def test_page_directive_twice(self):
        source = dedent('''
        .page links My Links

        .page
        ''')
        parser = Parser(source)
        result = parser.parse()
        self.assertIsInstance(result, UnexpectedTokenError)

    def test_section_directive_missing_modifier(self):
        source = dedent('''
        .page links My Links
        
        .section
        ''')
        parser = Parser(source)
        result = parser.parse()
        self.assertIsInstance(result, MissingModifierError)
        self.assertEqual('links', result.modifier)

    def test_section_directive_missing_title(self):
        source = dedent('''
        .page links My Links
        
        .section links
        ''')
        parser = Parser(source)
        result = parser.parse()
        self.assertIsInstance(result, MissingDataError)
        self.assertEqual('section title', result.data_description)

    def test_empty_section(self):
        source = dedent('''
        .page links My Links
        
        .section links New Links
        
        ''')
        parser = Parser(source)
        result = parser.parse()
        self.assertIsInstance(result, LinksPage)
        self.assertEqual(1, len(result.sections))

        section = result.sections[0]
        self.assertEqual('New Links', section.title)
        self.assertEqual([], section.notes)
        self.assertEqual([], section.links)

    def test_section_with_paragraph(self):
        source = dedent('''
        .page links My Links

        .section links New Links
        
        These are some links.
        ''')
        parser = Parser(source)
        result = parser.parse()
        self.assertIsInstance(result, LinksPage)
        self.assertEqual(1, len(result.sections))

        section = result.sections[0]
        self.assertEqual('New Links', section.title)
        self.assertEqual(['These are some links.'], section.notes)
        self.assertEqual([], section.links)

    def test_section_with_multiple_paragraph(self):
        source = dedent('''
        .page links My Links

        .section links New Links
        
        These are some links.
        
        There are many links.
        
        But these are mine.
        ''')
        parser = Parser(source)
        result = parser.parse()
        self.assertIsInstance(result, LinksPage)
        self.assertEqual(1, len(result.sections))

        section = result.sections[0]
        self.assertEqual('New Links', section.title)
        self.assertEqual(
            [
                'These are some links.',
                'There are many links.',
                'But these are mine.',
            ],
            section.notes
        )
        self.assertEqual([], section.links)

    def test_link_directive_missing_modifier(self):
        source = dedent('''
        .page links My Links

        .section links New Links
        
        .link
        ''')
        parser = Parser(source)
        result = parser.parse()
        self.assertIsInstance(result, MissingModifierError)
        self.assertEqual('book', result.modifier)


if __name__ == '__main__':
    unittest.main()
