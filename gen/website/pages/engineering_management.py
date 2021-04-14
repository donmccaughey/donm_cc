from markup import Section, H1, P, Ul
from resources import Directory, Page
from website.links import link


def engineering_management():
    with Directory('engineering_management', has_files=False):
        with Page('Engineering Management', name='index'):
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
                    link('podcast', 'Manager Tools "Basics"',
                         'https://www.manager-tools.com/manager-tools-basics',
                         authors=['Michael Auzenne', 'Mark Horstman'], date='2005')
                    link('book',
                         'Crucial Conversations: Tools for Talking When Stakes Are High',
                         'https://www.amazon.com/gp/product/B005K0AYH4',
                         authors=['Kerry Patterson', 'Joseph Grenny', 'Ron McMillan', 'Al Switzler'],
                         date='2011')
                    link('book',
                         'Crucial Accountability: Tools for Resolving Violated Expectations, Broken Commitments and Bad Behavior',
                         'https://www.amazon.com/Crucial-Accountability-Resolving-Expectations-Commitments-ebook/dp/B00C4BDRW6',
                         authors=['Kerry Patterson', 'Joseph Grenny', 'Ron McMillan', 'Al Switzler'],
                         date='2013')
                    link('blog', 'Ask a Manager', 'https://www.askamanager.org',
                         authors=['Alison Green'])
            with Section(class_names=['links']):
                H1('Engineering Management')
                with Ul():
                    link('email',
                         'Software Lead Weekly: A weekly email for busy people who care about people, culture and leadership',
                         'http://softwareleadweekly.com', authors=['Oren Ellenbogen'])
                    link('book',
                         "The Manager's Path: A Guide for Tech Leaders Navigating Growth and Change",
                         'https://www.amazon.com/gp/product/B06XP3GJ7F',
                         authors=['Camille Fournier'], date='2017')
                    link('blog', 'Irrational Exuberance!', 'https://lethain.com',
                         authors=['Will Larson'])
            with Section(class_names=['links']):
                H1('Teamwork')
                with Ul():
                    link('book',
                         'The Five Dysfunctions of a Team: A Leadership Fable',
                         'https://www.amazon.com/gp/product/B006960LQW',
                         authors=['Patrick Lencioni'], date='2011')
                    link('book',
                         'The Ideal Team Player: How to Recognize and Cultivate the Three Essential Virtues',
                         'https://www.amazon.com/Ideal-Team-Player-Recognize-Cultivate-ebook/dp/B01B6AEJJ0',
                         authors=['Patrick Lencioni'], date='2016')
            with Section(class_names=['links']):
                H1('Leadership')
                with Ul():
                    link('book',
                         'Turn the Ship Around!: A True Story of Turning Followers into Leaders',
                         'https://www.amazon.com/gp/product/B00AFPVP0Y',
                         authors=['L David Marquet'], date='2013')
                    link('book',
                         'The Four Obsessions of an Extraordinary Executive: A Leadership Fable',
                         'https://www.amazon.com/gp/product/B003WUYQOQ',
                         authors=['Patrick Lencioni'], date='2008')
            with Section(class_names=['links']):
                H1('Theoretical')
                with Ul():
                    link('book',
                         'Measuring and Managing Performance in Organizations',
                         'https://www.amazon.com/gp/product/B00DY3KQX6',
                         authors=['Robert D Austin'], date='1996')
                    link('book',
                         "Don't Shoot the Dog: The Art of Teaching and Training",
                         'https://www.amazon.com/Dont-Shoot-Dog-Teaching-Training/dp/1982106468',
                         authors=['Karen Pryor'], date='1984')