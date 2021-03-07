from markup import Section, H1, P, Ul
from resources import IndexPage
from website.collection import item
from website.pages.science_fiction.james_sa_corey import james_sa_corey
from website.pages.science_fiction.lois_mcmaster_bujold import lois_mcmaster_bujold


def science_fiction():
    with IndexPage('Science Fiction', has_files=True):
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
            item('Alastair Reynolds', '/science_fiction/alastair_reynolds.html')

        james_sa_corey()
        lois_mcmaster_bujold()
