import os
from typing import Optional, Tuple, Union

OptInt = Optional[int]
OptStr = Optional[str]


class Component:
    def __init__(
        self,
        type: int,
        disabled: bool = None,
        style: OptInt = None,
        label: OptStr = None,
        emoji: OptStr = None,
        url: OptStr = None,
        options: list = None,
        placeholder: OptStr = None,
        min_values: OptInt = None,
        max_values: OptInt = None,
        custom_id: OptStr = None,
    ):
        self.type: int = type
        self.disabled: bool = disabled
        self.style: OptInt = style
        self.label: OptStr = label
        self.emoji: OptStr = emoji
        self.url: OptStr = url
        self.options: list = options
        self.placeholder: OptStr = placeholder
        self.min_values: OptInt = min_values
        self.max_values: OptInt = max_values
        self.custom_id: Union[str, int] = custom_id

        if self.custom_id is None and self.url is None:
            self.custom_id = os.urandom(16).hex()

    def _to_dict(self):
        return {k: v for k, v in self.__dict__.items() if v is not None}


class View:
    def __init__(self, *components: Component):
        self.components: Tuple[Component] = components

    def _to_dict(self):
        return {
            "type": 1,
            "components": [component._to_dict() for component in self.components],
        }
