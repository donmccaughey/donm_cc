from markup import Section, H1, P, Ul, Li, A, Img, Strong


def package(
        name: str,
        version: str,
        package: str,
        source: str,
        project: str,
        description: str,
):
    with Section(class_names=['package']):
        H1(f'{name} {version}')
        P(description)
        with Ul(class_names=['collection']):
            with Li(class_names=['item']):
                with A(package):
                    Img('./package-32x32.png', 'package icon', class_names=['favicon'])
                    Strong('package')
            with Li(class_names=['item']):
                with A(source):
                    Img('./source-32x32.png', 'source icon', class_names=['favicon'])
                    Strong('source')
            with Li(class_names=['item']):
                with A(project):
                    Img('./project-32x32.png', 'project icon', class_names=['favicon'])
                    Strong('project')
