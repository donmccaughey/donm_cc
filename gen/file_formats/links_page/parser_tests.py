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

    def test_multiple_sections(self):
        source = dedent('''
        .page links My Links
        
        .section links New Links
        
        .section links Old Links
        
        The old stuff.
        
        .section links Really Old Links
        
        The really old stuff.
        ''')
        parser = Parser(source)
        result = parser.parse()
        self.assertIsInstance(result, LinksPage)
        self.assertEqual(3, len(result.sections))

        section = result.sections[0]
        self.assertEqual('New Links', section.title)
        self.assertEqual([], section.notes)
        self.assertEqual([], section.links)

        section = result.sections[1]
        self.assertEqual('Old Links', section.title)
        self.assertEqual(['The old stuff.'], section.notes)
        self.assertEqual([], section.links)

        section = result.sections[2]
        self.assertEqual('Really Old Links', section.title)
        self.assertEqual(['The really old stuff.'], section.notes)
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

    def test_link_directive_missing_title(self):
        source = dedent('''
        .page links My Links

        .section links New Links
        
        .link book
        ''')
        parser = Parser(source)
        result = parser.parse()
        self.assertIsInstance(result, MissingDataError)
        self.assertEqual('link title', result.data_description)

    def test_link_missing_url(self):
        source = dedent('''
        .page links My Links

        .section links New Links
        
        .link book Example Book
        ''')
        parser = Parser(source)
        result = parser.parse()
        self.assertIsInstance(result, MissingDirectiveError)
        self.assertEqual('url', result.directive)

    def test_link_missing_url_followed_by_link_directive(self):
        source = dedent('''
        .page links My Links

        .section links New Links

        .link book Example Book
        .link
        ''')
        parser = Parser(source)
        result = parser.parse()
        self.assertIsInstance(result, MissingDirectiveError)
        self.assertEqual('url', result.directive)

    def test_link_missing_url_data(self):
        source = dedent('''
        .page links My Links

        .section links New Links
        
        .link book Example Book
        .url
        ''')
        parser = Parser(source)
        result = parser.parse()
        self.assertIsInstance(result, MissingDataError)
        self.assertEqual('URL address', result.data_description)

    def test_link(self):
        source = dedent('''
        .page links My Links

        .section links New Links
        
        .link book Example Book
        .url https://example.book
        ''')
        parser = Parser(source)
        result = parser.parse()
        self.assertIsInstance(result, LinksPage)
        self.assertEqual(1, len(result.sections))

        section = result.sections[0]
        self.assertEqual('New Links', section.title)
        self.assertEqual([], section.notes)
        self.assertEqual(1, len(section.links))

        link = section.links[0]
        self.assertEqual('book', link.type)
        self.assertEqual('Example Book', link.title)
        self.assertEqual('https://example.book', link.link)
        self.assertIsNone(link.date)
        self.assertFalse(link.checked)

    def test_link_with_date_missing_value(self):
        source = dedent('''
        .page links My Links

        .section links New Links

        .link book Example Book
        .url https://example.book
        .date
        ''')
        parser = Parser(source)
        result = parser.parse()
        self.assertIsInstance(result, MissingDataError)
        self.assertEqual('date value', result.data_description)

    def test_link_with_date(self):
        source = dedent('''
        .page links My Links

        .section links New Links
        
        .link book Example Book
        .url https://example.book
        .date 2012
        ''')
        parser = Parser(source)
        result = parser.parse()
        self.assertIsInstance(result, LinksPage)
        self.assertEqual(1, len(result.sections))

        section = result.sections[0]
        self.assertEqual('New Links', section.title)
        self.assertEqual([], section.notes)
        self.assertEqual(1, len(section.links))

        link = section.links[0]
        self.assertEqual('book', link.type)
        self.assertEqual('Example Book', link.title)
        self.assertEqual('https://example.book', link.link)
        self.assertEqual('2012', link.date)
        self.assertFalse(link.checked)

    def test_link_with_date_and_checked(self):
        source = dedent('''
        .page links My Links

        .section links New Links
        
        .link book Example Book
        .url https://example.book
        .date 2012
        .checked
        ''')
        parser = Parser(source)
        result = parser.parse()
        self.assertIsInstance(result, LinksPage)
        self.assertEqual(1, len(result.sections))

        section = result.sections[0]
        self.assertEqual('New Links', section.title)
        self.assertEqual([], section.notes)
        self.assertEqual(1, len(section.links))

        link = section.links[0]
        self.assertEqual('book', link.type)
        self.assertEqual('Example Book', link.title)
        self.assertEqual('https://example.book', link.link)
        self.assertEqual('2012', link.date)
        self.assertTrue(link.checked)

    def test_link_with_checked(self):
        source = dedent('''
        .page links My Links

        .section links New Links
        
        .link book Example Book
        .url https://example.book
        .checked
        ''')
        parser = Parser(source)
        result = parser.parse()
        self.assertIsInstance(result, LinksPage)
        self.assertEqual(1, len(result.sections))

        section = result.sections[0]
        self.assertEqual('New Links', section.title)
        self.assertEqual([], section.notes)
        self.assertEqual(1, len(section.links))

        link = section.links[0]
        self.assertEqual('book', link.type)
        self.assertEqual('Example Book', link.title)
        self.assertEqual('https://example.book', link.link)
        self.assertIsNone(link.date)
        self.assertTrue(link.checked)

    def test_multiple_links(self):
        source = dedent('''
        .page links My Links

        .section links New Links
        
        .link book Example Book 1
        .url https://example1.book
        
        .link book Example Book 2
        .url https://example2.book
        .checked
        
        .link book Example Book 3
        .url https://example3.book
        .date 2001
        ''')
        parser = Parser(source)
        result = parser.parse()
        self.assertIsInstance(result, LinksPage)
        self.assertEqual(1, len(result.sections))

        section = result.sections[0]
        self.assertEqual('New Links', section.title)
        self.assertEqual([], section.notes)
        self.assertEqual(3, len(section.links))

        link = section.links[0]
        self.assertEqual('book', link.type)
        self.assertEqual('Example Book 1', link.title)
        self.assertEqual('https://example1.book', link.link)
        self.assertIsNone(link.date)
        self.assertFalse(link.checked)

        link = section.links[1]
        self.assertEqual('book', link.type)
        self.assertEqual('Example Book 2', link.title)
        self.assertEqual('https://example2.book', link.link)
        self.assertIsNone(link.date)
        self.assertTrue(link.checked)

        link = section.links[2]
        self.assertEqual('book', link.type)
        self.assertEqual('Example Book 3', link.title)
        self.assertEqual('https://example3.book', link.link)
        self.assertEqual('2001', link.date)
        self.assertFalse(link.checked)


if __name__ == '__main__':
    unittest.main()
