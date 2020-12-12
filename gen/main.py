from typing import Optional

from site import Directory, File, IndexPage, Page
from tags import A, Br, Div, Em, Img, Span, Strong


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

    IndexPage('Don McCaughey', name='aughey', has_files=True)
    IndexPage('Business Novels')
    IndexPage('Engineering Management')
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
    root.generate('../tmp', is_dry_run=False)
