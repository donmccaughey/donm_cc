from markdown import inline_markdown_to_markup
from markup import Section, H1, P, Ul, Li, A, Img, Strong, Text


def package(
        name: str,
        version: str,
        package: str,
        source: str,
        project: str,
        description: str, # markdown
):
    with Section(class_names=['package']):
        H1(f'{name} {version}')
        with P():
            inline_markdown_to_markup(description)
        with Ul():
            with Li(class_names=['installer']):
                with A(package):
                    Strong(f'{name} {version} installer package')
            with Li():
                with A(source):
                    inline_markdown_to_markup(f'build script for the **{name}** installer package')
            with Li():
                with A(project):
                    Strong(name)
                    Text(' project website')
