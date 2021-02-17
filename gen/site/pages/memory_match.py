from markup import Div
from resources import IndexPage


def memory_match():
    global page
    with IndexPage('Memory Match', has_files=True) as page:
        page.add_script(
            'https://cdnjs.cloudflare.com/ajax/libs/cash/1.3.0/cash.min.js')
        page.add_script('memory_match.js')
        Div(id='memory_match')