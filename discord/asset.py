import io
from typing import Union, TYPE_CHECKING

from pydantic import BaseModel


if TYPE_CHECKING:
    from discord import Client


class Asset(BaseModel):
    _client: "Client"
    url: str

    async def read(self):
        return await self._client.httphandler.get_from_cdn(self.url)

    async def save(self, fp: Union[str, io.BufferedIOBase]):
        if isinstance(fp, str):
            with open(fp, "wb+") as file:
                return file.write(await self.read())

        return fp.write(await self.read())
