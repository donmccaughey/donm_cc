from markup import Div, Ul, Section, H1, P, A, Text, Code, Form, \
    Label, Input, Button, Li, H2, Em
from resources import IndexPage, File, Directory, Page
from site.collection import item
from site.links import book, link
from site.packages import package
from site.pages.aughey import aughey
from site.pages.home import home


root = IndexPage('Don McCaughey', is_root=True)

with root:
    home()

    File('base.css')
    Directory('banners')
    Directory('icons')
    Directory('resume')

    aughey()

    with IndexPage('Business Novels'):
        with Section(class_names=['overview']):
            H1('Business Novels')
            P()
        with Section(class_names=['links']):
            H1('Recommended')
            with Ul():
                book('The Goal', 'https://www.amazon.com/Goal-Process-Ongoing-Improvement-ebook/dp/B002LHRM2O', authors='Eliyahu M Goldratt and Jeff Cox', date='1984', checked=True)
                book('The Phoenix Project', 'https://www.amazon.com/Phoenix-Project-DevOps-Helping-Business-ebook/dp/B078Y98RG8', authors='Gene Kim, Kevin Behr and George Spafford', date='2018', checked=True)
                book('The Unicorn Project', 'https://www.amazon.com/Unicorn-Project-Developers-Disruption-Thriving-ebook/dp/B07QT9QR41', authors='Gene Kim', date='2019', checked=True)
                book('The Ideal Team Player', 'https://www.amazon.com/Ideal-Team-Player-Recognize-Cultivate-ebook/dp/B01B6AEJJ0', authors='Patrick Lencioni', date='2016', checked=True)
                book('The Five Dysfunctions of a Team', 'https://www.amazon.com/Five-Dysfunctions-Team-Leadership-Lencioni-ebook/dp/B006960LQW', authors='Patrick Lencioni', date='2011', checked=True)
                book('The Four Obsessions of an Extraordinary Executive', 'https://www.amazon.com/Four-Obsessions-Extraordinary-Executive-Leadership-ebook/dp/B003WUYQOQ', authors='Patrick Lencioni', date='2008', checked=True)
        with Section(class_names=['links']):
            H1('Your Mileage May Vary')
            with Ul():
                book('The Five Temptations of a CEO', 'https://www.amazon.com/Five-Temptations-CEO-10th-Anniversary-ebook/dp/B0062OAEWM', authors='Patrick Lencioni', date='2008', checked=True)
                book('Critical Chain', 'https://www.amazon.com/Critical-Chain-Business-Eliyahu-Goldratt-ebook/dp/B002LHRM2E', authors='Eliyahu M Goldratt', date='1997', checked=True)
        with Section(class_names=['links']):
            H1('On My Readling List')
            with Ul():
                book('The Deadline: A Novel About Project Management', 'https://www.amazon.com/Deadline-Novel-About-Project-Management-ebook/dp/B006MN4RAS', authors='Tom DeMarco', date='2011')
                book('How To Destroy A Tech Startup In Three Easy Steps', 'https://www.amazon.com/Destroy-Tech-Startup-Three-Steps-ebook/dp/B0772FJQ1T', authors='Lawrence Krubner', date='2017', checked=True)
        with Section(class_names=['links']):
            H1('Business Comics')
            with Ul():
                book('The Adventures of Johnny Bunko', 'https://www.amazon.com/Adventures-Johnny-Bunko-Career-Guide-ebook/dp/B0015DRPL8', authors='Daniel H Pink and Reb Ten Pas', date='2008', checked=True)
                book("What Got You Here Won't Get You There", 'https://www.amazon.com/What-Here-There-illustrated-version-ebook/dp/B00710YFJY', authors='Marshall Goldsmith, Mark Reiter and Shane Clester', date='2011', checked=True)

    with IndexPage('Bash'):
        with Section(class_names=['overview']):
            H1('Bash: the "Bourne-again" shell')
            P()
        with Section(class_names=['links']):
            H1('Tips and Tricks')
            with Ul():
                link('blog', 'Use the Unofficial Bash Strict Mode (Unless You Looove Debugging)', 'http://redsymbol.net/articles/unofficial-bash-strict-mode/', authors='Aaron Maxwell')
                link('blog', 'How to write idempotent Bash scripts', 'https://arslan.io/2019/07/03/how-to-write-idempotent-bash-scripts/', authors='Fatih Arslan', date='2019-07-03')
                link('blog', 'Shortcuts to Move Faster in Bash Command Line', 'http://teohm.github.io/blog/2012/01/04/shortcuts-to-move-faster-in-bash-command-line/', authors='Huiming Teo', date='2012-01-04')

    with IndexPage('Engineering Management'):
        with Section(class_names=['overview']):
            H1('Engineering Management')
            P("""
                In 2017 I became an engineering manager, a career change I wasn't
                looking for and hadn't previously considered.  My experience as
                consultant, tech lead and member of Extreme Programming teams
                helped in the transition, but there is still a lot to learn in my
                new role.
            """)
            P("""
                Management is a skill quite different from software engineering,
                and I still consider myself a beginner.  This page includes some
                of the things I've found useful.
            """)
        with Section(class_names=['links']):
            H1('Practical')
            with Ul():
                link('podcast', 'Manager Tools "Basics"', 'https://www.manager-tools.com/manager-tools-basics', authors='Michael Auzenne and Mark Horstman', date='2005')
                link('book', 'Crucial Conversations: Tools for Talking When Stakes Are High', 'https://www.amazon.com/gp/product/B005K0AYH4', authors='Kerry Patterson, Joseph Grenny, Ron McMillan and Al Switzler', date='2011')
                link('book', 'Crucial Accountability: Tools for Resolving Violated Expectations, Broken Commitments and Bad Behavior', 'https://www.amazon.com/Crucial-Accountability-Resolving-Expectations-Commitments-ebook/dp/B00C4BDRW6', authors='Kerry Patterson, Joseph Grenny, Ron McMillan and Al Switzler', date='2013')
                link('blog', 'Ask a Manager', 'https://www.askamanager.org', authors='Alison Green')
        with Section(class_names=['links']):
            H1('Engineering Management')
            with Ul():
                link('email', 'Software Lead Weekly: A weekly email for busy people who care about people, culture and leadership', 'http://softwareleadweekly.com', authors='Oren Ellenbogen')
                link('book', "The Manager's Path: A Guide for Tech Leaders Navigating Growth and Change", 'https://www.amazon.com/gp/product/B06XP3GJ7F', authors='Camille Fournier', date='2017')
                link('blog', 'Irrational Exuberance!', 'https://lethain.com', authors='Will Larson')
        with Section(class_names=['links']):
            H1('Teamwork')
            with Ul():
                link('book', 'The Five Dysfunctions of a Team: A Leadership Fable', 'https://www.amazon.com/gp/product/B006960LQW', authors='Patrick Lencioni', date='2011')
                link('book', 'The Ideal Team Player: How to Recognize and Cultivate the Three Essential Virtues', 'https://www.amazon.com/Ideal-Team-Player-Recognize-Cultivate-ebook/dp/B01B6AEJJ0', authors='Patrick Lencioni', date='2016')
        with Section(class_names=['links']):
            H1('Leadership')
            with Ul():
                link('book', 'Turn the Ship Around!: A True Story of Turning Followers into Leaders', 'https://www.amazon.com/gp/product/B00AFPVP0Y', authors='L David Marquet', date='2013')
                link('book', 'The Four Obsessions of an Extraordinary Executive: A Leadership Fable', 'https://www.amazon.com/gp/product/B003WUYQOQ', authors='Patrick Lencioni', date='2008')
        with Section(class_names=['links']):
            H1('Theoretical')
            with Ul():
                link('book', 'Measuring and Managing Performance in Organizations', 'https://www.amazon.com/gp/product/B00DY3KQX6', authors='Robert D Austin', date='1996')
                link('book', "Don't Shoot the Dog: The Art of Teaching and Training", 'https://www.amazon.com/Dont-Shoot-Dog-Teaching-Training/dp/1982106468', authors='Karen Pryor', date='1984')

    with IndexPage('Hashtables'):
        with Section(class_names=['overview']):
            H1('Hashtables')
            with P():
                A('https://en.wikipedia.org/wiki/Hash_table', 'Hashtables')
                Text("""
                    are such an interesting and foundational data structure, though sadly
                    but understandably missing from the C standard library (and only
                    added to C++ in
                """)
                A('https://en.cppreference.com/w/cpp/container/unordered_map', 'C++ 11')
                Text(').')
            with P():
                Text('I have my own unpolished ')
                A('https://github.com/donmccaughey/hashtable', 'hashtable for C')
                Text("""
                    and I enjoy collecting links to other implementations, hashing
                    functions and related articles.
                """)
        with Section(class_names=['links']):
            H1('Hashtable Implementations')
            with Ul():
                link('repo', 'uthash: C macros for hash tables and more', 'https://github.com/troydhanson/uthash')
        with Section(class_names=['links']):
            H1('Hashing Functions')
            with Ul():
                link('site', 'FNV Hash', 'http://www.isthe.com/chongo/tech/comp/fnv/index.html', authors='Landon Curt Noll', date='2017-04-29')
        with Section(class_names=['links']):
            H1('Hashing')
            with Ul():
                link('blog', 'Advanced techniques to implement fast hash tables', 'https://attractivechaos.wordpress.com/2018/10/01/advanced-techniques-to-implement-fast-hash-tables/', date='2018-10-01')
                link('blog', 'A Probing Hash Table Framework', 'https://skystrife.github.io/blog/2016/01/29/a-probing-hash-table-framework/', authors='Chase Geigle', date='2016-01-29')
                link('blog', 'Best hash table for C', 'https://www.reddit.com/r/C_Programming/comments/3533bw/best_hash_table_for_c/', authors='Reddit', date='2015-05-06')
                link('blog', "Types Don't Know #", 'https://isocpp.org/files/papers/n3980.html', authors='Howard E. Hinnant, Vinnie Falco and John Bytheway', date='2014-05-24')
                link('blog', 'Dynamic Hash Tables', 'https://www.csd.uoc.gr/~hy460/pdf/Dynamic%20Hash%20Tables.pdf', authors='Per-Åke Larson', date='1988-04')

    with IndexPage('macOS Packages', has_files=True):
        with Section(class_names=['overview']):
            H1('Signed macOS Installer Packages')
            with P():
                Text('These standard macOS installer packages are built using ')
                Code('pkgbuild')
                Text(' and ')
                Code('productbuild')
                Text(' and are signed with my Apple developer credentials.')
            P("""
                This is a collection of command line tools that I've found useful
                at one time or another over the years. Some of them are widely used
                but excluded from macOS and Xcode due to GPL licenses.            
            """)
        package(
            name='pkg-config',
            version='0.29.1',
            package='https://github.com/donmccaughey/pkg-config_pkg/releases/download/v0.29.2-r1/pkg-config-0.29.2.pkg',
            source='https://github.com/donmccaughey/pkg-config_pkg',
            project='https://www.freedesktop.org/wiki/Software/pkg-config/',
            description='A helper tool used when compiling applications and libraries.'
        )
        package(
            name='tree',
            version='1.7.0',
            package='https://github.com/donmccaughey/tree_pkg/releases/download/v1.7.0-r1/tree-1.7.0.pkg',
            source='https://github.com/donmccaughey/tree_pkg',
            project='http://mama.indstate.edu/users/ice/tree/',
            description='A recursive directory listing command.'
        )
        package(
            name='XZ Utils',
            version='5.2.4',
            package='https://github.com/donmccaughey/xz_pkg/releases/download/v5.2.4-r1/xz-5.2.4.pkg',
            source='https://github.com/donmccaughey/xz_pkg',
            project='https://tukaani.org/xz/',
            description='A general purpose data compression tool and library, and includes the <code>xz</code> command line tool.'
        )

    with IndexPage('Make'):
        with Section(class_names=['overview']):
            H1('Make: a Tool for Building Software')
            with P():
                Text('Make is old. It was ')
                A('https://en.wikipedia.org/wiki/Make_(software)', 'first released')
                Text("""
                    in 1977.  It's ubiquitous.  Make is a
                """)
                A('http://pubs.opengroup.org/onlinepubs/009695399/utilities/make.html', 'standard')
                Text("""
                    development tool on Unix, Linux and POSIX systems.  Make is not 
                    easy to use.  It has many well-known warts and pitfalls.  The
                    things a beginner wants to do with Make aren't the things that Make
                    wants you to do.
                """)
            P("""
                Nevertheless, Make has survived for forty years because it is often
                good enough.  If you develop software, particularly if you work in 
                C or C++, you will encounter a makefile sooner or later.
            """)
            with P():
                Text("""
                    When you truly realize that Make is a <em>declarative</em> language
                    for specifying a
                """)
                A('https://en.wikipedia.org/wiki/Directed_acyclic_graph', 'directed acyclic graph')
                Text(',')
                Text("""
                    where the vertices are files and the edges are build scripts, then 
                    you can use Make effectively.  Even after many years, I still
                    sometimes forget this in both obvious and subtle ways while using
                    Make.
                """)
        with Section(class_names=['links']):
            H1('Books')
            with Ul():
                link('book', 'Managing Projects with GNU Make', 'https://www.amazon.com/Managing-Projects-GNU-Make-Handbooks/dp/0596006101', authors='Robert Mecklenburg', date='2004')
                link('book', 'The GNU Make Book', 'https://nostarch.com/gnumake', authors='John Graham-Cumming', date='2015')
                link('book', 'The GNU Make Manual', 'https://www.gnu.org/software/make/manual/html_node/index.html', date='2016')
        with Section(class_names=['links']):
            H1('Articles')
            with Ul():
                link('blog', 'Notes for new Make users', 'http://gromnitsky.users.sourceforge.net/articles/notes-for-new-make-users/', authors='Alexander Gromnitsky', date='2019-03-09')
                link('blog', 'make.mad-scientist.net', 'http://make.mad-scientist.net', authors='Paul D Smith', date='2017-07-30')
                link('blog', 'Notes on Writing Makefiles', 'http://eigenstate.org/notes/makefiles', authors='Ori Bernstein')
                link('blog', 'Self-Documented Makefile', 'http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html', authors='François Zaninotto', date='2016-02-29')

    with IndexPage('Memory Match', has_files=True) as page:
        page.add_script('https://cdnjs.cloudflare.com/ajax/libs/cash/1.3.0/cash.min.js')
        page.add_script('memory_match.js')
        Div(id='memory_match')

    with IndexPage('Random Words', has_files=True) as page:
        page.add_stylesheet('random_words.css')
        page.add_script('random_words.js')
        with Section(class_names=['overview']):
            H1('Random Words')
            P("""
                <em>Random Words</em> is a small program that chooses random
                entries from <a href=https://github.com/elasticdog/yawl>YAWL</a>,
                a public domain list of 264,097 English words.
             """)
        with Section(class_names=['generator']):
            H1('Results')
            P(id='random_words')
            with Form(action='./', method='GET'):
                with P():
                    Label('Number of Words:', for_id='count')
                    Input(id='count', type='number', value='0')
                with P():
                    Label('Format:')
                    Input(id='format_sentence', name='format', type='radio', value='sentence', checked=True)
                    Label('Sentence', for_id='format_sentence')
                    Input(id='format_list', name='format', type='radio', value='list')
                    Label('List', for_id='format_list')
                with P():
                    Button('Go')
        with Section(id='implementation'):
            H1('Implementation')
            with P():
                Text("""
                    <em>Random Words</em> is written in JavaScript and runs in the
                    browser.  To avoid the need to fetch the whole 2.7 MB YAWL
                    <a href=word.list><code>word.list</code></a> file, I've converted
                    <code>word.list</code> into a <a href=words.table>table</a> where 
                    each word is padded with spaces to 45 characters, the length of the
                 """)
                A('https://en.wikipedia.org/wiki/Pneumonoultramicroscopicsilicovolcanoconiosis', 'longest word')
                Text("""
                    in the list.
                 """)
            with P():
                Text("""
                    The program uses the
                 """)
                A('https://developer.mozilla.org/en-US/docs/Web/API/Crypto/getRandomValues', '<code>getRandomValues()</code>')
                Text("""
                    function to generate a random number in the range [0, 264097) to 
                    select a word, then uses the HTTP
                 """)
                A('https://tools.ietf.org/html/rfc7233#section-3.1', 'Range header')
                Text("""
                    to fetch only that word from the table.
                 """)
            with P():
                with Ul():
                    with Li():
                        A('random_words.js', 'The JavaScript code')
                    with Li():
                        A('word.list', 'The YAWL word list')
                    with Li():
                        A('make_table.py', 'The Python script to generate the words table')
                    with Li():
                        A('words.table', 'The table of padded words')

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

