import inspect
import re
from typing import List, Dict, Tuple, Optional, Union, Any

from discord.message import Message
from . import Command
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

    def remove_prefix(self, content: str):
        command_prefix = self.command_prefix
        if isinstance(command_prefix, (tuple, list, set)):
            for prefix in self.command_prefix:
                if content.startswith(prefix):
                    return content[len(prefix):]

        elif isinstance(command_prefix, str):
            return content[len(command_prefix):]

    def get_args(self, command: Command, content: str, prefix=None):
        prefix = prefix or command.name
        content = content[len(prefix):].strip()
        signature = inspect.signature(command.callback)
        parameters = signature.parameters.copy()
        parameters.pop(tuple(parameters.keys())[0])  # Remove the message parameter

        args = content.split()
        positional_arguments = []
        kwargs = {}
        extra_kwargs = {}

        for index, (name, parameter) in enumerate(parameters.items()):
            if parameter.kind is parameter.KEYWORD_ONLY:
                kwargs[name] = (" ".join(args[index:])).strip()

            elif parameter.kind is parameter.VAR_KEYWORD:
                extra_kwargs = dict(re.findall(r"(\D+)=(\w+)", content))

            elif parameter.kind is parameter.VAR_POSITIONAL:
                positional_arguments.extend(args)

            else:
                positional_arguments.append(args[index].strip())

        return positional_arguments, kwargs, extra_kwargs

    def parse_message(self, message: Message):
        if not self.commands:
            return None, []

        if not message.content.startswith(self.command_prefix):
            return None, []

        no_prefix = self.remove_prefix(message.content)  # The content of the message but without the command_prefix

        if not self.case_sensitive:
            no_prefix = no_prefix.lower()

        command = self.commands.get(no_prefix.split()[0])
        if command:
            return command, *self.get_args(command, no_prefix)

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

                return regex_command, *self.get_args(command, no_prefix, prefix=prefix)

        return None, []
