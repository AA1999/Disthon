from __future__ import annotations

import typing
from typing import Optional, Union

import aiohttp

from discord.interactions.components import View

from ..types.snowflake import Snowflake

from ..embeds import Embed
from ..exceptions import (DiscordChannelForbidden, DiscordChannelNotFound,
						  DiscordForbidden, DiscordGatewayNotFound,
						  DiscordHTTPException, DiscordNotAuthorized,
						  DiscordNotFound, DiscordServerError)


class HTTPHandler:
	def __init__(self):
		self.base_url: str = "https://discord.com/api/v9/"
		self.user_agent: str = "Disthon Discord API wrapper V0.0.1b"

	async def request(
		self,
		method: str,
		dest: str,
		*,
		headers: Optional[dict] = None,
		data: Optional[dict] = None,
	) -> Union[str, dict]:
		async with self._session.request(
			method, self.base_url + dest, headers=headers, json=data
		) as r:
			if not 200 <= r.status < 300:
				if r.status == 401:
					raise DiscordNotAuthorized
				elif r.status == 403:
					raise DiscordForbidden
				elif r.status == 404:
					raise DiscordGatewayNotFound
				elif r.status == 500:
					raise DiscordServerError
			text = await r.text()
			try:
				if r.headers["content-type"] == "application/json":
					return await r.json()
			except KeyError:
				pass

			return text

	async def login(self, token: str) -> Union[str, dict]:
		self.token = token
		self._session = aiohttp.ClientSession(
			headers={"Authorization": "Bot " + self.token}
		)

		try:
			auth_data = await self.request("GET", "/users/@me")
		except ConnectionError as e:
			raise ConnectionError("The token passed is invalid") from e

		return auth_data

	async def gateway(self) -> str:
		gw_data = await self.request("GET", "/gateway/bot")
		if isinstance(gw_data, dict):
			return gw_data["url"] + "?encoding=json&v=9&compress=zlib-stream"
		raise NotImplementedError

	async def connect(self, url: str) -> aiohttp.ClientWebSocketResponse:
		kwargs = {
			"timeout": 100.0,
			"autoclose": False,
			"headers": {
				"User-Agent": self.user_agent,
			},
			"compress": 0,
		}
		return await self._session.ws_connect(url, **kwargs)

	async def close(self) -> None:
		if self._session:
			await self._session.close()

	async def get_from_cdn(self, url: str) -> bytes:
		async with self._session.get(url) as response:
			if response.status == 200:
				return await response.read()
			elif response.status == 404:
				raise DiscordNotFound("asset not found")
			elif response.status == 403:
				raise DiscordForbidden("cannot retrieve asset")
			else:
				raise DiscordHTTPException("failed to get asset", response.status)

	async def send_message(
		self,
		channel_id: int,
		content: typing.Optional[str] = None,
		embeds: typing.Union[Embed, typing.List[Embed]] = None,
		views: typing.Union[View, typing.List[View]] = None,
		reference: typing.Optional[Snowflake] = None
	):
		if isinstance(embeds, Embed):
			embeds = [embeds]
		if isinstance(views, View):
			views = [views]

		payload = {}

		if content:
			payload["content"] = content
		
		if embeds:
			payload["embeds"] = [embed.dict() for embed in embeds]

		if views:
			payload["components"] = [view._to_dict() for view in views]

		if reference:
			payload["message_reference"] = { "message_id": reference }

		data = await self.request(
			"POST", f"channels/{channel_id}/messages", data=payload
		)
		try:
			if isinstance(data, dict):
				if data["code"] == 50008:
					raise DiscordChannelNotFound
				elif data["code"] == 10003:
					raise DiscordChannelForbidden
		except KeyError:
			return data

	async def edit_message(
		self,
		channel_id: int,
		message_id: int,
		*,
		content: typing.Optional[str] = None,
		embeds: typing.Union[Embed, typing.List[Embed]] = None,
		views: typing.Union[View, typing.List[View]] = None,
	):
		if isinstance(embeds, Embed):
			embeds = [embeds]
		if isinstance(views, View):
			views = [views]

		payload = {}

		if content:
			payload["content"] = content
		if embeds:
			payload["embeds"] = [embed._to_dict() for embed in embeds]
		if views:
			payload["components"] = [view._to_dict() for view in views]

		return await self.request(
			"PATCH", f"/channels/{channel_id}/messages/{message_id}", data=payload
		)

	async def delete_message(self, channel_id: int, message_id: int):
		await self.request("DELETE", f"/channels/{channel_id}/messages/{message_id}")

	async def bulk_delete_messages(
		self, channel_id: int, message_ids: typing.Iterable[int]
	):
		await self.request(
			"POST",
			f"/channels/{channel_id}/messages/bulk-delete",
			data={"messages": message_ids},
		)

	async def add_reaction(self, channel_id: int, message_id: int, emoji: str):
		await self.request(
			"PUT", f"/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me"
		)

	async def delete_own_reaction(self, channel_id: int, message_id: int, emoji: str):
		await self.request(
			"DELETE",
			f"/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me",
		)

	async def delete_user_reaction(
		self, channel_id: int, message_id: int, user_id: int, emoji: str
	):
		await self.request(
			"DELETE",
			f"/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/{user_id}",
		)

	async def fetch_message_reactions(
		self,
		channel_id: int,
		message_id: int,
		emoji: str,
		after: int = None,
		limit: int = None,
	):
		url = f"/channels/{channel_id}/messages/{message_id}/reactions/{emoji}"
		params = {"after": after, "limit": limit}

		if any(params.values()):
			url += "?"
			for k, v in params.items():
				url += f"{k}={v}&"

		await self.request("GET", url)

	async def delete_all_reactions(self, channel_id: int, message_id: int):
		await self.request(
			"DELETE", f"/channels/{channel_id}/messages/{message_id}/reactions"
		)

	async def delete_all_reactions_for_emoji(
		self, channel_id: int, message_id: int, emoji: str
	):
		await self.request(
			"DELETE", f"/channels/{channel_id}/messages/{message_id}/reactions/{emoji}"
		)

	async def delete_channel(self, channel_id: int):
		await self.request("DELETE", f"/channels/{channel_id}")

	async def fetch_channel_history(
		self, channel_id: int, limit=None, around=None, before=None, after=None
	):
		url = f"/channels/{channel_id}/messages"
		params = {"limit": limit, "around": around, "before": before, "after": after}

		if any(params.values()):
			url += "?"
			for k, v in params.items():
				if v is not None:
					url += f"{k}={v}&"

		await self.request("GET", url)

	async def fetch_channel(self, channel_id: int):
		data = await self.request("GET", f"/channels/{channel_id}")
		return data

	async def edit_guild_text_channel(self, channel_id: int, **options: typing.Any):
		payload = {k: v for k, v in options.items()}
		await self.request(
			"PATCH",
			f"/channels/{channel_id}",
			headers={"Content-Type": "application/json"},
			data=payload,
		)

	async def edit_guild_voice_channel(self, channel_id: int, **options):
		payload = {
			"name": options["name"],
			"position": options["position"],
			"bitrate": options["bitrate"],
			"user_limit": options["user_limit"],
			"permission_overwrites": options["overwrites"],
			"parent_id": options["category"],
			"rtc_region": options["region"],
		}
		await self.request("PATCH", f"/channels/{channel_id}", data=payload)

	async def get_from_cdn(self, url: str):
		async with self._session.get(url) as resp:
			if resp.status == 200:
				return await resp.read()
			if resp.status == 404:
				raise DiscordNotFound("Requested asset could not be found.")
			if resp.status == 403:
				raise DiscordForbidden("Unable to fetch requested asset.")
			if resp.status == 401:
				raise DiscordNotAuthorized("Fetching asset failed.")
			if resp.status == 500:
				raise DiscordServerError("Internal server error.")
			raise DiscordHTTPException("Failed to fetch the asset.", resp.status)
