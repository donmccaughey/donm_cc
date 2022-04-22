from typing import Optional

from tinycss2 import parse_stylesheet


class CSS:
    def __init__(self, path: Optional[str] = None, rules: Optional[list] = None):
        if path:
            self.path = path
            with open(path, 'r') as f:
                self.source = f.read()
            self.rules = parse_stylesheet(
                self.source, skip_comments=True, skip_whitespace=True
            )
        else:
            self.rules = rules if rules else []

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
