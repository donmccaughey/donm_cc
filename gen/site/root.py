from markup import Ul, Section, H1, P, A, Text, H2, Em
from resources import IndexPage, File, Directory, Page
from site.collection import item
from site.links import book, link
from site.pages.aughey import aughey
from site.pages.bash import bash
from site.pages.business_novels import business_novels
from site.pages.engineering_management import engineering_management
from site.pages.hashtables import hashtables
from site.pages.home import home
from site.pages.macos_packages import macos_packages
from site.pages.make import make
from site.pages.memory_match import memory_match
from site.pages.random_words import random_words


root = home()
with root:
    File('base.css')
    Directory('banners')
    Directory('icons')
    Directory('resume')

    aughey()
    business_novels()
    bash()
    engineering_management()
    hashtables()
    macos_packages()
    make()
    memory_match()
    random_words()

    with IndexPage('Rust and Wasm'):
        with Section(class_names=['overview']):
            H1('Rust and Wasm (WebAssembly)')
            P("""
                <em>Rust</em> is a modern, strongly-typed, compiled language with
                strict safety guarantees focused on building high performance
                systems.
             """)
            P("""
                <em>Wasm</em> (WebAssembly) is a binary instruction format for a
                stack-based virtual machine that runs in modern JavaScript 
                execution environments.
             """)
            P("""
                Together, Rust and Wasm open up new ways to write web clients,
                new ways to share code between client and server, and allow web
                clients to tackle problems that were previously impractical in
                JavaScript.
            """)
        with Section(class_names=['links']):
            H1('Rust')
            with Ul():
                link('site', 'The Rust Programming Language site', 'https://www.rust-lang.org')
                link('book', 'The Rust Programming Language book', 'https://doc.rust-lang.org/book/')
                link('book', 'Rust by Example', 'https://doc.rust-lang.org/rust-by-example/')
        with Section(class_names=['links']):
            H1('Wasm')
            with Ul():
                link('site', 'WebAssembly site', 'https://webassembly.org')
                link('docs', 'WebAssembly MDN web docs', 'https://developer.mozilla.org/docs/WebAssembly')
                link('blog', "WebAssembly's post-MVP future: A cartoon skill tree", 'https://hacks.mozilla.org/2018/10/webassemblys-post-mvp-future/', date='2018-10-22')
        with Section(class_names=['links']):
            H1('Rust and Wasm')
            with Ul():
                link('repo', '<code>wasm-bindgen</code>: Import JavaScript things into Rust and export Rust things to JavaScript', 'https://github.com/rustwasm/wasm-bindgen')
                link('book', 'Rust and WebAssembly book', 'https://rustwasm.github.io/book/')
                link('blog', 'Rust and JavaScript Interop', 'https://blog.ryanlevick.com/posts/wasm-bindgen-interop/', date='2018-09-12')
                link('blog', 'WebAssembly and Rust: A Web Love Story', 'https://github.com/raphamorim/wasm-and-rust', date='2018-07-24')
            H2('Web Client Frameworks')
            with Ul():
                link('repo', 'stdweb', 'https://github.com/koute/stdweb')
                link('repo', 'Percy', 'https://github.com/chinedufn/percy')
                link('repo', 'Yew', 'https://github.com/DenisKolodin/yew')
                link('repo', 'Ruuhk', 'https://github.com/csharad/ruukh')
                link('repo', 'Draco', 'https://github.com/utkarshkukreti/draco')
                link('repo', 'Seed', 'https://github.com/David-OConnor/seed')
            H2('Libraries')
            with Ul():
                link('blog', 'Fast, Bump-Allocated Virtual DOMs with Rust and Wasm', 'https://hacks.mozilla.org/2019/03/fast-bump-allocated-virtual-doms-with-rust-and-wasm/')
                link('repo', 'Dodrio: A fast, bump-allocated virtual DOM library for Rust and WebAssembly.', 'https://github.com/fitzgen/dodrio')
            H2('Experience Reports')
            with Ul():
                link('blog', 'Lessons learned on writing web applications completely in Rust', 'https://medium.com/@saschagrunert/lessons-learned-on-writing-web-applications-completely-in-rust-2080d0990287', date='2018-10-03')
                link('blog', 'Isomorphic Desktop Apps with Rust', 'https://speice.io/2018/09/isomorphic-apps.html', date='2018-09-15')
                link('blog', 'A static web app in Rust: A three day tour of Yew and WASM in Rust', 'https://bluejekyll.github.io/blog/rust/2018/07/22/static-web-app-rust.html', date='2018-07-22')
                link('blog', 'A web application completely in Rust', 'https://medium.com/@saschagrunert/a-web-application-completely-in-rust-6f6bdb6c4471', date='2018-07-07')

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
            item('Lois McMaster Bujold', '/science_fiction/lois_mcmaster_bujold.html')
            item('James SA Corey', '/science_fiction/james_sa_corey.html')
            item('Alastair Reynolds', '/science_fiction/alastair_reynolds.html')

        with Page('Alastair Reynolds'):
            with Section(class_names=['overview']):
                H1('Alastair Reynolds')
                P()
            with Section(class_names=['links']):
                H1('Revelation Space')
                with Ul():
                    book('Revelation Space', 'https://www.amazon.com/gp/product/B001QL5MAA', date='2000', checked=True)
                    book('Chasm City', 'https://www.amazon.com/gp/product/B000OIZUH6', date='2001', checked=True)
                    book('Diamond Dogs, Turquoise Days', 'https://www.amazon.com/gp/product/B001JJWICY', date='2002', checked=True)
                    book('Redemption Ark', 'https://www.amazon.com/gp/product/B001LFDABO', date='2002', checked=True)
                    book('Absolution Gap', 'https://www.amazon.com/gp/product/B001ODO61G', date='2003', checked=True)
                    book('Galactic North', 'https://www.amazon.com/gp/product/B0017SWQJW', date='2006')
                    book('The Prefect / Aurora Rising', 'https://www.amazon.com/gp/product/B0015DYJY4', date='2007', checked=True)
                    book('Elysium Fire', 'https://www.amazon.com/gp/product/B073P43TMS', date='2018', checked=True)
            with Section(class_names=['links']):
                H1("Poseidon's Children")
                with Ul():
                    book('Blue Remembered Earth', 'https://www.amazon.com/gp/product/B005ZOCF5E', date='2012', checked=True)
                    book('On the Steel Breeze', 'https://www.amazon.com/gp/product/B00H2V6IN8', date='2013', checked=True)
                    book("Poseidon's Wake", 'https://www.amazon.com/gp/product/B00X5937LW', date='2015', checked=True)
            with Section(class_names=['links']):
                H1('Revenger')
                with Ul():
                    book('Revenger', 'https://www.amazon.com/gp/product/B01LXW2IUQ', date='2016', checked=True)
                    book('Shadow Captain', 'https://www.amazon.com/gp/product/B07CWQN8FQ', date='2019')
                    book('Bone Silence', 'https://www.amazon.com/gp/product/B0819W4456', date='2020')
            with Section(class_names=['links']):
                H1('Merlin')
                with P():
                    with A('http://approachingpavonis.blogspot.com/2016/10/new-merlin-story-iron-tactician.html'):
                        Text('There are four Merlin stories to date, ...')
                with Ul():
                    book('Hideaway', 'https://www.goodreads.com/book/show/34793859-hideaway', date='2000')
                    book("Minla's Flowers (included in <em>Zima Blue</em>)", 'https://www.amazon.com/gp/product/B00GVG07DC', date='2009', checked=True)
                    book('The Iron Tactician', 'https://www.amazon.com/Iron-Tactician-Alastair-Reynolds-ebook/dp/B01M2B9P7V', date='2016')
                    book("Merlin's Gun", 'https://www.amazon.com/Mammoth-Books-presents-Merlins-Gun-ebook/dp/B00OGUTTEI', date='2012', checked=True)
            with Section(class_names=['links']):
                H1('House of Suns')
                with Ul():
                    book('Thousandth Night', 'https://www.amazon.com/Thousandth-Night-Alastair-Reynolds-ebook/dp/B00C89ORWI', date='2013')
                    book('House of Suns', 'https://www.amazon.com/gp/product/B002AKPECW', date='2008', checked=True)
            with Section(class_names=['links']):
                H1('Other Stories')
                with Ul():
                    book('Century Rain', 'https://www.amazon.com/gp/product/B0010SB6OK', date='2004', checked=True)
                    book('Pushing Ice', 'https://www.amazon.com/gp/product/B00NW2Z04E', date='2005', checked=True)
                    book('Terminal World', 'https://www.amazon.com/gp/product/B01K3LNPCK', date='2009')
                    book('Troika', 'https://www.amazon.com/gp/product/B00C89K574', date='2010', checked=True)
                    book('Sleepover', 'https://www.amazon.com/gp/product/B00OGUTOE8', date='2010')
                    book('Slow Bullets', 'https://www.amazon.com/gp/product/B00WGX4KT6', date='2015', checked=True)
                    book('Permafrost', 'https://www.amazon.com/gp/product/B07HF26D1H', date='2019')
            with Section(class_names=['links']):
                H1('Collections')
                with Ul():
                    book('Zima Blue', 'https://www.amazon.com/gp/product/B00GVG07DC', date='2006', checked=True)
                    book('The Six Directions of Space', 'https://www.amazon.com/Six-Directions-Space-Alastair-Reynolds-ebook/dp/B00C89JZCA', date='2008')
                    book('Deep Navigation', 'https://www.amazon.com/gp/product/B00XT0V0DY', date='2010')
                    book('Beyond the Aquila Rift', 'https://www.amazon.com/gp/product/B01FE7KJ2C', date='2016')

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
                    book('Consider Phlebas', 'https://www.amazon.com/gp/product/B0013TX6FI', date='1987', checked=True)
                    book('The Player of Games', 'https://www.amazon.com/gp/product/B002WM3HC2', date='1988', checked=True)
                    book('Use of Weapons', 'https://www.amazon.com/gp/product/B0015DWLTE', date='1990', checked=True)
                    book('The State of the Art (collection)', 'https://www.goodreads.com/book/show/129131.The_State_of_the_Art', date='1991', checked=True)
                    book('Excession', 'https://www.amazon.com/Excession-Iain-M-Banks/dp/0553575376', date='1996', checked=True)
                    book('Inversions', 'https://www.amazon.com/Inversions-Iain-M-Banks/dp/074341196X', date='1998', checked=True)
                    book('Look to Windward', 'https://www.amazon.com/gp/product/B001D20270', date='2000', checked=True)
                    book('Matter', 'https://www.amazon.com/gp/product/B000VMHI98', date='2008', checked=True)
                    book('Surface Detail', 'https://www.amazon.com/gp/product/B0046A9NLC', date='2010', checked=True)
                    book('The Hydrogen Sonata', 'https://www.amazon.com/gp/product/B0081BU42O', date='2012', checked=True)
            with Section(class_names=['links']):
                H1('Other Novels')
                with Ul():
                    book('Against a Dark Background', 'https://www.amazon.com/gp/product/B002CT0TXK', date='1993')
                    book('Feersum Endjinn', 'https://www.amazon.com/Feersum-Endjinn-Novel-Iain-Banks/dp/0553374591', date='1994')
                    book('The Algebraist', 'https://www.amazon.com/Algebraist-Iain-M-Banks/dp/1597800449', date='2004')
                    book('Transition', 'https://www.amazon.com/gp/product/B002O0Q6YS', date='2009')

        with Page('James SA Corey'):
            with Section(class_names=['overview']):
                H1('James SA Corey')
            with Section(class_names=['links']):
                H1('The Expanse')
                Em('(publication order)')
                with Ul():
                    book('Leviathan Wakes', 'https://www.amazon.com/gp/product/B0047Y171G', date='2011', checked=True)
                    book('The Butcher of Anderson Station (novella)', 'https://www.amazon.com/gp/product/B0052AHUYM', date='2011', checked=True)
                    book("Caliban's War", 'https://www.amazon.com/gp/product/B005SCRR1A', date='2012', checked=True)
                    book('Gods of Risk (novella)', 'https://www.amazon.com/gp/product/B008CJ241O', date='2012', checked=True)
                    book('Drive (short story)', 'https://www.syfy.com/theexpanse/drive/', date='2012')
                    book("Abaddon's Gate", 'https://www.amazon.com/gp/product/B00A2DZMYE', date='2013', checked=True)
                    book('The Churn (novella)', 'https://www.amazon.com/gp/product/B00I82884W', date='2014', checked=True)
                    book('Cibola Burn', 'https://www.amazon.com/gp/product/B00FPQA4F0', date='2014', checked=True)
                    book('Nemesis Games', 'https://www.amazon.com/gp/product/B00O7X626W', date='2015', checked=True)
                    book('The Vital Abyss (novella)', 'https://www.amazon.com/gp/product/B015NRKNS8', date='2015', checked=True)
                    book("Babylon's Ashes", 'https://www.amazon.com/gp/product/B018S2773Y', date='2016', checked=True)
                    book('Strange Dogs (novella)', 'https://www.amazon.com/gp/product/B06ZZ1MKW8', date='2017', checked=True)
                    book('Persepolis Rising', 'https://www.amazon.com/gp/product/B06XKN9G27', date='2017')
                    book("Tiamat's Wrath", 'https://www.amazon.com/gp/product/B07BVNVWL6', date='2019')
                    book('Auberon (novella)', 'https://www.amazon.com/gp/product/B07YKR19FN', date='2019')
                    book('The Last Flight of the Cassandra', 'https://www.goodreads.com/book/show/49233894-the-last-flight-of-the-cassandra', date='2019')

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
                    book("Dreamweaver's Dilemma (short story)", 'https://www.amazon.com/Dreamweavers-Dilemma-Lois-McMaster-Bujold/dp/0915368536', date='1995')
                    book('Falling Free', 'https://www.amazon.com/gp/product/B005SHX1CE', date='1987', checked=True)
                    book('Shards of Honor', 'https://www.amazon.com/gp/product/B005BH9T86', date='1986', checked=True)
                    book('Aftermaths (short story)', 'https://www.goodreads.com/book/show/869033.Far_Frontiers_5', date='1986')
                    book('Barrayar', 'https://www.amazon.com/gp/product/B005BFIH7M', date='1991', checked=True)
                    book("The Warrior's Apprentice", 'https://www.amazon.com/gp/product/B005DNGSUU', date='1986', checked=True)
                    book('Mountains of Mourning (novella)', 'https://www.amazon.com/gp/product/B004O4C13W', date='1989', checked=True)
                    book('Weatherman (novella)', 'https://www.amazon.com/gp/product/B004U7LWQK', date='1990', checked=True)
                    book('The Vor Game', 'https://www.amazon.com/gp/product/B005O2WQ60', date='1990', checked=True)
                    book('Cetaganda', 'https://www.amazon.com/gp/product/B007XFJDYO', date='1995', checked=True)
                    book('Ethan of Athos', 'https://www.amazon.com/Ethan-Athos-Vorkosigan-McMaster-Bujold-ebook/dp/B0055EFASI', date='1986', checked=True)
                    book('Labyrinth (novella)', 'https://www.amazon.com/gp/product/B004YXBDG4', date='1989', checked=True)
                    book('The Borders of Infinity (novella)', 'https://www.amazon.com/Borders-Infinity-3-novella-collection-Vorkosigan-ebook/dp/B0062CKP2S', date='1989', checked=True)
                    book('Brothers in Arms', 'https://www.amazon.com/gp/product/B005S4FLCK', date='1989', checked=True)
                    book('Mirror Dance', 'https://www.amazon.com/gp/product/B005AJQ9U6', date='1994', checked=True)
                    book('Memory', 'https://www.amazon.com/gp/product/B005LI3W9W', date='1996', checked=True)
                    book('Komarr', 'https://www.amazon.com/gp/product/B005FRGCZA', date='1998', checked=True)
                    book('A Civil Campaign', 'https://www.amazon.com/gp/product/B005FSI1IK', date='1999', checked=True)
                    book('Winterfair Gifts', 'https://www.amazon.com/gp/product/B004I6CZ28', date='2004', checked=True)
                    book('Diplomatic Immunity', 'https://www.amazon.com/gp/product/B005GLJD7E', date='2002', checked=True)
                    book("Captain Vorpatril's Alliance", 'https://www.amazon.com/gp/product/B00AP9RQE4', date='2012', checked=True)
                    book('Cryoburn', 'https://www.amazon.com/gp/product/B00APACSJG', date='2010', checked=True)
                    book('Gentleman Jole and the Red Queen', 'https://www.amazon.com/gp/product/B01A9CDKDC', date='2016', checked=True)
                    book('The Flowers of Vashnoi (novella)', 'https://www.amazon.com/Flowers-Vashnoi-Vorkosigan-Saga-ebook/dp/B07D4M7N3L', date='2018', checked=True)

