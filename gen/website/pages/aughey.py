from markup import Div, Img, Br, Span
from resources import Directory, Page


def aughey():
    with Directory('aughey', has_files=True):
        with Page('Don McCaughey', name='index'):
            with Div(class_names=['banner']):
                Img(src='/aughey/handstand.jpg', alt='Don doing a handstand')
                Br()
                Span(class_names=['caption'],
                     text='Coachella Festival, spring 2007')