import typing
import aiohttp
import handler
import asyncio
import sys
import zlib
import json

class WebSocket:    
    # websocket opcodes
    DISPATCH           = 0
    HEARTBEAT          = 1
    IDENTIFY           = 2
    PRESENCE           = 3
    VOICE_STATE        = 4
    VOICE_PING         = 5
    RESUME             = 6
    RECONNECT          = 7
    REQUEST_MEMBERS    = 8
    INVALIDATE_SESSION = 9
    HELLO              = 10
    HEARTBEAT_ACK      = 11
    GUILD_SYNC         = 12

    def __init__(self, client, token):
        self.decompress = zlib.decompressobj()
        self.buffer = bytearray()
        self.client = client
        self.token = token
        self.session_id = None

    async def start(self, url):
        self.socket = await self.client.handler.connect(url)
        await self.receive_events()
        await self.identify()
        return self

    def on_websocket_message(self, msg):
        # always push the message data to your cache'
        if type(msg) is bytes:
            self.buffer.extend(msg)

        # check if the last four bytes are equal to ZLIB_SUFFIX
        if len(msg) < 4 or msg[-4:] != b'\x00\x00\xff\xff':
            self.buffer = bytearray()
            return msg.decode('utf-8')

        msg = self.decompress.decompress(self.buffer)
        self.buffer = bytearray()

        return msg.decode('utf-8')

    async def receive_events(self):
        msg = await self.socket.receive()
        if msg.type is aiohttp.WSMsgType.TEXT:
            msg = self.on_websocket_message(msg.data)
        elif msg.type is aiohttp.WSMsgType.BINARY:
            msg = self.on_websocket_message(msg.data)
        elif msg.type in (aiohttp.WSMsgType.CLOSE, aiohttp.WSMsgType.CLOSING, aiohttp.WSMsgType.CLOSED):
            print(msg)
            raise ConnectionResetError(msg.extra)
        
        print(msg)
        msg = json.loads(msg)

        op = msg["op"]
        data = msg["d"]
        sequence = msg["s"]
        
        if op == self.HELLO:
            self.sequence = sequence
            await self.heartbeat()

        if op == self.HEARTBEAT:
            print("HB")
            self.sequence = sequence
            await self.heartbeat()

    async def dispatch(self):
        pass
    
    async def heartbeat(self):
        """Send HB packet"""
        payload = {
            'op': self.HEARTBEAT,
            'd': self.sequence
            }
        await self.socket.send_json(payload)

    async def identify(self):
        """Sends the IDENTIFY packet"""
        print("sent identify")
        payload = {
            'op': self.IDENTIFY,
            'd': {
                'token': self.token,
                'intents': 32767,
                'properties': {
                    '$os': sys.platform,
                    '$browser': 'disthon',
                    '$device': 'disthon'
                },
                'large_threshold': 250,
            }
        }
        await self.socket.send_json(payload)
    
    async def resume(self):
        """Sends the RESUME packet."""
        payload = {
            'op': self.RESUME,
            'd': {
                'seq': self.sequence,
                'session_id': self.session_id,
                'token': self.token
            }
        }

        await self.socket.send_json(payload)
