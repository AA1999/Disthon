from __future__ import annotations

from pydantic import BaseModel
import datetime

__all__ = ("Snowflake",)


class Snowflake(BaseModel):
    id: int

    def __init__(self, id: int):
        super().__init__(id=id)

    @property
    def timestamp(self):
        return (self.id >> 22) + 1420070400000

    @property
    def worker_id(self):
        return (self.id & 0x3E0000) >> 17

    @property
    def process_id(self):
        return (self.id & 0x1F000) >> 12

    @property
    def increment(self):
        return self.id & 0xFFF
    
    @property
    def created_at(self):
        return datetime.datetime.fromtimestamp(self.timestamp/1000)

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        if isinstance(value, int):
            return cls(value)
        elif isinstance(value, str):
            if value.isdigit():
                return cls(value)
            else:
                raise ValueError("Invalid Snowflake")
        elif isinstance(value, Snowflake):
            return value
        else:
            return ValueError("Invalid Snowflake")

    def __eq__(self, other) -> bool:
        if isinstance(other, (int, str)):
            return self.id == other
        return isinstance(other, Snowflake) and self.id == other.id

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __lt__(self, other: object):
        if isinstance(other, int):
            return self.id < other
        if isinstance(other, str) and other.isdigit():
            return self.id < int(other)
        if isinstance(other, Snowflake):
            return self.id < other.id
        raise NotImplementedError

    def __le__(self, other: object):
        return self.__eq__(other) or self.__lt__(other)

    def __gt__(self, other: object):
        return not self.__le__(other)

    def __ge__(self, other: object):
        return not self.__lt__(other)

    def __str__(self) -> str:
        return str(self.id)

    def __int__(self) -> int:
        return int(self.id)

    def __repr__(self) -> str:
        return f"Snowflake with id {self.id}"
