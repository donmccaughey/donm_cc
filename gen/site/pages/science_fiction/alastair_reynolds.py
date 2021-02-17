from markup import Section, H1, P, Ul, A, Text
from resources import Page
from site.links import book


def alastair_reynolds():
    with Page('Alastair Reynolds'):
        with Section(class_names=['overview']):
            H1('Alastair Reynolds')
            P("""
                Reynolds is an astrophysicist turned writer with a nack for
                creating trippy, mind-bending stories.
            """)
        with Section(class_names=['links']):
            H1('Revelation Space')
            P("""
                <em>Revelation Space</em> is the gateway drug that got me hooked
                on Reynolds' strange vision of the future.  It forms
                a loosely connected trilogy with <em>Redemption Ark</em> (featuring
                a riveting near-light-speed chase between the stars spanning decades) and 
                <em>Absolution Gap</em> (with a virus-induced religious cult, moving cathedrals
                and a vanishing gas giant). 
            """)
            P("""
                <em>Aurora Rising</em> and <em>Elysium Fire</em> form the
                <a href=http://approachingpavonis.blogspot.com/2017/07/elysium-fire-and-new-title-for-prefect.html>Prefect
                Dreyfuss Emergency</a> sub-series.  They're police procedurals
                set in the Glitter Band, a swarm of thousands of orbital habitats.
            """)
            with Ul():
                book('Revelation Space',
                     'https://www.amazon.com/gp/product/B001QL5MAA',
                     date='2000', checked=True)
                book('Chasm City',
                     'https://www.amazon.com/gp/product/B000OIZUH6',
                     date='2001', checked=True)
                book('Diamond Dogs, Turquoise Days',
                     'https://www.amazon.com/gp/product/B001JJWICY',
                     date='2002', checked=True)
                book('Redemption Ark',
                     'https://www.amazon.com/gp/product/B001LFDABO',
                     date='2002', checked=True)
                book('Absolution Gap',
                     'https://www.amazon.com/gp/product/B001ODO61G',
                     date='2003', checked=True)
                book('Galactic North',
                     'https://www.amazon.com/gp/product/B0017SWQJW',
                     date='2006')
                book('The Prefect / Aurora Rising',
                     'https://www.amazon.com/gp/product/B0015DYJY4',
                     date='2007', checked=True)
                book('Elysium Fire',
                     'https://www.amazon.com/gp/product/B073P43TMS',
                     date='2018', checked=True)
        with Section(class_names=['links']):
            H1("Poseidon's Children")
            with Ul():
                book('Blue Remembered Earth',
                     'https://www.amazon.com/gp/product/B005ZOCF5E',
                     date='2012', checked=True)
                book('On the Steel Breeze',
                     'https://www.amazon.com/gp/product/B00H2V6IN8',
                     date='2013', checked=True)
                book("Poseidon's Wake",
                     'https://www.amazon.com/gp/product/B00X5937LW',
                     date='2015', checked=True)
        with Section(class_names=['links']):
            H1('Revenger')
            with Ul():
                book('Revenger',
                     'https://www.amazon.com/gp/product/B01LXW2IUQ',
                     date='2016', checked=True)
                book('Shadow Captain',
                     'https://www.amazon.com/gp/product/B07CWQN8FQ',
                     date='2019')
                book('Bone Silence',
                     'https://www.amazon.com/gp/product/B0819W4456',
                     date='2020')
        with Section(class_names=['links']):
            H1('Merlin')
            with P():
                with A('http://approachingpavonis.blogspot.com/2016/10/new-merlin-story-iron-tactician.html'):
                    Text('There are four Merlin stories to date, ...')
            with Ul():
                book('Hideaway',
                     'https://www.goodreads.com/book/show/34793859-hideaway',
                     date='2000')
                book("Minla's Flowers (included in <em>Zima Blue</em>)",
                     'https://www.amazon.com/gp/product/B00GVG07DC',
                     date='2009', checked=True)
                book('The Iron Tactician',
                     'https://www.amazon.com/Iron-Tactician-Alastair-Reynolds-ebook/dp/B01M2B9P7V',
                     date='2016')
                book("Merlin's Gun",
                     'https://www.amazon.com/Mammoth-Books-presents-Merlins-Gun-ebook/dp/B00OGUTTEI',
                     date='2012', checked=True)
        with Section(class_names=['links']):
            H1('House of Suns')
            with Ul():
                book('Thousandth Night',
                     'https://www.amazon.com/Thousandth-Night-Alastair-Reynolds-ebook/dp/B00C89ORWI',
                     date='2013')
                book('House of Suns',
                     'https://www.amazon.com/gp/product/B002AKPECW',
                     date='2008', checked=True)
        with Section(class_names=['links']):
            H1('Other Stories')
            with Ul():
                book('Century Rain',
                     'https://www.amazon.com/gp/product/B0010SB6OK',
                     date='2004', checked=True)
                book('Pushing Ice',
                     'https://www.amazon.com/gp/product/B00NW2Z04E',
                     date='2005', checked=True)
                book('Terminal World',
                     'https://www.amazon.com/gp/product/B01K3LNPCK',
                     date='2009')
                book('Troika',
                     'https://www.amazon.com/gp/product/B00C89K574',
                     date='2010', checked=True)
                book('Sleepover',
                     'https://www.amazon.com/gp/product/B00OGUTOE8',
                     date='2010')
                book('Slow Bullets',
                     'https://www.amazon.com/gp/product/B00WGX4KT6',
                     date='2015', checked=True)
                book('Permafrost',
                     'https://www.amazon.com/gp/product/B07HF26D1H',
                     date='2019')
        with Section(class_names=['links']):
            H1('Collections')
            P("""
                Reynolds' short stories are like small bite-sized versions of his
                novels.  Notably, the stories <em>Zima Blue</em> and <em>Beyond the Aquila Rift</em>
                come to life in episodes of the animated series
                <a href=https://www.netflix.com/title/80174608>Love, Death & Robots</a>.
            """)
            with Ul():
                book('Zima Blue',
                     'https://www.amazon.com/gp/product/B00GVG07DC',
                     date='2006', checked=True)
                book('The Six Directions of Space',
                     'https://www.amazon.com/Six-Directions-Space-Alastair-Reynolds-ebook/dp/B00C89JZCA',
                     date='2008')
                book('Deep Navigation',
                     'https://www.amazon.com/gp/product/B00XT0V0DY',
                     date='2010')
                book('Beyond the Aquila Rift',
                     'https://www.amazon.com/gp/product/B01FE7KJ2C',
                     date='2016')