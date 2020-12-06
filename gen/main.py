from gen import Directory, File, IndexPage, Page


root = IndexPage('Don McCaughey', is_root=True)
with root:
    File('base.css')
    Directory('banners')
    Directory('icons')
    Directory('resume')

    IndexPage('Don McCaughey', name='aughey')
    IndexPage('Business Novels')
    IndexPage('Engineering Management')
    IndexPage('Hash Tables')
    IndexPage('macOS Packages', has_files=True)
    IndexPage('Make')
    IndexPage('Memory Match', has_files=True)
    IndexPage('Random Words', has_files=True)
    IndexPage('Rust and Wasm')
    with IndexPage('Science Fiction'):
        alastair_reynolds = Page('Alastair Reynolds')
        iain_m_banks = Page('Iain M Banks')
        james_sa_corey = Page('James SA Corey')
        lois_mcmaster_bujold = Page('Lois McMaster Bujold')


if __name__ == '__main__':
    root.find_files('../wwwroot')
    root.generate('../tmp', is_dry_run=False)
