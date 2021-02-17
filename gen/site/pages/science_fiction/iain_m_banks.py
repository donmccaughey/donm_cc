from markup import Section, H1, P, Ul
from resources import Page
from site.links import book


def iain_m_banks():
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