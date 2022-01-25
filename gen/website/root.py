from resources import Directory
from website.pages.aughey import aughey
from website.pages.bash import bash
from website.pages.hashtables import hashtables
from website.pages.home_page import home_page
from website.pages.macos_packages import macos_packages
from website.pages.memory_match import memory_match
from website.pages.random_words import random_words
from website.pages.rust_and_wasm import rust_and_wasm
from website.pages.science_fiction import science_fiction


root = Directory(name='', is_root=True)
with root:
    home_page()

    Directory('banners')
    Directory('business_novels')
    Directory('engineering_management')
    Directory('icons')
    Directory('make')
    Directory('resume')

    aughey()
    bash()
    hashtables()
    macos_packages()
    memory_match()
    random_words()
    rust_and_wasm()
    science_fiction()
