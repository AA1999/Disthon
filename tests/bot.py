import os
import sys

import asyncio

from discord import Client, Message

from discord.api.intents import Intents

from discord.types.snowflake import Snowflake

client = Client(intents = Intents.all())

async def create(msg: Message):
	if msg.author.id != Snowflake(msg.client.info["id"]):
		await msg.reply("Hello!");
	
	pass

async def main(token):
	task = asyncio.create_task(client.alive_loop(token))

	client.on("message_create")(create)

	print("Running")

	await task

def run(token):
	asyncio.run(main(token))