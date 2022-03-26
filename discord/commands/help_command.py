import abc
import sys
import traceback
import typing

from discord.embeds import Embed

from .context import Context
from .core import Command
from .errors import CommandNotFound


async def help_cmd_callback(context: Context, *args): pass


class HelpCommand(abc.ABC, Command):
    def __init__(self,
                 name: str = "help",
                 *,
                 description: str = None,
                 aliases: typing.Iterable[str] = None,
                 regex_command: bool = False,
                 regex_flags=0
                 ):
        help_cmd_callback.__doc__ = description
        super().__init__(callback=help_cmd_callback, name=name, aliases=aliases, regex_command=regex_command,
                         regex_flags=regex_flags)
        self.on_error = self.on_help_error

    async def execute(self, context: Context, *args, **kwargs):
        await self.run_checks(context)

        client = context.client

        target_command_name = args[0] if args else None

        if target_command_name is None:
            await self.send_bot_help(context)
            return

        command = client.get_command_named(target_command_name)

        if command is None:
            error = CommandNotFound(target_command_name)
            await self.on_error(context, error)
            return

        await self.send_command_help(context, command)

    @abc.abstractmethod
    async def send_bot_help(self, context: Context):
        pass

    @abc.abstractmethod
    async def send_command_help(self, context: Context, command: Command):
        pass

    async def on_help_error(self, context: Context, error):
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


class DefaultHelpCommand(HelpCommand):
    async def send_bot_help(self, context: Context):
        embed = Embed(title="Help", description=f"All commands: {', '.join([str(cmd.qualified_name) for cmd in context.client.commands.values()])}")
        await context.send(embeds=embed)

    async def send_command_help(self, context: Context, command: Command):
        embed = Embed(title=command.qualified_name, description=f"Description: {command.description}")
        await context.send(embeds=embed)
