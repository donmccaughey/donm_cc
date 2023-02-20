from markup import FigCaption, Figure, Img
from resources import Directory, Page
from website.figures import banner


def aughey():
    with Directory('aughey'):
        with Page('Don McCaughey', name='index'):
            banner(
                image='/aughey/handstand.jpg',
                width=600, height=800,
                description='Don doing a handstand',
                caption='Coachella Festival, Spring 2007',
                position='upper'
            )
