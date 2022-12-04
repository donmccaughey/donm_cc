from markup import FigCaption, Figure, Img


def banner(image: str, description: str, caption: str, position: str):
    with Figure(class_names=['banner']):
        if 'upper' == position:
            FigCaption(class_names=['upper-right'], text=caption)
        Img(src=image, alt=description)
        if 'lower' == position:
            FigCaption(class_names=['lower-right'], text=caption)
