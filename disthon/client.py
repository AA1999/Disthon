import handler
import aiohttp
import asyncio

class Client:
    def __init__(self):
        self.stay_alive = True
        self.handler = handler.Handler()

    async def alive(self):
        while self.stay_alive:
            pass

    async def login(self, token):
        await self.handler.login(token)

    def run(self, token):
        self.__loop = asyncio.get_event_loop()
        
        self.__loop.create_task(self.login(token))
        self.__loop.run_forever()

