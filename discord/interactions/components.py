import os
from typing import Optional, Tuple, Union, Callable, Any

from discord.utils import maybe_await

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

    async def run_callback(self, *args, **kwargs):
        raise NotImplementedError

    def _to_dict(self):
        exclude = ("_callback", "callback", "run_callback")
        return {k: v for k, v in self.__dict__.items() if v is not None and k not in exclude}


class Button(Component):
    def __init__(self, style: int, *, label: str = None, emoji: dict = None, url: str = None, disabled: bool = None,
                 callback: Callable[[Any, Any], Any] = None):
        super().__init__(type=2, style=style, label=label, emoji=emoji, url=url, disabled=disabled)
        self._callback = callback

    async def run_callback(self, *args, **kwargs):
        """Runs the callback function with the given arguments"""
        if hasattr(self, "callback") and self._callback:
            raise ValueError("Callback is specified twice")

        if hasattr(self, "callback"):
            return await maybe_await(self.callback, *args, **kwargs)

        elif self._callback:
            return await maybe_await(self._callback, *args, **kwargs)

        else:
            raise ValueError("Callback not specified")

    def __init_subclass__(cls, **kwargs):
        # Check if subclasses implement the callback method
        super().__init_subclass__(**kwargs)

        if not hasattr(cls, "callback"):
            raise TypeError("Subclasses of Button must implement callback method")


class View:
    def __init__(self, *components: Component):
        self.components: Tuple[Component] = components

    async def run_component_callback(self, custom_id: str, *args, **kwargs):
        """Runs the callback of the component with the given custom_id"""
        for component in self.components:
            if component.custom_id == custom_id:
                await component.run_callback(*args, **kwargs)

    def _to_dict(self):
        return {
            "type": 1,
            "components": [component._to_dict() for component in self.components],
        }
