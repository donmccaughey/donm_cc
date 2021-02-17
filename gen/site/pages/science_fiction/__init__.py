from markup import Section, H1, P, Ul, Em
from resources import IndexPage, Page
from site.collection import item
from site.links import book
from site.pages.science_fiction.alastair_reynolds import alastair_reynolds


def science_fiction():
    with IndexPage('Science Fiction'):
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

        alastair_reynolds()

        with Page('Iain M Banks'):
            with Section(class_names=['overview']):
                H1('Iain M Banks')
                P("""
                    Banks passed away in 2013, and I've been carefully parceling out the
                    remaining Culture novels since.  I was hooked early into <i>Consider
                    Phlebas</i>, though <i>The Player of Games</i> and <i>Use of
                    Weapons</i> are probably better and more accessible starting places.
                    For me, <i>Look to Windward</i> best captures the heart and soul of
                    the Culture.
                 """)
            with Section(class_names=['links']):
                H1('The Culture Novels')
                with Ul():
                    book('Consider Phlebas',
                         'https://www.amazon.com/gp/product/B0013TX6FI',
                         date='1987', checked=True)
                    book('The Player of Games',
                         'https://www.amazon.com/gp/product/B002WM3HC2',
                         date='1988', checked=True)
                    book('Use of Weapons',
                         'https://www.amazon.com/gp/product/B0015DWLTE',
                         date='1990', checked=True)
                    book('The State of the Art (collection)',
                         'https://www.goodreads.com/book/show/129131.The_State_of_the_Art',
                         date='1991', checked=True)
                    book('Excession',
                         'https://www.amazon.com/Excession-Iain-M-Banks/dp/0553575376',
                         date='1996', checked=True)
                    book('Inversions',
                         'https://www.amazon.com/Inversions-Iain-M-Banks/dp/074341196X',
                         date='1998', checked=True)
                    book('Look to Windward',
                         'https://www.amazon.com/gp/product/B001D20270',
                         date='2000', checked=True)
                    book('Matter',
                         'https://www.amazon.com/gp/product/B000VMHI98',
                         date='2008', checked=True)
                    book('Surface Detail',
                         'https://www.amazon.com/gp/product/B0046A9NLC',
                         date='2010', checked=True)
                    book('The Hydrogen Sonata',
                         'https://www.amazon.com/gp/product/B0081BU42O',
                         date='2012', checked=True)
            with Section(class_names=['links']):
                H1('Other Novels')
                with Ul():
                    book('Against a Dark Background',
                         'https://www.amazon.com/gp/product/B002CT0TXK',
                         date='1993')
                    book('Feersum Endjinn',
                         'https://www.amazon.com/Feersum-Endjinn-Novel-Iain-Banks/dp/0553374591',
                         date='1994')
                    book('The Algebraist',
                         'https://www.amazon.com/Algebraist-Iain-M-Banks/dp/1597800449',
                         date='2004')
                    book('Transition',
                         'https://www.amazon.com/gp/product/B002O0Q6YS',
                         date='2009')

        with Page('James SA Corey'):
            with Section(class_names=['overview']):
                H1('James SA Corey')
            with Section(class_names=['links']):
                H1('The Expanse')
                Em('(publication order)')
                with Ul():
                    book('Leviathan Wakes',
                         'https://www.amazon.com/gp/product/B0047Y171G',
                         date='2011', checked=True)
                    book('The Butcher of Anderson Station (novella)',
                         'https://www.amazon.com/gp/product/B0052AHUYM',
                         date='2011', checked=True)
                    book("Caliban's War",
                         'https://www.amazon.com/gp/product/B005SCRR1A',
                         date='2012', checked=True)
                    book('Gods of Risk (novella)',
                         'https://www.amazon.com/gp/product/B008CJ241O',
                         date='2012', checked=True)
                    book('Drive (short story)',
                         'https://www.syfy.com/theexpanse/drive/', date='2012')
                    book("Abaddon's Gate",
                         'https://www.amazon.com/gp/product/B00A2DZMYE',
                         date='2013', checked=True)
                    book('The Churn (novella)',
                         'https://www.amazon.com/gp/product/B00I82884W',
                         date='2014', checked=True)
                    book('Cibola Burn',
                         'https://www.amazon.com/gp/product/B00FPQA4F0',
                         date='2014', checked=True)
                    book('Nemesis Games',
                         'https://www.amazon.com/gp/product/B00O7X626W',
                         date='2015', checked=True)
                    book('The Vital Abyss (novella)',
                         'https://www.amazon.com/gp/product/B015NRKNS8',
                         date='2015', checked=True)
                    book("Babylon's Ashes",
                         'https://www.amazon.com/gp/product/B018S2773Y',
                         date='2016', checked=True)
                    book('Strange Dogs (novella)',
                         'https://www.amazon.com/gp/product/B06ZZ1MKW8',
                         date='2017', checked=True)
                    book('Persepolis Rising',
                         'https://www.amazon.com/gp/product/B06XKN9G27',
                         date='2017')
                    book("Tiamat's Wrath",
                         'https://www.amazon.com/gp/product/B07BVNVWL6',
                         date='2019')
                    book('Auberon (novella)',
                         'https://www.amazon.com/gp/product/B07YKR19FN',
                         date='2019')
                    book('The Last Flight of the Cassandra',
                         'https://www.goodreads.com/book/show/49233894-the-last-flight-of-the-cassandra',
                         date='2019')

        with Page('Lois McMaster Bujold'):
            with Section(class_names=['overview']):
                H1('Lois McMaster Bujold')
                P("""
                    The <i>Vorkosigan Saga</i> is a fun, pulpy space opera that draws
                    more on Golden Age science fiction than New Wave or Cyberpunk.
                """)
                P("""
                    The novels <i>Shards of Honor</i> and <i>Barrayar</i> form a
                    two-part romance that is also Miles Vorkosigan's origin story.  Most
                    of the remainder feature Miles' picaresque adventures.
                """)
            with Section(class_names=['links']):
                H1('The Vorkosigan Saga')
                Em('(internal chronological order)')
                with Ul():
                    book("Dreamweaver's Dilemma (short story)",
                         'https://www.amazon.com/Dreamweavers-Dilemma-Lois-McMaster-Bujold/dp/0915368536',
                         date='1995')
                    book('Falling Free',
                         'https://www.amazon.com/gp/product/B005SHX1CE',
                         date='1987', checked=True)
                    book('Shards of Honor',
                         'https://www.amazon.com/gp/product/B005BH9T86',
                         date='1986', checked=True)
                    book('Aftermaths (short story)',
                         'https://www.goodreads.com/book/show/869033.Far_Frontiers_5',
                         date='1986')
                    book('Barrayar',
                         'https://www.amazon.com/gp/product/B005BFIH7M',
                         date='1991', checked=True)
                    book("The Warrior's Apprentice",
                         'https://www.amazon.com/gp/product/B005DNGSUU',
                         date='1986', checked=True)
                    book('Mountains of Mourning (novella)',
                         'https://www.amazon.com/gp/product/B004O4C13W',
                         date='1989', checked=True)
                    book('Weatherman (novella)',
                         'https://www.amazon.com/gp/product/B004U7LWQK',
                         date='1990', checked=True)
                    book('The Vor Game',
                         'https://www.amazon.com/gp/product/B005O2WQ60',
                         date='1990', checked=True)
                    book('Cetaganda',
                         'https://www.amazon.com/gp/product/B007XFJDYO',
                         date='1995', checked=True)
                    book('Ethan of Athos',
                         'https://www.amazon.com/Ethan-Athos-Vorkosigan-McMaster-Bujold-ebook/dp/B0055EFASI',
                         date='1986', checked=True)
                    book('Labyrinth (novella)',
                         'https://www.amazon.com/gp/product/B004YXBDG4',
                         date='1989', checked=True)
                    book('The Borders of Infinity (novella)',
                         'https://www.amazon.com/Borders-Infinity-3-novella-collection-Vorkosigan-ebook/dp/B0062CKP2S',
                         date='1989', checked=True)
                    book('Brothers in Arms',
                         'https://www.amazon.com/gp/product/B005S4FLCK',
                         date='1989', checked=True)
                    book('Mirror Dance',
                         'https://www.amazon.com/gp/product/B005AJQ9U6',
                         date='1994', checked=True)
                    book('Memory',
                         'https://www.amazon.com/gp/product/B005LI3W9W',
                         date='1996', checked=True)
                    book('Komarr',
                         'https://www.amazon.com/gp/product/B005FRGCZA',
                         date='1998', checked=True)
                    book('A Civil Campaign',
                         'https://www.amazon.com/gp/product/B005FSI1IK',
                         date='1999', checked=True)
                    book('Winterfair Gifts',
                         'https://www.amazon.com/gp/product/B004I6CZ28',
                         date='2004', checked=True)
                    book('Diplomatic Immunity',
                         'https://www.amazon.com/gp/product/B005GLJD7E',
                         date='2002', checked=True)
                    book("Captain Vorpatril's Alliance",
                         'https://www.amazon.com/gp/product/B00AP9RQE4',
                         date='2012', checked=True)
                    book('Cryoburn',
                         'https://www.amazon.com/gp/product/B00APACSJG',
                         date='2010', checked=True)
                    book('Gentleman Jole and the Red Queen',
                         'https://www.amazon.com/gp/product/B01A9CDKDC',
                         date='2016', checked=True)
                    book('The Flowers of Vashnoi (novella)',
                         'https://www.amazon.com/Flowers-Vashnoi-Vorkosigan-Saga-ebook/dp/B07D4M7N3L',
                         date='2018', checked=True)
