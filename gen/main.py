from typing import Optional

from site import Directory, File, IndexPage, Page
from tags import A, Br, Div, Em, H1, Img, P, Section, Span, Strong, Text, Time


def item(
        title: str,
        subtitle: str,
        href: str,
        favicon: Optional[str] = None,
        is_local: bool = False
):
    class_names = ['item'] + (['local'] if is_local else [])
    with A(class_names=class_names, href=href):
        if favicon:
            Img(class_names=['favicon'], src=favicon, alt=f'{title} icon')
        Strong(title)
        Br()
        Em(subtitle)


def link(
        type: str,
        title: str,
        href: str,
        author: Optional[str] = None,
        date: Optional[str] = None,
        checked: bool = False
):
    with A(class_names=[type], href=href):
        Text(title)
        if author:
            Span(class_names=['authors'], text=author)
        if date:
            Time(datetime=date)
        if checked:
            Text('✓')


def book(
        title: str,
        href: str,
        author: Optional[str] = None,
        date: Optional[str] = None,
        checked: bool = False
):
    link(
        type='book',
        title=title,
        href=href,
        author=author,
        date=date,
        checked=checked,
    )


root = IndexPage('Don McCaughey', is_root=True)
with root:
    with Div(class_names=['banner']):
        Img(
            src='/banners/Don_and_Molly_Round_Hill_Lake_Tahoe_summer_2019.jpg',
            alt='Don and Molly atop Round Hill'
        )
        Span(
            text='Round Hill, Lake Tahoe, summer 2019',
            class_names=['lower-caption']
        )
    with Div(class_names=['collection']):
        item('Sourcehut', 'donmcc', 'https://git.sr.ht/~donmcc')
        item('GitHub', 'donmccaughey', 'https://github.com/donmccaughey', favicon='/icons/github.png')
        item('Twitter', '@donmccaughey', 'https://twitter.com/donmccaughey', favicon='/icons/twitter.png')
        item('LinkedIn', 'donmccaughey', 'https://www.linkedin.com/in/donmccaughey', favicon='/icons/linkedin.png')
        item('Résumé', "Stuff I've done", '/resume/Resume_of_Don_McCaughey.pdf', is_local=True)
        item('Truework', 'My current gig', 'https://www.truework.com', favicon='/icons/truework.png')
        item('Copper', 'My previous gig', 'https://www.copper.com', favicon='/icons/copper.png')
        item('Memory Match', 'A tile matching game', '/memory_match/', is_local=True)
        item('macOS Packages', 'Software installers', '/macos_packages/', favicon='/macos_packages/package-32x32.png', is_local=True)
        item('Engineering Management', 'Software is a team sport', '/engineering_management/', is_local=True)
        item('Rust and Wasm', 'Assembling the web', '/rust_and_wasm/', is_local=True)
        item('Make', 'The build tool', '/make/', is_local=True)
        item('Hashtables', 'Keys and values', '/hashtables/', is_local=True)
        item('Science Fiction', 'Reading for fun', '/science_fiction/', is_local=True)
        item('Random Words', 'A handy word picker', '/random_words/', is_local=True)

    File('base.css')
    Directory('banners')
    Directory('icons')
    Directory('resume')

    with IndexPage('Don McCaughey', name='aughey', has_files=True):
        with Div(class_names=['banner']):
            Img(src='/aughey/handstand.jpg', alt='Don doing a handstand')
            Span(class_names=['caption'], text='Coachella Festival, spring 2007')
    with IndexPage('Business Novels'):
        with Section(class_names=['overview']):
            H1('Business Novels')
            P()
        with Section(class_names=['links']):
            H1('Recommended')
            book('The Goal', '', checked=True)
            book('The Phoenix Project', '', checked=True)
            book('The Unicorn Project', '', checked=True)
            book('The Ideal Team Player', '', checked=True)
            book('The Five Dysfunctions of a Team', '', checked=True)
            book('The Four Obsessions of an Extraordinary Executive', '', checked=True)
        with Section(class_names=['links']):
            book('The Five Temptations of a CEO', '', checked=True)
            book('Critical Chain', '', checked=True)
            book('The Deadline: A Novel About Project Management', '')
            book('How To Destroy A Tech Startup In Three Easy Steps', '', checked=True)
        with Section(class_names=['links']):
            H1('Business Comics')
            book('The Adventures of Johnny Bunko', '', checked=True)
            book("What Got You Here Won't Get You There", '', checked=True)

    with IndexPage('Engineering Management'):
        with Section(class_names=['overview']):
            H1('Engineering Management')
            P("""
                In 2017 I became an engineering manager, a career change I wasn't
                looking for and hadn't previously considered.  My experience as
                consultant, tech lead and member of Extreme Programming teams
                helped in the transition, but there is still a lot to learn in my
                new role.
            """)
            P("""
                Management is a skill quite different from software engineering,
                and I still consider myself a beginner.  This page includes some
                of the things I've found useful.
            """)

    IndexPage('Hash Tables', name='hashtables')
    IndexPage('macOS Packages', has_files=True)
    IndexPage('Make')
    IndexPage('Memory Match', has_files=True)
    IndexPage('Random Words', has_files=True)
    IndexPage('Rust and Wasm')
    with IndexPage('Science Fiction'):
        Page('Alastair Reynolds')
        Page('Iain M Banks')
        Page('James SA Corey')
        Page('Lois McMaster Bujold')

if __name__ == '__main__':
    root.find_files('../wwwroot')
    root.generate('../tmp', is_dry_run=False, overwrite=True)
