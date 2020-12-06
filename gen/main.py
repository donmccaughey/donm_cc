import sys
from gen import Directory, File, IndexPage, Page


root = IndexPage('Don McCaughey', name="")
with root:
    IndexPage('Don McCaughey', name='aughey')
    Directory('banners')
    File('base.css')
    IndexPage('Business Novels')
    IndexPage('Engineering Management')
    IndexPage('Hash Tables')
    Directory('icons')
    IndexPage('macOS Packages', has_files=True)
    IndexPage('Make')
    IndexPage('Memory Match', has_files=True)
    IndexPage('Random Words', has_files=True)
    Directory('resume')
    IndexPage('Rust and Wasm')
    with IndexPage('Science Fiction'):
        alastair_reynolds = Page('Alastair Reynolds')
        iain_m_banks = Page('Iain M Banks')
        james_sa_corey = Page('James SA Corey')
        lois_mcmaster_bujold = Page('Lois McMaster Bujold')


def main():
    root.find_files('../wwwroot')
    root.write_tree_description(sys.stdout)


if __name__ == '__main__':
    main()
