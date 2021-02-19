from markup import Section, H1, P, A, Text, Ul
from resources import IndexPage
from website.links import link


def hashtables():
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
                A('https://en.cppreference.com/w/cpp/container/unordered_map',
                  'C++ 11')
                Text(').')
            with P():
                Text('I have my own unpolished ')
                A('https://github.com/donmccaughey/hashtable',
                  'hashtable for C')
                Text("""
                    and I enjoy collecting links to other implementations, hashing
                    functions and related articles.
                """)
        with Section(class_names=['links']):
            H1('Hashtable Implementations')
            with Ul():
                link('repo', 'uthash: C macros for hash tables and more',
                     'https://github.com/troydhanson/uthash')
        with Section(class_names=['links']):
            H1('Hashing Functions')
            with Ul():
                link('site', 'FNV Hash',
                     'http://www.isthe.com/chongo/tech/comp/fnv/index.html',
                     authors='Landon Curt Noll', date='2017-04-29')
        with Section(class_names=['links']):
            H1('Hashing')
            with Ul():
                link('blog',
                     'Advanced techniques to implement fast hash tables',
                     'https://attractivechaos.wordpress.com/2018/10/01/advanced-techniques-to-implement-fast-hash-tables/',
                     date='2018-10-01')
                link('blog', 'A Probing Hash Table Framework',
                     'https://skystrife.github.io/blog/2016/01/29/a-probing-hash-table-framework/',
                     authors='Chase Geigle', date='2016-01-29')
                link('blog', 'Best hash table for C',
                     'https://www.reddit.com/r/C_Programming/comments/3533bw/best_hash_table_for_c/',
                     authors='Reddit', date='2015-05-06')
                link('blog', "Types Don't Know #",
                     'https://isocpp.org/files/papers/n3980.html',
                     authors='Howard E. Hinnant, Vinnie Falco and John Bytheway',
                     date='2014-05-24')
                link('blog', 'Dynamic Hash Tables',
                     'https://www.csd.uoc.gr/~hy460/pdf/Dynamic%20Hash%20Tables.pdf',
                     authors='Per-Åke Larson', date='1988-04')