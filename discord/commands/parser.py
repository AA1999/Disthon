from re import L
from typing import List, Dict, Tuple, Optional

from discord.message import Message
from .core import Command


class CommandParser:
    def __init__(
        self,
        command_prefix: str,
        commands: Dict[str, Command],
        case_sensitive: bool = True,
    ):
        self.command_prefix = command_prefix
        self.case_sensitive = case_sensitive
        self.commands = commands

    def remove_prefix(self, content):
        command_prefix = self.command_prefix
        if isinstance(command_prefix, (tuple, list, set)):
            for prefix in self.command_prefix:
                if content.startswith(prefix):
                    return content[len(prefix) :]

        elif isinstance(command_prefix, str):
            return content[len(command_prefix) :]

    def parse_message(self, message: Message) -> Tuple[Optional[Command], List[str]]:
        if not self.commands:
            return

        if not message.content.startswith(self.command_prefix):
            return

        no_prefix = self.remove_prefix(message.content)  # The content of the message but without the command_prefix

        if not self.case_sensitive:
            no_prefix = no_prefix.lower()

        command = self.commands.get(no_prefix.split()[0])
        if command:
            args = no_prefix[len(command.name) :].split()

            return command, args

        for regex_command in filter(
            lambda cmd: cmd.is_regex_command, self.commands.values()
        ):
            regex = regex_command.name
            regex_match_func = regex_command.regex_match_func
            regex_flags = regex_command.regex_flags

            if match := regex_match_func(regex, no_prefix, regex_flags):
                try:
                    prefix = match.group(1)
                except IndexError:
                    raise ValueError(
                        "First match group of command regex does not exist"
                    )

                args = no_prefix[len(prefix) :].split()
                return regex_command, args

        return (None, [])
