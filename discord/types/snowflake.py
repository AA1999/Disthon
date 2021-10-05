from typing import Union, Any


class Snowflake():
    __slots__ = ('_id',)
    _id: Union[int, str]

    def __init__(self, value: Union[int, str]):
        if(isinstance(value, str) and value.isdigit()) or isinstance(value, int):
            self._id = value
        else:
            raise ValueError('Snowflake can only contain digits.')

    def __eq__(self, o: Any) -> bool:
        return isinstance(o, Snowflake) and self._id == o._id

    def __ne__(self, o: Any):
        return not self.__eq__(o)

    def __len__(self) -> int:
        return len(str(self._id))

    def __repr__(self):
        return self._id

    @property
    def id(self):
        return self._id
