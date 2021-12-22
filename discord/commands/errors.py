class CommandError(Exception):
    pass


class CheckFailure(Exception):
    def __init__(self, command):
        self.command = command
        super().__init__(f"Check failed for command {command.name}")
