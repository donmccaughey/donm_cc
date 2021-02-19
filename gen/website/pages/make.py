from markup import Section, H1, P, Text, A, Ul
from resources import IndexPage
from website.links import link


def make():
    with IndexPage('Make'):
        with Section(class_names=['overview']):
            H1('Make: a Tool for Building Software')
            with P():
                Text('Make is old. It was ')
                A('https://en.wikipedia.org/wiki/Make_(software)',
                  'first released')
                Text("""
                    in 1977.  It's ubiquitous.  Make is a
                """)
                A(
                    'http://pubs.opengroup.org/onlinepubs/009695399/utilities/make.html',
                    'standard')
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
                A('https://en.wikipedia.org/wiki/Directed_acyclic_graph',
                  'directed acyclic graph')
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
                link('book', 'Managing Projects with GNU Make',
                     'https://www.amazon.com/Managing-Projects-GNU-Make-Handbooks/dp/0596006101',
                     authors='Robert Mecklenburg', date='2004')
                link('book', 'The GNU Make Book',
                     'https://nostarch.com/gnumake',
                     authors='John Graham-Cumming', date='2015')
                link('book', 'The GNU Make Manual',
                     'https://www.gnu.org/software/make/manual/html_node/index.html',
                     date='2016')
        with Section(class_names=['links']):
            H1('Articles')
            with Ul():
                link('blog', 'Notes for new Make users',
                     'http://gromnitsky.users.sourceforge.net/articles/notes-for-new-make-users/',
                     authors='Alexander Gromnitsky', date='2019-03-09')
                link('blog', 'make.mad-scientist.net',
                     'http://make.mad-scientist.net', authors='Paul D Smith',
                     date='2017-07-30')
                link('blog', 'Notes on Writing Makefiles',
                     'http://eigenstate.org/notes/makefiles',
                     authors='Ori Bernstein')
                link('blog', 'Self-Documented Makefile',
                     'http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html',
                     authors='François Zaninotto', date='2016-02-29')