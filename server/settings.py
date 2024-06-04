import orjson
import asyncio
import aiofiles

from server.utils.deep_dict import deep_get, deep_set, deep_unset

loaded_settings = {}

async def save() -> None:
    async with aiofiles.open("./user_data/setings.json", "wb") as file:
        contents = await asyncio.to_thread(orjson.dumps, loaded_settings, option=orjson.OPT_NON_STR_KEYS)
        await file.write(contents)

async def load() -> dict:
    async with aiofiles.open("./user_data/settings.json", "rb") as file:
        contents = await file.read()
        loaded_settings = await asyncio.to_thread(orjson.loads, contents)

        return loaded_settings
    
async def set(key: str, value):
    await deep_set(loaded_settings, key, value)

async def unset(key: str):
    await deep_unset(loaded_settings, key)
    await save()

async def get(key: str, default=None):
    return await deep_get(loaded_settings, key, default)