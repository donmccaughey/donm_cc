from site import Directory, File, IndexPage, Page
from tags import Div, Img, Span


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

    File('base.css')
    Directory('banners')
    Directory('icons')
    Directory('resume')

    IndexPage('Don McCaughey', name='aughey', has_files=True)
    IndexPage('Business Novels')
    IndexPage('Engineering Management')
    IndexPage('Hash Tables')
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
