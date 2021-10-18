
from typing import Optional

import arrow


def utcnow():
    return arrow.utcnow()

def parse_time(timestamp: Optional[str]):
    if timestamp:
        return arrow.get(timestamp)
    return None

