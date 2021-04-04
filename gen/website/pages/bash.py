from markup import Section, H1, P, Ul
from resources import Directory, Page
from website.links import link


def bash():
    with Directory('bash', has_files=False):
        with Page('Bash', name='index'):
            with Section(class_names=['overview']):
                H1('Bash: the "Bourne-again" shell')
                P()
            with Section(class_names=['links']):
                H1('Tips and Tricks')
                with Ul():
                    link('blog',
                         'Use the Unofficial Bash Strict Mode (Unless You Looove Debugging)',
                         'http://redsymbol.net/articles/unofficial-bash-strict-mode/',
                         authors='Aaron Maxwell')
                    link('blog', 'How to write idempotent Bash scripts',
                         'https://arslan.io/2019/07/03/how-to-write-idempotent-bash-scripts/',
                         authors='Fatih Arslan', date='2019-07-03')
                    link('blog', 'Shortcuts to Move Faster in Bash Command Line',
                         'http://teohm.github.io/blog/2012/01/04/shortcuts-to-move-faster-in-bash-command-line/',
                         authors='Huiming Teo', date='2012-01-04')