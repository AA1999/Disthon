from __future__ import annotations

import asyncio
import json
import sys
import threading
import time
import typing
import zlib
from copy import deepcopy

import aiohttp
from aiohttp.http_websocket import WSMessage, WSMsgType

from ..cache import LFUCache, FIFOCache
from ..channels.basechannel import BaseChannel
from ..guild import Guild
from ..types.snowflake import Snowflake

if typing.TYPE_CHECKING:
    from ..client import Client
    from ..message import Message


class WebSocket:
    # websocket opcodes
    DISPATCH = 0
    HEARTBEAT = 1
    IDENTIFY = 2
    PRESENCE = 3
    VOICE_STATE = 4
    VOICE_PING = 5
    RESUME = 6
    RECONNECT = 7
    REQUEST_MEMBERS = 8
    INVALIDATE_SESSION = 9
    HELLO = 10
    HEARTBEAT_ACK = 11
    GUILD_SYNC = 12

    def __init__(self, client, token: str) -> None:
        self.decompress = zlib.decompressobj()
        self.buffer = bytearray()
        self.client: Client = client
        self.token = token
        self.session_id = None
        self.heartbeat_acked = True
        self.closed: bool = False

        self.guild_cache = LFUCache[Snowflake, Guild](1000)
        self.channel_cache = LFUCache[Snowflake, BaseChannel](5000)
        self.member_cache = LFUCache[Snowflake, dict](5000)
        self.user_cache = LFUCache[Snowflake, dict](5000)
        self.message_cache = FIFOCache[Snowflake, "Message"](1000)

    async def start(
        self,
        url: typing.Optional[str] = None,
        *,
        reconnect: typing.Optional[bool] = False
    ):
        if not url:
            url = self.client.httphandler.gateway()
        self.socket = await self.client.httphandler.connect(url)
        await self.receive_events()
        await self.identify()
        if reconnect:
            await self.resume()
        else:
            self.hb_t: threading.Thread = threading.Thread(target=self.keep_alive, daemon=True)
            self.hb_stop: threading.Event = threading.Event()
            self.hb_t.start()
            return self

    async def close(self) -> None:
        """Closes the websocket"""
        self.closed = True
        await self.socket.close()
        self.hb_stop.set()

    def keep_alive(self) -> None:
        while not self.hb_stop.wait(self.hb_int):
            if not self.heartbeat_acked:
                # We have a zombified connection
                self.socket.close(code=1000)
                asyncio.run(self.start(reconnect=True))
            else:
                asyncio.run(self.heartbeat())

    def on_websocket_message(self, msg: WSMessage) -> dict: 
        if type(msg) is bytes:
            # always push the message data to your cache
            self.buffer.extend(msg)

            # check if last 4 bytes are ZLIB_SUFFIX
            if len(msg) < 4 or msg[-4:] != b"\x00\x00\xff\xff":
                return msg

            msg: bytes = self.decompress.decompress(self.buffer)
            msg = msg.decode("utf-8")
            self.buffer = bytearray()

        return msg

    async def receive_events(self) -> None:
        msg: WSMessage = await self.socket.receive()
        # if the message is something we can handle
        if msg.type is aiohttp.WSMsgType.TEXT or msg.type is aiohttp.WSMsgType.BINARY:
            msg = self.on_websocket_message(msg.data)
        # if it's a disconnection
        elif msg.type in (
            aiohttp.WSMsgType.CLOSE,
            aiohttp.WSMsgType.CLOSING,
            aiohttp.WSMsgType.CLOSED,
        ):
            if not self.closed:
                await self.socket.close()
                raise ConnectionResetError(msg.extra)
            else:
                return

        msg = json.loads(msg)

        op = msg["op"]
        data = msg["d"]
        sequence = msg["s"]

        self.sequence = sequence

        if op == self.HELLO:
            self.hb_int = msg["d"]["heartbeat_interval"] // 1000
            await self.heartbeat()

        elif op == self.HEARTBEAT:
            await self.heartbeat()

        elif op == self.DISPATCH:
            if msg["t"] == "READY":
                self.session_id = msg["d"]["session_id"]

            # send event to dispatch
            await self.client.handle_event(msg)

    async def heartbeat(self) -> None:
        """Send HB packet"""
        payload = {"op": self.HEARTBEAT, "d": self.sequence}
        await self.socket.send_json(payload)

    async def identify(self) -> None:
        """Sends the IDENTIFY packet"""
        payload = {
            "op": self.IDENTIFY,
            "d": {
                "token": self.token,
                "intents": self.client.intents.value,
                "properties": {
                    "$os": sys.platform,
                    "$browser": "disthon",
                    "$device": "disthon",
                },
                "large_threshold": 250,
                "compress": True,
            },
        }
        await self.socket.send_json(payload)

    async def resume(self) -> None:
        """Sends the RESUME packet."""
        payload = {
            "op": self.RESUME,
            "d": {
                "seq": self.sequence,
                "session_id": self.session_id,
                "token": self.token,
            },
        }

        await self.socket.send_json(payload)
