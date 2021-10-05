from typing import Optional
from datetime import datetime


class BaseActivity:
    _created_at: Optional[datetime]
    __slots__ = ('_created_at')
    
    def __init(self, **kwargs):
        self._created_at = kwargs.pop('created_at', None)
    
    @property
    def created_at(self):
        return self._created_at  