import os


class Component:
    def __init__(self, type: int, disabled=None, style=None, label=None, emoji=None, url=None, options=None,
                 placeholder=None, min_values=None, max_values=None, custom_id=None):
        self.type = type
        self.disabled = disabled
        self.style = style
        self.label = label
        self.emoji = emoji
        self.url = url
        self.options = options
        self.placeholder = placeholder
        self.min_values = min_values
        self.max_values = max_values
        self.custom_id = custom_id

        if self.custom_id is None and self.url is None:
            self.custom_id = os.urandom(16).hex()

    def _to_dict(self):
        return {k: v for k, v in self.__dict__.items() if v is not None}


class View:
    def __init__(self, *components: Component):
        self.components = components

    def _to_dict(self):
        return {"type": 1, "components": [component._to_dict() for component in self.components]}
