from typing import Optional, List, Tuple

from tinycss2 import parse_stylesheet
from tinycss2.ast import IdentToken, LiteralToken, AtRule, ParenthesesBlock, WhitespaceToken, HashToken, QualifiedRule


UNRECOGNIZED_RULE = 0
ELEMENT_RULE = 1
CLASS_RULE = 2
ID_RULE = 3
MEDIA_QUERY = 4


class CSS:
    def __init__(self, path: Optional[str] = None, rules: Optional[list] = None):
        if path:
            self.path = path
            with open(path, 'r') as f:
                self.source = f.read()
            nodes = parse_stylesheet(
                self.source, skip_comments=True, skip_whitespace=True
            )
            self.rules = []
            for node in nodes:
                if CSS.is_rule(node):
                    self.rules.append(Rule(node))
                elif CSS.is_media_query(node):
                    self.rules.append(MediaQuery(node))
                else:
                    self.rules.append(UnrecognizedRule(node))
        elif rules:
            self.rules = list(rules)
        else:
            self.rules = []
        self.rules.sort(key=lambda r: r.sort_key())
        # TODO: merge identical media queries
        # TODO: detect duplicate rules

    def __repr__(self):
        if self.path:
            return f'CSS file {self.path} ({len(self.rules)} rules)'
        else:
            return f'CSS file ({len(self.rules)} rules)'

    def __str__(self):
        serialized_rules = [rule.serialize() for rule in self.rules]
        return '\n'.join(serialized_rules)

    def __add__(self, other):
        rules = self.rules + other.rules
        return CSS(rules=rules)

    @staticmethod
    def is_media_query(node) -> bool:
        return isinstance(node, AtRule) and node.at_keyword == 'media'

    @staticmethod
    def is_rule(node) -> bool:
        return isinstance(node, QualifiedRule)


class Rule:
    def __init__(self, node):
        self.node = node
        self.selector = Selector(self.node.prelude)

    def __str__(self) -> str:
        return self.serialize()

    def is_class_rule(self) -> bool:
        return (
            isinstance(self.node, QualifiedRule)
            and isinstance(self.node.prelude[0], LiteralToken)
            and self.node.prelude[0].value == '.'
        )

    def is_element_rule(self) -> bool:
        return (
            isinstance(self.node, QualifiedRule)
            and isinstance(self.node.prelude[0], IdentToken)
            and self.node.prelude[0].value[0].isalpha()
        )

    def is_id_rule(self) -> bool:
        return (
            isinstance(self.node, QualifiedRule)
            and isinstance(self.node.prelude[0], HashToken)
        )

    def serialize(self) -> str:
        return self.node.serialize()

    def sort_key(self) -> Tuple[int, str]:
        if self.is_element_rule():
            return ELEMENT_RULE, str(self.selector)
        if self.is_id_rule():
            return ID_RULE, str(self.selector)
        if self.is_class_rule():
            return CLASS_RULE, str(self.selector)
        return 0, str(self.selector)


class Selector:
    def __init__(self, components):
        self.components = components
        self.name = components_name(components)

    def __repr__(self) -> str:
        return f'Selector "{self.name}"'

    def __str__(self) -> str:
        return self.name


class MediaQuery:
    def __init__(self, node):
        self.node = node
        self.name = Expression(node.prelude)

    def __str__(self) -> str:
        return self.serialize()

    def serialize(self) -> str:
        return self.node.serialize()

    def sort_key(self) -> Tuple[int, str]:
        return MEDIA_QUERY, str(self.name)


class Expression:
    def __init__(self, components):
        self.components = components
        self.name = components_name(components)

    def __repr__(self) -> str:
        return f'Expression "{self.name}"'

    def __str__(self) -> str:
        return self.name


class UnrecognizedRule:
    def __init__(self, node):
        self.node = node
        self.name = repr(node)

    def __str__(self) -> str:
        return self.serialize()

    def serialize(self) -> str:
        return self.node.serialize()

    def sort_key(self) -> Tuple[int, str]:
        return UNRECOGNIZED_RULE, self.name


def components_name(components) -> str:
    components = list(components)
    while isinstance(components[0], WhitespaceToken):
        del components[0]
    while isinstance(components[-1], WhitespaceToken):
        del components[-1]

    name = ''
    for component in components:
        match component:
            case HashToken():
                name += '#'
                name += component.value
            case IdentToken():
                name += component.lower_value
            case LiteralToken():
                name += component.value
            case ParenthesesBlock():
                name += components_name(component.content)
            case WhitespaceToken():
                name += ' '
            case _:
                print(f'Unrecognized component {component}')
    return name
