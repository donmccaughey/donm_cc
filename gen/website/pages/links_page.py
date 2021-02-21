from file_formats.links_page import LinksPage
from markup import Section, H1, P, Ul
from resources import Page
from website.links import link as build_link


def build_links_page(links_page: LinksPage):
    with Page(links_page.title):
        with Section(class_names=['overview']):
            H1(links_page.title)
            for note in links_page.notes:
                P(note)
        for section in links_page.sections:
            with Section(class_names=['links']):
                H1(section.title)
                for note in section.notes:
                    P(note)
                with Ul():
                    for link in section.links:
                        build_link(
                            type=link.type,
                            title=link.title,
                            href=link.link,
                            authors=None,
                            date=link.date,
                            checked=link.checked,
                        )
