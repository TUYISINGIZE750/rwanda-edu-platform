import redis.asyncio as redis
from .config import settings

class RedisClient:
    def __init__(self):
        self.client = None
    
    async def connect(self):
        self.client = await redis.from_url(settings.REDIS_URL, decode_responses=True)
    
    async def disconnect(self):
        if self.client:
            await self.client.close()
    
    async def publish(self, channel: str, message: str):
        await self.client.publish(channel, message)
    
    async def subscribe(self, channel: str):
        pubsub = self.client.pubsub()
        await pubsub.subscribe(channel)
        return pubsub

redis_client = RedisClient()
