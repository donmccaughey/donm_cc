from resources import Directory
from website.pages.aughey import aughey
from website.pages.bash import bash
from website.pages.business_novels import business_novels
from website.pages.engineering_management import engineering_management
from website.pages.hashtables import hashtables
from website.pages.home import home
from website.pages.macos_packages import macos_packages
from website.pages.make import make
from website.pages.memory_match import memory_match
from website.pages.random_words import random_words
from website.pages.rust_and_wasm import rust_and_wasm
from website.pages.science_fiction import science_fiction


root = home()
with root:
    Directory('banners')
    Directory('icons')
    Directory('resume')

    aughey()
    business_novels()
    bash()
    engineering_management()
    hashtables()
    macos_packages()
    make()
    memory_match()
    random_words()
    rust_and_wasm()
    science_fiction()
