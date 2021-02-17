from markup import Section, H1, P, Em, Ul
from resources import Page
from site.links import book


def lois_mcmaster_bujold():
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