from markup import Section, H1, Em, Ul
from resources import Page
from site.links import book


def james_sa_corey():
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