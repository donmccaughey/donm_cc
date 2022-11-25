import unittest
from textwrap import dedent

from file_formats.page_file import PageFile
from file_formats.page_file.parser import Parser, \
    MissingDirectiveError, MissingModifierError, MissingDataError, \
    UnexpectedTokenError, MissingDirectivesError, InvalidModifierError, PAGE_MODIFIERS


class ParserTestCase(unittest.TestCase):

    def test_empty_file(self):
        source = ''
        result = Parser(source).parse()
        self.assertIsInstance(result, MissingDirectiveError)
        self.assertEqual('page', result.directive)

    def test_page_directive_missing_modifier(self):
        source = '.page'
        result = Parser(source).parse()
        self.assertIsInstance(result, InvalidModifierError)
        self.assertEqual(PAGE_MODIFIERS, result.modifiers)

    def test_page_directive_missing_title(self):
        source = '.page links'
        result = Parser(source).parse()
        self.assertIsInstance(result, MissingDataError)
        self.assertEqual('page title', result.data_description)

    def test_page_directive_only(self):
        source = '.page links My Links'
        result = Parser(source).parse()
        self.assertIsInstance(result, PageFile)
        self.assertEqual('links', result.modifier)
        self.assertEqual('My Links', result.title)
        self.assertIsNone(result.subtitle)
        self.assertEqual([], result.notes)
        self.assertEqual([], result.sections)

    def test_page_directive_author(self):
        source = '.page author William Shakespeare'
        result = Parser(source).parse()
        self.assertIsInstance(result, PageFile)
        self.assertEqual('author', result.modifier)
        self.assertEqual('William Shakespeare', result.title)
        self.assertIsNone(result.subtitle)
        self.assertEqual([], result.notes)
        self.assertEqual([], result.sections)

    def test_page_directive_invalid_modifier(self):
        source = '.page invalid My Links'
        result = Parser(source).parse()
        self.assertIsInstance(result, InvalidModifierError)
        self.assertEqual(PAGE_MODIFIERS, result.modifiers)

    def test_page_directive_invalid_data(self):
        source = dedent('''
        .page links 
        
        This is a paragraph.
        ''')
        result = Parser(source).parse()
        self.assertIsInstance(result, MissingDataError)
        self.assertEqual('page title', result.data_description)

    def test_page_directive_with_subtitle(self):
        source = dedent('''
        .page links My Links 
        .subtitle The Movie
        ''')
        result = Parser(source).parse()
        self.assertIsInstance(result, PageFile)
        self.assertEqual('My Links', result.title)
        self.assertEqual('The Movie', result.subtitle)
        self.assertEqual([], result.notes)
        self.assertEqual([], result.sections)

    def test_page_directive_with_one_paragraph(self):
        source = dedent('''
        .page links My Links
        
        This is a paragraph.
        ''')
        result = Parser(source).parse()
        self.assertIsInstance(result, PageFile)
        self.assertEqual('My Links', result.title)
        self.assertIsNone(result.subtitle)
        self.assertEqual(['This is a paragraph.'], result.notes)
        self.assertEqual([], result.sections)

    def test_page_directive_with_paragraphs(self):
        source = dedent('''
        .page links My Links
        This is the first paragraph.
        
        This is the second paragraph.
        
        This is the third paragraph.
        ''')
        result = Parser(source).parse()
        self.assertIsInstance(result, PageFile)
        self.assertEqual('My Links', result.title)
        self.assertIsNone(result.subtitle)
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
        result = Parser(source).parse()
        self.assertIsInstance(result, UnexpectedTokenError)

    def test_section_directive_missing_modifier(self):
        source = dedent('''
        .page links My Links
        
        .section
        ''')
        result = Parser(source).parse()
        self.assertIsInstance(result, MissingModifierError)
        self.assertEqual('links', result.modifier)

    def test_section_directive_missing_title(self):
        source = dedent('''
        .page links My Links
        
        .section links
        ''')
        result = Parser(source).parse()
        self.assertIsInstance(result, MissingDataError)
        self.assertEqual('section title', result.data_description)

    def test_empty_section(self):
        source = dedent('''
        .page links My Links
        
        .section links New Links
        
        ''')
        result = Parser(source).parse()
        self.assertIsInstance(result, PageFile)
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
        result = Parser(source).parse()
        self.assertIsInstance(result, PageFile)
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
        result = Parser(source).parse()
        self.assertIsInstance(result, PageFile)
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
        result = Parser(source).parse()
        self.assertIsInstance(result, PageFile)
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
        result = Parser(source).parse()
        self.assertIsInstance(result, InvalidModifierError)

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
        result = Parser(source).parse()
        self.assertIsInstance(result, MissingDirectivesError)
        self.assertEqual(['url', 'asin'], result.directives)

    def test_general_link_missing_url(self):
        source = dedent('''
        .page links My Links

        .section links New Links
        
        .link blog Example Blog
        ''')
        result = Parser(source).parse()
        self.assertIsInstance(result, MissingDirectiveError)
        self.assertEqual('url', result.directive)

    def test_link_missing_url_followed_by_link_directive(self):
        source = dedent('''
        .page links My Links

        .section links New Links

        .link book Example Book
        .link
        ''')
        result = Parser(source).parse()
        self.assertIsInstance(result, MissingDirectivesError)
        self.assertEqual(['url', 'asin'], result.directives)

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

    def test_book_link(self):
        source = dedent('''
        .page links My Links

        .section links New Links
        
        .link book Example Book
        .url https://example.book
        ''')
        result = Parser(source).parse()
        self.assertIsInstance(result, PageFile)
        self.assertEqual(1, len(result.sections))

        section = result.sections[0]
        self.assertEqual('New Links', section.title)
        self.assertEqual([], section.notes)
        self.assertEqual(1, len(section.links))

        link = section.links[0]
        self.assertEqual('book', link.modifier)
        self.assertEqual('Example Book', link.title)
        self.assertEqual('https://example.book', link.url)
        self.assertIsNone(link.asin)
        self.assertIsNone(link.date)
        self.assertFalse(link.checked)

    def test_book_link_with_asin(self):
        source = dedent('''
        .page links My Links

        .section links New Links
        
        .link book Example Book
        .asin B123456789
        ''')
        result = Parser(source).parse()
        self.assertIsInstance(result, PageFile)
        self.assertEqual(1, len(result.sections))

        section = result.sections[0]
        self.assertEqual('New Links', section.title)
        self.assertEqual([], section.notes)
        self.assertEqual(1, len(section.links))

        link = section.links[0]
        self.assertEqual('book', link.modifier)
        self.assertEqual('Example Book', link.title)
        self.assertIsNone(link.url)
        self.assertEqual('B123456789', link.asin)
        self.assertIsNone(link.date)
        self.assertFalse(link.checked)

    def test_book_link_with_url_and_asin(self):
        source = dedent('''
        .page links My Links

        .section links New Links
        
        .link book Example Book
        .url https://example.book
        .asin B123456789
        ''')
        result = Parser(source).parse()
        self.assertIsInstance(result, PageFile)
        self.assertEqual(1, len(result.sections))

        section = result.sections[0]
        self.assertEqual('New Links', section.title)
        self.assertEqual([], section.notes)
        self.assertEqual(1, len(section.links))

        link = section.links[0]
        self.assertEqual('book', link.modifier)
        self.assertEqual('Example Book', link.title)
        self.assertEqual('https://example.book', link.url)
        self.assertEqual('B123456789', link.asin)
        self.assertIsNone(link.date)
        self.assertFalse(link.checked)

    def test_book_link_with_asin_and_url(self):
        source = dedent('''
        .page links My Links

        .section links New Links
        
        .link book Example Book
        .asin B123456789
        .url https://example.book
        ''')
        result = Parser(source).parse()
        self.assertIsInstance(result, PageFile)
        self.assertEqual(1, len(result.sections))

        section = result.sections[0]
        self.assertEqual('New Links', section.title)
        self.assertEqual([], section.notes)
        self.assertEqual(1, len(section.links))

        link = section.links[0]
        self.assertEqual('book', link.modifier)
        self.assertEqual('Example Book', link.title)
        self.assertEqual('https://example.book', link.url)
        self.assertEqual('B123456789', link.asin)
        self.assertIsNone(link.date)
        self.assertFalse(link.checked)

    def test_repo_link(self):
        source = dedent('''
        .page links My Links

        .section links New Links
        
        .link repo Example Repo
        .url https://example.repo
        ''')
        result = Parser(source).parse()
        self.assertIsInstance(result, PageFile)
        self.assertEqual(1, len(result.sections))

        section = result.sections[0]
        self.assertEqual('New Links', section.title)
        self.assertEqual([], section.notes)
        self.assertEqual(1, len(section.links))

        link = section.links[0]
        self.assertEqual('repo', link.modifier)
        self.assertEqual('Example Repo', link.title)
        self.assertEqual('https://example.repo', link.url)
        self.assertIsNone(link.date)
        self.assertFalse(link.checked)

    def test_paper_link(self):
        source = dedent('''
        .page links My Links

        .section links New Links
        
        .link paper Example Paper
        .url https://example.paper
        ''')
        result = Parser(source).parse()
        self.assertIsInstance(result, PageFile)
        self.assertEqual(1, len(result.sections))

        section = result.sections[0]
        self.assertEqual('New Links', section.title)
        self.assertEqual([], section.notes)
        self.assertEqual(1, len(section.links))

        link = section.links[0]
        self.assertEqual('paper', link.modifier)
        self.assertEqual('Example Paper', link.title)
        self.assertEqual('https://example.paper', link.url)
        self.assertIsNone(link.date)
        self.assertFalse(link.checked)

    def test_link_with_author_missing_value(self):
        source = dedent('''
        .page links My Links

        .section links New Links

        .link book Example Book
        .url https://example.book
        .author
        ''')
        result = Parser(source).parse()
        self.assertIsInstance(result, MissingDataError)
        self.assertEqual('author value', result.data_description)

    def test_link_with_one_author(self):
        source = dedent('''
        .page links My Links

        .section links New Links

        .link book Example Book
        .url https://example.book
        .author Alice Author
        ''')
        result = Parser(source).parse()
        self.assertIsInstance(result, PageFile)
        self.assertEqual(1, len(result.sections))

        section = result.sections[0]
        self.assertEqual('New Links', section.title)
        self.assertEqual([], section.notes)
        self.assertEqual(1, len(section.links))

        link = section.links[0]
        self.assertEqual('book', link.modifier)
        self.assertEqual('Example Book', link.title)
        self.assertEqual('https://example.book', link.url)
        self.assertIsNone(link.asin)
        self.assertEqual(['Alice Author'], link.authors)
        self.assertIsNone(link.date)
        self.assertFalse(link.checked)

    def test_link_with_two_author(self):
        source = dedent('''
        .page links My Links

        .section links New Links

        .link book Example Book
        .url https://example.book
        .author Alice Author
        .author Bob Booker
        ''')
        result = Parser(source).parse()
        self.assertIsInstance(result, PageFile)
        self.assertEqual(1, len(result.sections))

        section = result.sections[0]
        self.assertEqual('New Links', section.title)
        self.assertEqual([], section.notes)
        self.assertEqual(1, len(section.links))

        link = section.links[0]
        self.assertEqual('book', link.modifier)
        self.assertEqual('Example Book', link.title)
        self.assertEqual('https://example.book', link.url)
        self.assertIsNone(link.asin)
        self.assertEqual(['Alice Author', 'Bob Booker'], link.authors)
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
        result = Parser(source).parse()
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
        result = Parser(source).parse()
        self.assertIsInstance(result, PageFile)
        self.assertEqual(1, len(result.sections))

        section = result.sections[0]
        self.assertEqual('New Links', section.title)
        self.assertEqual([], section.notes)
        self.assertEqual(1, len(section.links))

        link = section.links[0]
        self.assertEqual('book', link.modifier)
        self.assertEqual('Example Book', link.title)
        self.assertEqual('https://example.book', link.url)
        self.assertIsNone(link.asin)
        self.assertEqual('2012', link.date)
        self.assertFalse(link.checked)

    def test_link_with_date_twice(self):
        source = dedent('''
        .page links My Links

        .section links New Links
        
        .link book Example Book
        .url https://example.book
        .date 2012
        .date 2011
        ''')
        result = Parser(source).parse()
        self.assertIsInstance(result, PageFile)
        self.assertEqual(1, len(result.sections))

        section = result.sections[0]
        self.assertEqual('New Links', section.title)
        self.assertEqual([], section.notes)
        self.assertEqual(1, len(section.links))

        link = section.links[0]
        self.assertEqual('book', link.modifier)
        self.assertEqual('Example Book', link.title)
        self.assertEqual('https://example.book', link.url)
        self.assertIsNone(link.asin)
        self.assertEqual('2011', link.date)
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
        result = Parser(source).parse()
        self.assertIsInstance(result, PageFile)
        self.assertEqual(1, len(result.sections))

        section = result.sections[0]
        self.assertEqual('New Links', section.title)
        self.assertEqual([], section.notes)
        self.assertEqual(1, len(section.links))

        link = section.links[0]
        self.assertEqual('book', link.modifier)
        self.assertEqual('Example Book', link.title)
        self.assertEqual('https://example.book', link.url)
        self.assertIsNone(link.asin)
        self.assertEqual('2012', link.date)
        self.assertTrue(link.checked)

    def test_link_with_checked_and_date(self):
        source = dedent('''
        .page links My Links

        .section links New Links
        
        .link book Example Book
        .url https://example.book
        .checked
        .date 2012
        ''')
        result = Parser(source).parse()
        self.assertIsInstance(result, PageFile)
        self.assertEqual(1, len(result.sections))

        section = result.sections[0]
        self.assertEqual('New Links', section.title)
        self.assertEqual([], section.notes)
        self.assertEqual(1, len(section.links))

        link = section.links[0]
        self.assertEqual('book', link.modifier)
        self.assertEqual('Example Book', link.title)
        self.assertEqual('https://example.book', link.url)
        self.assertIsNone(link.asin)
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
        result = Parser(source).parse()
        self.assertIsInstance(result, PageFile)
        self.assertEqual(1, len(result.sections))

        section = result.sections[0]
        self.assertEqual('New Links', section.title)
        self.assertEqual([], section.notes)
        self.assertEqual(1, len(section.links))

        link = section.links[0]
        self.assertEqual('book', link.modifier)
        self.assertEqual('Example Book', link.title)
        self.assertEqual('https://example.book', link.url)
        self.assertIsNone(link.asin)
        self.assertIsNone(link.date)
        self.assertTrue(link.checked)

    def test_link_with_checked_twice(self):
        source = dedent('''
        .page links My Links

        .section links New Links
        
        .link book Example Book
        .url https://example.book
        .checked
        .checked
        ''')
        result = Parser(source).parse()
        self.assertIsInstance(result, PageFile)
        self.assertEqual(1, len(result.sections))

        section = result.sections[0]
        self.assertEqual('New Links', section.title)
        self.assertEqual([], section.notes)
        self.assertEqual(1, len(section.links))

        link = section.links[0]
        self.assertEqual('book', link.modifier)
        self.assertEqual('Example Book', link.title)
        self.assertEqual('https://example.book', link.url)
        self.assertIsNone(link.asin)
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
        result = Parser(source).parse()
        self.assertIsInstance(result, PageFile)
        self.assertEqual(1, len(result.sections))

        section = result.sections[0]
        self.assertEqual('New Links', section.title)
        self.assertEqual([], section.notes)
        self.assertEqual(3, len(section.links))

        link = section.links[0]
        self.assertEqual('book', link.modifier)
        self.assertEqual('Example Book 1', link.title)
        self.assertEqual('https://example1.book', link.url)
        self.assertIsNone(link.asin)
        self.assertIsNone(link.date)
        self.assertFalse(link.checked)

        link = section.links[1]
        self.assertEqual('book', link.modifier)
        self.assertEqual('Example Book 2', link.title)
        self.assertEqual('https://example2.book', link.url)
        self.assertIsNone(link.date)
        self.assertTrue(link.checked)

        link = section.links[2]
        self.assertEqual('book', link.modifier)
        self.assertEqual('Example Book 3', link.title)
        self.assertEqual('https://example3.book', link.url)
        self.assertEqual('2001', link.date)
        self.assertFalse(link.checked)


if __name__ == '__main__':
    unittest.main()
