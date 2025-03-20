from markup import FigCaption, Figure, Img, Ul
from resources import Page
from website.collection import item
from website.figures import banner


def home_page():
    with Page('Don McCaughey', name='index'):
        banner(
            image='/banners/Thorton_State_Beach_summer_2016.jpg',
            width=1024, height=341,
            description='A dog running on the beach chasing sea birds',
            caption='Thorton State Beach, summer 2016',
            position='upper'
        )
        with Ul(class_names=['collection']):
            item('Sourcehut', 'https://git.sr.ht/~donmcc', 'donmcc')
            item('GitHub', 'https://github.com/donmccaughey', 'donmccaughey')
            item('News', 'https://news.donm.cc/', 'Unsocial media')
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
