from markup import Section, H1, P, Ul
from resources import Directory, Page
from website.collection import item


def science_fiction():
    with Directory('science_fiction'):
        with Page('Science Fiction', name='index'):
            with Section(class_names=['overview']):
                H1('Science Fiction')
                P("""
                    Science fiction has been a staple of my reading diet since I was
                    very young.  I gravitate towards space opera; multi-book,
                    galaxy-spanning sagas are my bread and butter.
                """)
            with Ul(class_names=['collection']):
                item('Iain M Banks', '/science_fiction/iain_m_banks.html')
                item('Lois McMaster Bujold',
                     '/science_fiction/lois_mcmaster_bujold.html')
                item('James SA Corey', '/science_fiction/james_sa_corey.html')
                item('Andrew Moriarty', '/science_fiction/andrew_moriarty.html')
                item('Alastair Reynolds', '/science_fiction/alastair_reynolds.html')
                item('Neal Stephenson', '/science_fiction/neal_stephenson.html')
                item('David Weber', '/science_fiction/david_weber.html')
                item('Walter Jon Williams', '/science_fiction/walter_jon_williams.html')
