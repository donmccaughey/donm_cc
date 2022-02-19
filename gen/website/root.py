from resources import Directory, Sitemap
from website.pages.aughey import aughey
from website.pages.home_page import home_page
from website.pages.macos_packages import macos_packages
from website.pages.memory_match import memory_match
from website.pages.random_words import random_words
from website.pages.science_fiction import science_fiction


root = Directory(name='', is_root=True)
with root:
    Sitemap('https://donm.cc')

    home_page()

    Directory('banners')
    Directory('business_novels')
    Directory('engineering_management')
    Directory('hashtables')
    Directory('make')
    Directory('resume')
    Directory('shell')

    aughey()
    macos_packages()
    memory_match()
    random_words()
    science_fiction()
