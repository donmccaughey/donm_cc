from markup import Div, Img, Br, Span
from resources import IndexPage


def aughey():
    with IndexPage('Don McCaughey', name='aughey', has_files=True):
        with Div(class_names=['banner']):
            Img(src='/aughey/handstand.jpg', alt='Don doing a handstand')
            Br()
            Span(class_names=['caption'],
                 text='Coachella Festival, spring 2007')