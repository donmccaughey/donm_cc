from markup import Div, Img, Br, Span, Ul
from resources import Page
from website.collection import item


def home_page():
    with Page('Don McCaughey', name='index'):
        with Div(class_names=['banner']):
            Img(
                src='/banners/Don_and_Molly_San_Francisco_autumn_2021.jpg',
                alt='Don and Molly atop Round Hill'
            )
            Br()
            Span(
                text='San Francisco, autumn 2021',
                class_names=['lower-caption']
            )
        with Ul(class_names=['collection']):
            item('Sourcehut', 'https://git.sr.ht/~donmcc', 'donmcc')
            item('GitHub', 'https://github.com/donmccaughey', 'donmccaughey')
            item('Memory Match', '/memory_match/', 'A tile matching game')
            item('Random Words', '/random_words/', 'A handy word picker')
            item('macOS Packages', '/macos_packages/', 'Software installers')
            item('Engineering Management', '/engineering_management/', 'Software is a team sport')
            item('Hashtables', '/hashtables/', 'Keys and values')
            item('Make', '/make/', 'The build tool')
            item('Objective-C Tuesdays', '/objective-c_tuesdays/', 'Smalltalk meets C')
            item('Shell', '/shell/', 'Unix glue')
            item('Science Fiction', '/science_fiction/', 'Reading for fun')
            item('Business Novels', '/business_novels/', 'Fictionalized learning')
            item('Résumé', '/resume/', "Stuff I've done")
