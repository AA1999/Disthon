from __future__ import annotations

from pydantic import BaseModel

__all__ = ('Snowflake', )


class Snowflake(BaseModel):
    id: int
                    
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
        return f'Snowflake with id {self.id}'
