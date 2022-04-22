from tinycss2 import parse_stylesheet


class CSS:
    def __init__(self, path: str):
        with open(path, 'r') as f:
            self.source = f.read()
        self.rules = parse_stylesheet(
            self.source, skip_comments=True, skip_whitespace=True
        )

    def __str__(self):
        serialized_rules = [rule.serialize() for rule in self.rules]
        return '\n'.join(serialized_rules)
