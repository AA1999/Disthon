import os
import sys

import asyncio

from discord import Client, Message

from discord.api.intents import Intents

from discord.types.snowflake import Snowflake

kwargs = {name: True for name in Intents.VALID_INTENTS}

client = Client(intents = Intents.all())

async def create(msg: Message):
	if msg.content == "Hello":
		print(msg.__repr__())
		await msg.reply("Hello!");
	
	pass

async def main(token):
	task = asyncio.create_task(client.alive_loop(token))

	client.on("message_create")(create)

	print("Running")

	await task

def run(token):
	asyncio.run(main(token))