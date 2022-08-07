from __future__ import annotations

from typing import Any, Dict, OrderedDict

from .types.snowflake import Snowflake


class LFUCache(OrderedDict):
    def __init__(self, capacity: int) -> None:
        self.capacity: int = capacity
        self._frequency: Dict[Snowflake, int] = {}
        self.length: int = 0
        super().__init__()

    def __setitem__(self, key: Snowflake, value: Any) -> None:
        frequency = self._frequency

        if key not in self:
            self.length += 1

        super().__setitem__(key, value)
        frequency[key] = 0

        if self.length > self.capacity:
            inverted = dict(zip(frequency.values(), frequency.keys()))
            least_used = min(self._frequency.values())
            del self[inverted[least_used]]

    def __getitem__(self, key: Snowflake):
        self._frequency[key] += 1
        return self[key]

    def __delitem__(self, key: Snowflake):
        super().__delitem__(key)
        del self._frequency[key]
        self.length -= 1


class FIFOCache(OrderedDict):
    def __init__(self, capacity: int):
        self.capacity: int = capacity
        super().__init__()

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.move_to_end(key, last=True)

        if len(self) > self.capacity:
            # Pop the first value if the capacity is exceeded
            self.popitem(last=False)
