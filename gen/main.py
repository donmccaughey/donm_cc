from typing import Optional

from resources import Directory, File, IndexPage, Page
from tags import A, Br, Button, Code, Div, Em, Form, H1, Img, Input, Label, Li
from tags import P, Section, Span, Strong, Text, Time, Ul


def item(
        title: str,
        subtitle: str,
        href: str,
        favicon: Optional[str] = None,
        is_local: bool = False
):
    class_names = ['item'] + (['local'] if is_local else [])
    with A(class_names=class_names, href=href):
        if favicon:
            Img(class_names=['favicon'], src=favicon, alt=f'{title} icon')
        Strong(title)
        Br()
        Em(subtitle)


def link(
        type: str,
        title: str,
        href: str,
        authors: Optional[str] = None,
        date: Optional[str] = None,
        checked: bool = False
):
    with A(class_names=[type], href=href):
        Text(title)
        if authors:
            Span(class_names=['authors'], text=authors)
        if date:
            Time(datetime=date)
        if checked:
            Text('✓')


def book(
        title: str,
        href: str,
        author: Optional[str] = None,
        date: Optional[str] = None,
        checked: bool = False
):
    link(
        type='book',
        title=title,
        href=href,
        authors=author,
        date=date,
        checked=checked,
    )


def package(
        name: str,
        version: str,
        package: str,
        source: str,
        project: str,
        description: str,
):
    with Section(class_names=['package']):
        H1(f'{name} {version}')
        P(description)
        with Div(class_names=['collection']):
            with A(package, class_names=['item']):
                Img('./package-32x32.png', 'package icon', class_names=['favicon'])
                Strong('package')
            with A(source, class_names=['item']):
                Img('./source-32x32.png', 'source icon', class_names=['favicon'])
                Strong('source')
            with A(project, class_names=['item']):
                Img('./project-32x32.png', 'project icon', class_names=['favicon'])
                Strong('project')


root = IndexPage('Don McCaughey', is_root=True)
with root:
    with Div(class_names=['banner']):
        Img(
            src='/banners/Don_and_Molly_Round_Hill_Lake_Tahoe_summer_2019.jpg',
            alt='Don and Molly atop Round Hill'
        )
        Span(
            text='Round Hill, Lake Tahoe, summer 2019',
            class_names=['lower-caption']
        )
    with Div(class_names=['collection']):
        item('Sourcehut', 'donmcc', 'https://git.sr.ht/~donmcc')
        item('GitHub', 'donmccaughey', 'https://github.com/donmccaughey', favicon='/icons/github.png')
        item('Twitter', '@donmccaughey', 'https://twitter.com/donmccaughey', favicon='/icons/twitter.png')
        item('LinkedIn', 'donmccaughey', 'https://www.linkedin.com/in/donmccaughey', favicon='/icons/linkedin.png')
        item('Résumé', "Stuff I've done", '/resume/Resume_of_Don_McCaughey.pdf', is_local=True)
        item('Truework', 'My current gig', 'https://www.truework.com', favicon='/icons/truework.png')
        item('Copper', 'My previous gig', 'https://www.copper.com', favicon='/icons/copper.png')
        item('Memory Match', 'A tile matching game', '/memory_match/', is_local=True)
        item('macOS Packages', 'Software installers', '/macos_packages/', favicon='/macos_packages/package-32x32.png', is_local=True)
        item('Engineering Management', 'Software is a team sport', '/engineering_management/', is_local=True)
        item('Rust and Wasm', 'Assembling the web', '/rust_and_wasm/', is_local=True)
        item('Make', 'The build tool', '/make/', is_local=True)
        item('Hashtables', 'Keys and values', '/hashtables/', is_local=True)
        item('Science Fiction', 'Reading for fun', '/science_fiction/', is_local=True)
        item('Random Words', 'A handy word picker', '/random_words/', is_local=True)

    File('base.css')
    Directory('banners')
    Directory('icons')
    Directory('resume')

    with IndexPage('Don McCaughey', name='aughey', has_files=True):
        with Div(class_names=['banner']):
            Img(src='/aughey/handstand.jpg', alt='Don doing a handstand')
            Span(class_names=['caption'], text='Coachella Festival, spring 2007')

    with IndexPage('Business Novels'):
        with Section(class_names=['overview']):
            H1('Business Novels')
            P()
        with Section(class_names=['links']):
            H1('Recommended')
            book('The Goal', '', checked=True)
            book('The Phoenix Project', '', checked=True)
            book('The Unicorn Project', '', checked=True)
            book('The Ideal Team Player', '', checked=True)
            book('The Five Dysfunctions of a Team', '', checked=True)
            book('The Four Obsessions of an Extraordinary Executive', '', checked=True)
        with Section(class_names=['links']):
            book('The Five Temptations of a CEO', '', checked=True)
            book('Critical Chain', '', checked=True)
            book('The Deadline: A Novel About Project Management', '')
            book('How To Destroy A Tech Startup In Three Easy Steps', '', checked=True)
        with Section(class_names=['links']):
            H1('Business Comics')
            book('The Adventures of Johnny Bunko', '', checked=True)
            book("What Got You Here Won't Get You There", '', checked=True)

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
            link('podcast', 'Manager Tools "Basics"', 'https://www.manager-tools.com/manager-tools-basics', authors='Michael Auzenne and Mark Horstman')
            link('book', 'Crucial Conversations: Tools for Talking When Stakes Are High', 'https://www.amazon.com/gp/product/B005K0AYH4', authors='Kerry Patterson, Joseph Grenny, Ron McMillan and Al Switzler')
            link('book', 'Crucial Accountability: Tools for Resolving Violated Expectations, Broken Commitments and Bad Behavior', 'https://www.amazon.com/Crucial-Accountability-Resolving-Expectations-Commitments-ebook/dp/B00C4BDRW6', authors='Kerry Patterson, Joseph Grenny, Ron McMillan and Al Switzler')
            link('blog', 'Ask a Manager', 'https://www.askamanager.org', authors='Alison Green')
        with Section(class_names=['links']):
            H1('Engineering Management')
            link('email', 'Software Lead Weekly: A weekly email for busy people who care about people, culture and leadership', 'http://softwareleadweekly.com', authors='Oren Ellenbogen')
            link('book', "The Manager's Path: A Guide for Tech Leaders Navigating Growth and Change", 'https://www.amazon.com/gp/product/B06XP3GJ7F', authors='Camille Fournier')
            link('blog', 'Irrational Exuberance!', 'https://lethain.com', authors='Will Larson')
        with Section(class_names=['links']):
            H1('Teamwork')
            link('book', 'The Five Dysfunctions of a Team: A Leadership Fable', 'https://www.amazon.com/gp/product/B006960LQW', authors='Patrick Lencioni')
            link('book', 'The Ideal Team Player: How to Recognize and Cultivate the Three Essential Virtues', 'https://www.amazon.com/Ideal-Team-Player-Recognize-Cultivate-ebook/dp/B01B6AEJJ0', authors='Patrick Lencioni')
        with Section(class_names=['links']):
            H1('Leadership')
            link('book', 'Turn the Ship Around!: A True Story of Turning Followers into Leaders', 'https://www.amazon.com/gp/product/B00AFPVP0Y', authors='L David Marquet')
            link('book', 'The Four Obsessions of an Extraordinary Executive: A Leadership Fable', 'https://www.amazon.com/gp/product/B003WUYQOQ', authors='Patrick Lencioni')
        with Section(class_names=['links']):
            H1('Theoretical')
            link('book', 'Measuring and Managing Performance in Organizations', 'https://www.amazon.com/gp/product/B00DY3KQX6', authors='Robert D Austin')
            link('book', "Don't Shoot the Dog: The Art of Teaching and Training", 'https://www.amazon.com/Dont-Shoot-Dog-Teaching-Training/dp/1982106468', authors='Karen Pryor')

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
                # TODO: handle runs of tags and text in phrasing content
            with P():
                Text('I have my own unpolished')
                A('https://github.com/donmccaughey/hashtable', 'hashtable for C')
                Text("""
                    and I enjoy collecting links to other implementations, hashing
                    functions and related articles.
                """)
        with Section(class_names=['links']):
            H1('Hashtable Implementations')
            link('repo', 'uthash: C macros for hash tables and more', 'https://github.com/troydhanson/uthash')
        with Section(class_names=['links']):
            H1('Hashing Functions')
            link('site', 'FNV Hash', 'http://www.isthe.com/chongo/tech/comp/fnv/index.html', authors='Landon Curt Noll', date='2017-04-29')
        with Section(class_names=['links']):
            H1('Hashing')
            link('blog', 'Advanced techniques to implement fast hash tables', 'https://attractivechaos.wordpress.com/2018/10/01/advanced-techniques-to-implement-fast-hash-tables/', date='2018-10-01')
            link('blog', 'A Probing Hash Table Framework', 'https://skystrife.github.io/blog/2016/01/29/a-probing-hash-table-framework/', authors='Chase Geigle', date='2016-01-29')
            link('blog', 'Best hash table for C', 'https://www.reddit.com/r/C_Programming/comments/3533bw/best_hash_table_for_c/', authors='Reddit', date='2015-05-06')
            link('blog', "Types Don't Know #", 'https://isocpp.org/files/papers/n3980.html', authors='Howard E. Hinnant, Vinnie Falco and John Bytheway', date='2014-05-24')
            link('blog', 'Dynamic Hash Tables', 'https://www.csd.uoc.gr/~hy460/pdf/Dynamic%20Hash%20Tables.pdf', authors='Per-Åke Larson', date='1988-04')

    with IndexPage('macOS Packages', has_files=True):
        with Section(class_names=['overview']):
            H1('Signed macOS Installer Packages')
            with P():
                Text('These standard macOS installer packages are built using')
                Code('pkgbuild')
                Text(' and ')
                Code('productbuild')
                Text('and are signed with my Apple developer credentials.')
            P("""
                This is a collection of command line tools that I've found useful
                at one time or another over the years. Some of them are widely 
                used but excluded from macOS and Xcode due to GPL 
                licenses.            
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
                Text('Make is old. It was')
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
                Text("""
                    , where the vertices are files and the edges are build scripts, then 
                    you can use Make effectively.  Even after many years, I still
                    sometimes forget this in both obvious and subtle ways while using
                    Make.
                """)
        with Section(class_names=['links']):
            H1('Books')
            link('book', 'Managing Projects with GNU Make', 'https://www.amazon.com/Managing-Projects-GNU-Make-Handbooks/dp/0596006101', authors='Robert Mecklenburg', date='2004')
            link('book', 'The GNU Make Book', 'https://nostarch.com/gnumake', authors='John Graham-Cumming', date='2015')
            link('book', 'The GNU Make Manual', 'https://www.gnu.org/software/make/manual/html_node/index.html', date='2016')
        with Section(class_names=['links']):
            H1('Articles')
            link('blog', 'Notes for new Make users', 'http://gromnitsky.users.sourceforge.net/articles/notes-for-new-make-users/', authors='Alexander Gromnitsky', date='2019-03-09')
            link('blog', 'make.mad-scientist.net', 'http://make.mad-scientist.net', authors='Paul D Smith', date='2017-07-30')
            link('blog', 'Notes on Writing Makefiles', 'http://eigenstate.org/notes/makefiles', authors='Ori Bernstein')
            link('blog', 'Self-Documented Makefile', 'http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html', authors='François Zaninotto', date='2016-02-29')

    with IndexPage('Memory Match', has_files=True) as page:
        page.add_script('https://cdnjs.cloudflare.com/ajax/libs/cash/1.3.0/cash.min.js')
        page.add_script('memory_match.js', charset='utf-8')
        Div(id='memory_match')

    with IndexPage('Random Words', has_files=True) as page:
        page.add_stylesheet('random_words.css')
        page.add_script('random_words.js', charset='utf-8')
        with Section(class_names=['overview']):
            H1('Random Words')
            P("""
                <em>Random Words</em> is a small program that chooses random
                entries from <a href=https://github.com/elasticdog/yawl>YAWL</a>, 
                a public domain list of 264,097 English words.
             """)
        with Section(class_names=['generator']):
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
            P(id='random_words')
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

    IndexPage('Rust and Wasm')
    with IndexPage('Science Fiction'):
        Page('Alastair Reynolds')
        Page('Iain M Banks')
        Page('James SA Corey')
        Page('Lois McMaster Bujold')

if __name__ == '__main__':
    root.find_files('../wwwroot')
    root.generate('../tmp', is_dry_run=False, overwrite=True)
