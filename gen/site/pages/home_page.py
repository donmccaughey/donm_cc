from markup import Div, Img, Br, Span, Ul
from site.collection import item


def home_page():
    with Div(class_names=['banner']):
        Img(
            src='/banners/Don_and_Molly_Round_Hill_Lake_Tahoe_summer_2019.jpg',
            alt='Don and Molly atop Round Hill'
        )
        Br()
        Span(
            text='Round Hill, Lake Tahoe, summer 2019',
            class_names=['lower-caption']
        )
    with Ul(class_names=['collection']):
        item('Sourcehut', 'https://git.sr.ht/~donmcc', 'donmcc', external=True)
        item('GitHub', 'https://github.com/donmccaughey', 'donmccaughey',
             favicon='/icons/github.png', external=True)
        item('Twitter', 'https://twitter.com/donmccaughey', '@donmccaughey',
             favicon='/icons/twitter.png', external=True)
        item('LinkedIn', 'https://www.linkedin.com/in/donmccaughey',
             'donmccaughey', favicon='/icons/linkedin.png', external=True)
        item('Truework', 'https://www.truework.com', 'My current gig',
             favicon='/icons/truework.png', external=True)
        item('Copper', 'https://www.copper.com', 'My previous gig',
             favicon='/icons/copper.png', external=True)
        item('Résumé', '/resume/Resume_of_Don_McCaughey.pdf', "Stuff I've done")
        item('Memory Match', '/memory_match/', 'A tile matching game')
        item('Random Words', '/random_words/', 'A handy word picker')
        item('macOS Packages', '/macos_packages/', 'Software installers',
             favicon='/macos_packages/package-32x32.png')
        item('Engineering Management', '/engineering_management/',
             'Software is a team sport')
        item('Make', '/make/', 'The build tool')
        item('Hashtables', '/hashtables/', 'Keys and values')
        item('Science Fiction', '/science_fiction/', 'Reading for fun')
