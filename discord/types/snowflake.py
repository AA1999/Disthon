import datetime

__all__ = ("Snowflake",)


class Snowflake(int):
    @property
    def timestamp(self):
        return (self >> 22) + 1420070400000

    @property
    def worker_id(self):
        return (self & 0x3E0000) >> 17

    @property
    def process_id(self):
        return (self & 0x1F000) >> 12

    @property
    def increment(self):
        return self & 0xFFF
    
    @property
    def created_at(self):
        return datetime.datetime.fromtimestamp(self.timestamp)  # TODO: Fix this

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
