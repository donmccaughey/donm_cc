

class NameMixin:
    def __init__(self, name:str, **kwargs):
        super().__init__(**kwargs)
        self.name = name
