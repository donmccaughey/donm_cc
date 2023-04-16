from markdown import inline_markdown_to_markup
from markup import A, Section, H1, P, Ul, Li, Text, H2, Br, Strong, Em, Aside, Address, Div
from resources import Directory, Page


def alternate_formats(format_links: dict[str, str]):
    with Aside():
        with Ul():
            for format, link in format_links.items():
                with Li():
                    A(link, format)


def contact_info(contact_links: dict[str, str]):
    with Address():
        with Ul():
            for contact, link in contact_links.items():
                with Li():
                    if link:
                        A(link, contact)
                    else:
                        Text(contact)


def organization_details(location: str, start_date: str, end_date: str, titles: list[str]):
    with Ul(class_names=['details']):
        Li(location)
        Li(f'{start_date} to {end_date}')
        Li(' → '.join(titles))


def project(customer: str, date: str, summary: str, description: str):
    with Li(class_names=['project']):
        Strong(customer)
        Text(f', {date} — ')
        with Em():
            inline_markdown_to_markup(summary)
        Br()
        inline_markdown_to_markup(description)


def resume():
    with Directory('resume'):
        with Page('Résumé', name='index') as page:
            page.add_stylesheet('resume.css')
            with Section(class_names=['overview']):
                H1('Résumé of Don McCaughey')
                alternate_formats({
                    'markdown': '/resume/Resume_of_Don_McCaughey.md',
                    'pdf': '/resume/Resume_of_Don_McCaughey.pdf',
                })
                contact_info({
                    'don@donm.cc': 'mailto:don@donm.cc',
                    'linkedin.com/in/donmccaughey': 'https://www.linkedin.com/in/donmccaughey/',
                    '+1 (415) 793-1166': 'tel:+1-415-793-1166',
                })
                P('''
                    I'm a software engineer with strong technical, leadership 
                    and organizational skills.  I build high performing, 
                    collaborative, cross-functional teams that focus on
                    sustained, regular delivery of value to customers.
                ''')
            with Section(class_names=['experience']):
                H1('Selected Experience')
                with Section(class_names=['organization']):
                    H2('Cruise')
                    organization_details('San Francisco, CA', '2022', 'present',
                                         ['Staff Software Engineer'])
                    with P():
                        Text('''
                            I joined the fleet management team supporting
                            Cruise's rapidly growing fleet of autonomous
                            vehicles.
                        ''')
                        with Ul():
                            Li('''
                                Worked on complex cross-functional integration
                                efforts to deliver automatic firmware updates
                                for Cruise's new Origin vehicle.
                            ''')
                            Li('''
                                Drove efforts to improve engineering culture and
                                standards.
                            ''')
                            Li('''
                                On-boarded and mentored new engineers as the
                                team doubled in size.
                            ''')
                with Section(class_names=['organization']):
                    H2('Truework')
                    organization_details('San Francisco, CA', '2019', '2021',
                                         ['Engineering Manager'])
                    with P():
                        Text('''
                            I was the first engineering manager at this early 
                            stage fintech startup.
                        ''')
                        with Ul():
                            Li('''
                                Established a fast and lightweight weekly 
                                planning and delivery cycle that increased 
                                engineering velocity and predictability.
                            ''')
                            Li('''
                                Doubled the team to 15 engineers, hiring across 
                                all experience levels.
                            ''')
                            Li('''
                                Guided delivery of key features, including
                                public SDKs, SSO, tools for 80+ person back
                                office team and payroll provider integrations.
                            ''')
                with Section(class_names=['organization']):
                    H2('Copper CRM')
                    organization_details('San Francisco, CA', '2016', '2019',
                                         ['Principal Software Engineer',
                                         'Engineering Manager',
                                         'Senior Engineering Manager'])
                    with P():
                        Text('''
                            I joined Copper as the sole developer for our native 
                            iOS app.  I became manager of the mobile team and 
                            later the infrastructure team.
                        ''')
                        with Ul():
                            Li('''
                                Established a regular release cadence and
                                shipped many new features.
                            ''')
                            Li('''
                                Grew the mobile team from two to six engineers 
                                and fostered a collaborative, cross-functional 
                                team culture.
                            ''')
                            Li('''
                                Doubled the rate of web app releases through a 
                                release improvement process.
                            ''')

                with Section(class_names=['organization']):
                    H2('Able Pear Software')
                    organization_details('Burlingame, CA', '2008', '2016',
                                         ['Founder and Principal Developer'])
                    with P():
                        Text('''
                            I ran a small software development firm focused on 
                            mobile apps.  Interesting projects included:
                        ''')
                        with Ul():
                            project(
                                customer='Square',
                                date='2012',
                                summary='iPad integration with point-of-sale (POS) hardware',
                                description='''
                                    Built an iOS library linking the Square POS 
                                    app with the Square Stand. Worked with the 
                                    app team and embedded software team to 
                                    create APIs and communication protocols. 
                                    Built engineering test applications.
                                '''
                            )
                            project(
                                customer='BMW',
                                date='2009-2010',
                                summary='first iPhone integration for the [BMW Mini](https://apps.apple.com/us/app/id1519458349)',
                                description='''
                                    Starting with BMW's prototype iPhone app
                                    that used HTTP to connect to the
                                    [automotive head unit](https://en.wikipedia.org/wiki/Automotive_head_unit),
                                    I designed and implemented a unique proxy
                                    to direct HTTP connections from the app to
                                    the head unit over the phone's 30 pin
                                    connector.  Worked with embedded engineers
                                    to design a communication protocol.  Built
                                    a C++ echo server running on the head unit
                                    to diagnose intermittent data corruption.
                                    Implemented simple flow control to work
                                    around deficiencies in the underlying
                                    [iAP protocol](https://en.wikipedia.org/wiki/List_of_Bluetooth_profiles#iPod_Accessory_Protocol_(iAP)).
                                '''
                            )

            with Section(class_names=['personal-projects']):
                H1('Personal Projects')
                with Ul():
                    with Li():
                        inline_markdown_to_markup('''
                            [News](https://news.donm.cc), a personal tech news
                            aggregator.
                        ''')
                    with Li():
                        inline_markdown_to_markup('''
                            [macOS Installer Packages](https://donm.cc/macos_packages/)
                            for missing Unix command line utilities.
                        ''')
                    with Li():
                        inline_markdown_to_markup('''
                            [Objective-C Tuesdays](https://donm.cc/objective-c_tuesdays/),
                            tutorials on the basics of C and Objective-C.
                        ''')
                    with Li():
                        inline_markdown_to_markup('''
                            [C-evo-X](https://github.com/donmccaughey/C-evo-x), 
                            maintainer of a Civilization-inspired Windows 
                            strategy game.
                        ''')

            with Section(class_names=['education']):
                H1('Education')
                with Ul():
                    with Li():
                        Strong('Stanford University')
                        Text('''
                            — One year of graduate study in mechanical 
                            engineering; focus in smart product design (ME 218).
                        ''')
                    with Li():
                        Strong('New Jersey Institute of Technology')
                        Text(' — BS, Mechanical Engineering.')
