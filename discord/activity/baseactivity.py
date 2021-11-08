from __future__ import annotations

from datetime import datetime
from typing import Optional

from ..types.activitypayload import ActivityPayload


class BaseActivity:
    _created_at: Optional[datetime]
    __slots__ = ("_created_at",)

    def __init(self, **kwargs):
        self._created_at = kwargs.pop("created_at", None)

    @property
    def created_at(self):
        return self._created_at

    def to_dict(self) -> ActivityPayload:
        payload = ActivityPayload()
        payload["created_at"] = self.created_at
        return payload
