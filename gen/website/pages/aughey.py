from markup import FigCaption, Figure, Img
from resources import Directory, Page
from website.figures import banner


def aughey():
    with Directory('aughey'):
        with Page('Don McCaughey', name='index'):
            banner(
                image='/aughey/Split-Rocker_by_Jeff_Koons_Glenstone_summer_2024.jpg',
                width=1024, height=768,
                description='A larger than life head of an animal covered in blooming flowers.',
                caption='Split-Rocker by Jeff Koons, Glenstone, summer 2024',
                position='upper'
            )
