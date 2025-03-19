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
                    'linkedin': 'https://www.linkedin.com/in/donmccaughey/',
                })
                contact_info({
                    'don@donm.cc': 'mailto:don@donm.cc',
                })
                P('''
                    I'm a software engineer with strong technical, leadership 
                    and organizational skills.  I build high performing, 
                    collaborative, cross-functional teams that focus on
                    sustained, predictable delivery of value to customers.
                ''')
            with Section(class_names=['experience']):
                H1('Selected Experience')
                with Section(class_names=['organization']):
                    H2('United States Digital Service')
                    organization_details('Remote', '2023', '2025',
                                         ['Digital Services Expert'])
                    with P():
                        Text('''
                            The United States Digital Service (USDS) helped
                            agencies across the federal government build and
                            improve their software systems, delivering a better
                            government experience to millions of people.
                        ''')
                    with P():
                        inline_markdown_to_markup('''
                            At USDS I was detailed to the Office of the CTO
                            (OCTO) at the Department of Veterans Affairs (VA),
                            where I was the lead engineer for the
                            [VA: Health and Benefits](https://mobile.va.gov/app/va-health-and-benefits)
                            mobile app.
                        ''')
                        with Ul():
                            Li('''
                                Engineering leader for a thirty person mobile
                                development team.
                            ''')
                            Li('''
                                Shipped a high quality release every two weeks
                                used by over one million veterans monthly.
                            ''')
                            Li('''
                                Worked closely with health, benefits and digital
                                experience teams to ship new mobile features.
                            ''')
                            Li('''
                                Helped develop and run a lightweight engineering
                                review for fifty contract teams building on
                                VA.gov, spotting problems or omissions in 75% of
                                projects.
                            ''')
                with Section(class_names=['organization']):
                    H2('Cruise')
                    organization_details('San Francisco, CA', '2022', '2023',
                                         ['Staff Software Engineer'])
                    with P():
                        Text('''
                            I worked on cloud services for managing Cruise's
                            fleet of autonomous vehicles.
                        ''')
                        with Ul():
                            Li('''
                                Drove efforts to improve engineering culture and
                                standards.
                            ''')
                            Li('''
                                On-boarded and mentored new engineers as the
                                team doubled in size.
                            ''')
                            Li('''
                                Helped get a complex cross-functional
                                integration effort back on track.
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
                                Guided delivery of public SDKs, SSO, internal
                                tools and partner integrations.
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
                                Quadrupled web app release rate by improving the
                                release process.
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
                                customer='Facebook, Skype, Pivotal Labs',
                                date='2011',
                                summary='Skype app for unreleased phone',
                                description='''
                                    Created a Skype client for a mobile OS built
                                    on an Android core.  Worked with Skype and
                                    Facebook engineers to integrate the Skype
                                    client library with the phone's custom UI
                                    toolkit built atop HTML, CSS and JavaScript.
                                '''
                            )
                            project(
                                customer='BMW',
                                date='2009-2010',
                                summary='first iPhone integration for the [BMW Mini](https://apps.apple.com/us/app/id1519458349)',
                                description='''
                                    Designed and implemented a unique proxy to
                                    direct HTTP connections from the app to the
                                    [automotive head unit](https://en.wikipedia.org/wiki/Automotive_head_unit)
                                    over the phone's 30 pin connector.  Worked
                                    with embedded engineers to design a
                                    communication protocol.  Built tools in C++
                                    to diagnose intermittent data corruption.
                                    Implemented simple flow control to work
                                    around deficiencies in the underlying
                                    [iAP protocol](https://en.wikipedia.org/wiki/List_of_Bluetooth_profiles#iPod_Accessory_Protocol_(iAP)).
                                '''
                            )

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
