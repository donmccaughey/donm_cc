from markup import Section, H1, P, Text, Code
from resources import Directory, Page
from website.packages import package


def macos_packages():
    with Directory('macos_packages'):
        with Page('macOS Packages', name='index') as page:
            page.add_stylesheet('macos_packages.css')
            with Section(class_names=['overview']):
                H1('Signed and Notarized Universal macOS Installer Packages')
                with P():
                    Text('These standard macOS installer packages are built using ')
                    Code('pkgbuild')
                    Text(' and ')
                    Code('productbuild')
                    Text(' and are signed and notarized with my Apple developer credentials.')
                    Text(' They install universal binaries that will run on both Intel and Apple Silicon Macs.')
                P("""
                    This is a collection of command line tools that I've found useful
                    at one time or another over the years. Some of them are widely used
                    but excluded from macOS and Xcode due to GPL licenses.            
                """)
            package(
                name='FLAC',
                version='1.5.0',
                package='https://github.com/donmccaughey/flac_pkg/releases/download/v1.5.0-r1/flac-1.5.0.pkg',
                source='https://github.com/donmccaughey/flac_pkg',
                project='https://xiph.org/flac/',
                description='A fast and widely supported lossless audio codec.'
            )
            package(
                name='jq',
                version='1.7.1',
                package='https://github.com/donmccaughey/jq_pkg/releases/download/v1.7.1-r1/jq-1.7.1.pkg',
                source='https://github.com/donmccaughey/jq_pkg',
                project='https://jqlang.github.io/jq/',
                description='A lightweight and flexible command line JSON processor.'
            )
            package(
                name='nginx',
                version='1.24.0',
                package='https://github.com/donmccaughey/nginx_pkg/releases/download/v1.24.0-r2/nginx-1.24.0-r2.pkg',
                source='https://github.com/donmccaughey/nginx_pkg',
                project='https://nginx.org',
                description='A widely used and capable HTTP and proxy server.'
            )
            package(
                name='pkg-config',
                version='0.29.2',
                package='https://github.com/donmccaughey/pkg-config_pkg/releases/download/v0.29.2-r4/pkg-config-0.29.2-r4.pkg',
                source='https://github.com/donmccaughey/pkg-config_pkg',
                project='https://www.freedesktop.org/wiki/Software/pkg-config/',
                description='A helper tool used when compiling applications and libraries.'
            )
            package(
                name='tree',
                version='2.1.1',
                package='https://github.com/donmccaughey/tree_pkg/releases/download/v2.1.1-r1/tree-2.1.1.pkg',
                source='https://github.com/donmccaughey/tree_pkg',
                project='http://oldmanprogrammer.net/source.php?dir=projects/tree',
                description='A recursive directory listing command.'
            )
            package(
                name='wget',
                version='1.21.5',
                package='https://github.com/donmccaughey/wget_pkg/releases/download/v1.21.5-r1/wget-1.21.5.pkg',
                source='https://github.com/donmccaughey/wget_pkg',
                project='https://www.gnu.org/software/wget/',
                description='A command line tool for retrieving files using HTTP, HTTPS, FTP and FTPS.'
            )
            package(
                name='XZ Utils',
                version='5.4.5',
                package='https://github.com/donmccaughey/xz_pkg/releases/download/v5.4.5-r1/xz-5.4.5.pkg',
                source='https://github.com/donmccaughey/xz_pkg',
                project='https://tukaani.org/xz/',
                description='A general purpose data compression tool and library, and includes the `xz` command line tool.'
            )
