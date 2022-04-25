import re
from collections import defaultdict
from functools import reduce
from typing import Optional, Tuple, List

from tinycss2 import parse_stylesheet
from tinycss2.ast import IdentToken, LiteralToken, AtRule, ParenthesesBlock, \
    WhitespaceToken, HashToken, QualifiedRule, Node


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
        self.rules = merge_media_queries(self.rules)
        # TODO: detect duplicate rules
        self.rules.sort(key=lambda r: r.sort_key())

    def __add__(self, other) -> 'CSS':
        rules = self.rules + other.rules
        return CSS(rules=rules)

    def __repr__(self) -> str:
        if self.path:
            return f'CSS file {self.path} ({len(self.rules)} rules)'
        else:
            return f'CSS file ({len(self.rules)} rules)'

    def __str__(self) -> str:
        serialized_rules = [rule.serialize() for rule in self.rules]
        return '\n'.join(serialized_rules)

    @staticmethod
    def is_media_query(node) -> bool:
        return isinstance(node, AtRule) and node.at_keyword == 'media'

    @staticmethod
    def is_rule(node) -> bool:
        return isinstance(node, QualifiedRule)


class Rule:
    def __init__(self, qualified_rule: QualifiedRule):
        self.qualified_rule = qualified_rule
        self.selector = Selector(self.qualified_rule.prelude)

    def __repr__(self) -> str:
        return f'Rule "{self.selector}"'

    def __str__(self) -> str:
        return self.serialize()

    def is_class_rule(self) -> bool:
        return (
            isinstance(self.qualified_rule.prelude[0], LiteralToken)
            and self.qualified_rule.prelude[0].value == '.'
        )

    def is_element_rule(self) -> bool:
        return (
            isinstance(self.qualified_rule.prelude[0], IdentToken)
            and self.qualified_rule.prelude[0].value[0].isalpha()
        )

    def is_id_rule(self) -> bool:
        return isinstance(self.qualified_rule.prelude[0], HashToken)

    def serialize(self) -> str:
        return self.qualified_rule.serialize()

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
    def __init__(self, at_rule: AtRule):
        self.at_rule = at_rule
        self.expression = Expression(at_rule.prelude)

    def __add__(self, other) -> 'MediaQuery':
        content = list(self.at_rule.content)
        content.extend(other.at_rule.content)
        at_rule = AtRule(
            self.at_rule.source_line,
            self.at_rule.source_column,
            self.at_rule.at_keyword,
            self.at_rule.lower_at_keyword,
            list(self.at_rule.prelude),
            content
        )
        return MediaQuery(at_rule)

    def __eq__(self, other) -> bool:
        return self.expression == other.expression

    def __repr__(self) -> str:
        return f'MediaQuery "{self.expression}"'

    def __str__(self) -> str:
        return self.serialize()

    def remove_blank_lines(self):
        def is_last(i: int):
            return i == len(self.at_rule.content) - 1

        content = []
        for i in range(len(self.at_rule.content)):
            node = self.at_rule.content[i]
            if isinstance(node, WhitespaceToken):
                if node.value == '\n':
                    if not is_last(i):
                        continue
                else:
                    node.value = re.sub('\n+', '\n', node.value)
            content.append(node)
        self.at_rule.content = content

    def serialize(self) -> str:
        return self.at_rule.serialize()

    def sort_key(self) -> Tuple[int, str]:
        return MEDIA_QUERY, str(self.expression)


class Expression:
    def __init__(self, components: List[Node]):
        self.components = components
        self.name = components_name(components)

    def __eq__(self, other) -> bool:
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)

    def __repr__(self) -> str:
        return f'Expression "{self.name}"'

    def __str__(self) -> str:
        return self.name


class UnrecognizedRule:
    def __init__(self, node: Node):
        self.node = node
        self.name = repr(node)

    def __repr__(self) -> str:
        return f'UnrecognizedRule: "{self.name}"'

    def __str__(self) -> str:
        return self.serialize()

    def serialize(self) -> str:
        return self.node.serialize()

    def sort_key(self) -> Tuple[int, str]:
        return UNRECOGNIZED_RULE, self.name


def components_name(components: List[Node]) -> str:
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


def merge_media_queries(rules: List) -> List:
    media_queries = []
    everything_else = []
    for rule in rules:
        if isinstance(rule, MediaQuery):
            media_queries.append(rule)
        else:
            everything_else.append(rule)

    grouped_queries = defaultdict(list)
    for media_query in media_queries:
        grouped_queries[media_query.expression].append(media_query)

    media_queries = []
    for group in grouped_queries.values():
        media_query = reduce(lambda a, b: a + b, group)
        media_query.remove_blank_lines()
        media_queries.append(media_query)

    return everything_else + media_queries
