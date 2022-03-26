class CommandError(Exception):
    pass


class CheckFailure(CommandError):
    def __init__(self, command):
        self.command = command
        super().__init__(f"Check failed for command {command.name}")


class CommandNotFound(CommandError):
    def __init__(self, command_name):
        self.command_name = command_name

        super().__init__(f"Command with the name {self.command_name} does not exist")
