from markup import Div
from resources import Directory, Page


def memory_match():
    with Directory('memory_match'):
        with Page('Memory Match', name='index') as page:
            page.add_script(
                'https://cdnjs.cloudflare.com/ajax/libs/cash/1.3.0/cash.min.js')
            page.add_script('memory_match.js')
            Div(id='memory_match')