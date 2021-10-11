from enum import IntEnum


class AuditLogActionCategory(IntEnum):
    create = 1
    delete = 2
    update = 3
