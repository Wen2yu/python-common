from entity import BaseObj


class CodeItem(BaseObj):

    def __init__(self, code, desc, **kwargs):
        super().__init__(**kwargs)
        self.code = code
        self.desc = desc
