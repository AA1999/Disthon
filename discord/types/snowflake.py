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
