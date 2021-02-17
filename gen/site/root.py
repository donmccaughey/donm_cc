from resources import File, Directory
from site.pages.aughey import aughey
from site.pages.bash import bash
from site.pages.business_novels import business_novels
from site.pages.engineering_management import engineering_management
from site.pages.hashtables import hashtables
from site.pages.home import home
from site.pages.macos_packages import macos_packages
from site.pages.make import make
from site.pages.memory_match import memory_match
from site.pages.random_words import random_words
from site.pages.rust_and_wasm import rust_and_wasm
from site.pages.science_fiction import science_fiction


root = home()
with root:
    File('base.css')
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
