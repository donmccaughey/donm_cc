import sys
from gen import Directory, File, IndexPage, Page


root = IndexPage('Don McCaughey', name="", parent=None)

aughey = IndexPage('Don McCaughey', parent=root, name='aughey')

banners = Directory('banners', parent=root)

base_css = File('base.css', parent=root)

business_novels = IndexPage('Business Novels', parent=root)

engineering_management = IndexPage('Engineering Management', parent=root)

hash_tables = IndexPage('Hash Tables', parent=root)

icons = Directory('icons', parent=root)

macos_packages = IndexPage('macOS Packages', parent=root, has_files=True)

make = IndexPage('Make', parent=root)

memory_match = IndexPage('Memory Match', parent=root, has_files=True)

random_words = IndexPage('Random Words', parent=root, has_files=True)

resume = Directory('resume', parent=root)

rust_and_wasm = IndexPage('Rust and Wasm', parent=root)

science_fiction = IndexPage('Science Fiction', parent=root)
alastair_reynolds = Page('Alastair Reynolds', parent=science_fiction)
iain_m_banks = Page('Iain M Banks', parent=science_fiction)
james_sa_corey = Page('James SA Corey', parent=science_fiction)
lois_mcmaster_bujold = Page('Lois McMaster Bujold', parent=science_fiction)


def main():
    root.find_files('../wwwroot')
    root.write_tree_description(sys.stdout)


if __name__ == '__main__':
    main()
