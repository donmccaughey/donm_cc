from markup import Section, H1, P, Ul
from resources import Directory, Page
from website.links import book


def business_novels():
    with Directory('business_novels', has_files=False):
        with Page('Business Novels', name='index'):
            with Section(class_names=['overview']):
                H1('Business Novels')
                P()
            with Section(class_names=['links']):
                H1('Recommended')
                with Ul():
                    book('The Goal',
                         'https://www.amazon.com/Goal-Process-Ongoing-Improvement-ebook/dp/B002LHRM2O',
                         authors='Eliyahu M Goldratt and Jeff Cox', date='1984',
                         checked=True)
                    book('The Phoenix Project',
                         'https://www.amazon.com/Phoenix-Project-DevOps-Helping-Business-ebook/dp/B078Y98RG8',
                         authors='Gene Kim, Kevin Behr and George Spafford',
                         date='2018', checked=True)
                    book('The Unicorn Project',
                         'https://www.amazon.com/Unicorn-Project-Developers-Disruption-Thriving-ebook/dp/B07QT9QR41',
                         authors='Gene Kim', date='2019', checked=True)
                    book('The Ideal Team Player',
                         'https://www.amazon.com/Ideal-Team-Player-Recognize-Cultivate-ebook/dp/B01B6AEJJ0',
                         authors='Patrick Lencioni', date='2016', checked=True)
                    book('The Five Dysfunctions of a Team',
                         'https://www.amazon.com/Five-Dysfunctions-Team-Leadership-Lencioni-ebook/dp/B006960LQW',
                         authors='Patrick Lencioni', date='2011', checked=True)
                    book('The Four Obsessions of an Extraordinary Executive',
                         'https://www.amazon.com/Four-Obsessions-Extraordinary-Executive-Leadership-ebook/dp/B003WUYQOQ',
                         authors='Patrick Lencioni', date='2008', checked=True)
            with Section(class_names=['links']):
                H1('Your Mileage May Vary')
                with Ul():
                    book('The Five Temptations of a CEO',
                         'https://www.amazon.com/Five-Temptations-CEO-10th-Anniversary-ebook/dp/B0062OAEWM',
                         authors='Patrick Lencioni', date='2008', checked=True)
                    book('Critical Chain',
                         'https://www.amazon.com/Critical-Chain-Business-Eliyahu-Goldratt-ebook/dp/B002LHRM2E',
                         authors='Eliyahu M Goldratt', date='1997', checked=True)
            with Section(class_names=['links']):
                H1('On My Readling List')
                with Ul():
                    book('The Deadline: A Novel About Project Management',
                         'https://www.amazon.com/Deadline-Novel-About-Project-Management-ebook/dp/B006MN4RAS',
                         authors='Tom DeMarco', date='2011')
                    book('How To Destroy A Tech Startup In Three Easy Steps',
                         'https://www.amazon.com/Destroy-Tech-Startup-Three-Steps-ebook/dp/B0772FJQ1T',
                         authors='Lawrence Krubner', date='2017', checked=True)
            with Section(class_names=['links']):
                H1('Business Comics')
                with Ul():
                    book('The Adventures of Johnny Bunko',
                         'https://www.amazon.com/Adventures-Johnny-Bunko-Career-Guide-ebook/dp/B0015DRPL8',
                         authors='Daniel H Pink and Reb Ten Pas', date='2008',
                         checked=True)
                    book("What Got You Here Won't Get You There",
                         'https://www.amazon.com/What-Here-There-illustrated-version-ebook/dp/B00710YFJY',
                         authors='Marshall Goldsmith, Mark Reiter and Shane Clester',
                         date='2011', checked=True)