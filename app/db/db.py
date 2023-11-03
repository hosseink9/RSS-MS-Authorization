import asyncio
import aioredis


class RedisDB:
    address = aioredis.from_url("redis://localhost:6379/1")

    def __init__(self) -> None:
        self.redis = self.address

    async def set_data(self, key: str, value: str, timeout):
        await self.redis.set(key, value, timeout)
        return "data is store"

    async def get_data(self, key: str):
        result = await self.redis.get(key)
        return result

    async def delete_data(self, key: str):
        await self.redis.delete(key)
        return f"{key} was deleted"
