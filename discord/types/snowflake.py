from typing import Union, Any


class Snowflake:
    __slots__ = ('_id',)
    _id: Union[int, str]

    def __init__(self, value: Union[int, str]):
        if(isinstance(value, str) and value.isdigit()) or isinstance(value, int):
            self._id = value
        else:
            raise ValueError('Snowflake can only contain digits.')

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Snowflake) and self._id == other._id

    def __lt__(self, other):
        return isinstance(other, Snowflake) and self.id < other.id

    def __le__(self, other):
        return isinstance(other, Snowflake) and self.id <= other.id

    def __gt__(self, other):
        return isinstance(other, Snowflake) and self.id > other.id

    def __ge__(self, other):
        return isinstance(other, Snowflake) and self.id >= other.id

    def __int__(self):
        return int(self.id)

    def __str__(self):
        return str(self.id)

    def __ne__(self, other: Any):
        return not self.__eq__(other)

    def __len__(self) -> int:
        return len(str(self._id))

    def __repr__(self):
        return self._id

    @property
    def id(self):
        return self._id
