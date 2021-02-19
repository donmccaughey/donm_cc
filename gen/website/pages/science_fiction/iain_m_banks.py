from markup import Section, H1, P, Ul
from resources import Page
from website.links import book


def iain_m_banks():
    with Page('Iain M Banks'):
        with Section(class_names=['overview']):
            H1('Iain M Banks')
            P("""
                Banks passed away in 2013, and I've been carefully parceling out his
                remaining novels since.  
             """)
        with Section(class_names=['links']):
            H1('The Culture Novels')
            P("""
                Banks creates a vision of a galaxy-spanning
                post-scarcity future that is unique, hopeful and somehow very comforting
                in its humanity.  I was hooked in the early chapters of
                <em>Consider Phlebas</em>, though lots of folks in 
                <a href=https://www.reddit.com/r/printSF/>r/printSF</a> seem lukewarm
                on this one.  <em>The Player of Games</em> and <em>Use of
                Weapons</em> are probably better and more accessible starting places.
                For me, <em>Look to Windward</em> best captures the heart and soul of
                the Culture.            
            """)
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