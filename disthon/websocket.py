import typing
import aiohttp
import handler
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

    async def gateway(self):
        try:
            gw_data = await self.client.handler.request("GET", "/gateway")
            url = gw_data['url'] + '?encoding=json&v=9&compress=zlib-stream'
            return url
        except Exception as e:
            raise ConnectionError("An issue occured connecting to the discord API") from e

    def on_websocket_message(self, msg):
        # always push the message data to your cache
        self.buffer.extend(msg)

        # check if the last four bytes are equal to ZLIB_SUFFIX
        if len(msg) < 4 or msg[-4:] != b'\x00\x00\xff\xff':
            self.buffer = bytearray()
            return msg.decode('utf-8')

        msg = self.decompress.decompress(self.buffer)
        self.buffer = bytearray()

        return msg.decode('utf-8')

    async def receive_events(self):
        msg = await self.connection.receive()
        print(msg.type)
        if msg.type is aiohttp.WSMsgType.TEXT:
            msg = self.on_websocket_message(msg.data)
        elif msg.type is aiohttp.WSMsgType.BINARY:
            msg = self.on_websocket_message(msg.data)
        
        print("msg ", msg)
        msg = json.loads(msg)

        op = msg["op"]
        data = msg["d"]
        sequence = msg["s"]

        if op == self.HEARTBEAT:
            self.sequence = sequence
            await self.heartbeat()

    def dispatch(self):
        pass
    
    async def heartbeat(self):
        """Send HB packet"""
        payload = {
            'op': self.HEARTBEAT,
            'd': self.sequence
            }
        self.connection.send_json(payload, compress=9)

    async def identify(self):
        """Sends the IDENTIFY packet"""
        payload = {
            'op': self.IDENTIFY,
            'd': {
                'token': self.token,
                'properties': {
                    '$os': sys.platform,
                    '$browser': 'discord.py',
                    '$device': 'discord.py',
                    '$referrer': '',
                    '$referring_domain': ''
                },
                'compress': True,
                'large_threshold': 250,
                'v': 3
            }
        }
        await self.connection.send_json(payload, compress=9)
    
    def resume(self):
        pass
