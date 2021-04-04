from markup import Section, H1, P, Text, Code
from resources import Directory, Page
from website.packages import package


def macos_packages():
    with Directory('macos_packages'):
        with Page('macOS Packages', name='index'):
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