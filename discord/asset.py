import io
from typing import Union

from pydantic import BaseModel

from discord import Client


CDN_URL = "https://cdn.discordapp.com"

class Asset(BaseModel):
    _client: Client
    url: str

    async def read(self):
        return await self._client.httphandler.get_from_cdn(self.url)

    async def save(self, fp: Union[str, io.BufferedIOBase]):
        data = await self.read()
        if isinstance(fp, str):
            with open(fp, "wb+") as file:
                return file.write(data)

        return fp.write(data)