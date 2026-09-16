from redis import asyncio as redis
import json

REDIS_HOST = '192.168.154.130'

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=6379,
    decode_responses=True,
    password='foobared'
)

async def get_cache(key: str):
    try:
        return await redis_client.get(key)
    except Exception as e:
        print(f'获取缓存失败：{e}')
        return None

async def get_json_cache(key: str):
    try:
        data = await redis_client.get(key)
        if data:
            return json.loads(data)
        return None
    except Exception as e:
        print(f'获取JSON缓存失败:{e}')
        return None

async def set_cache(key: str, value, expire: int = 3600):
    try:
        if isinstance(value, (dict, list)):
            value = json.dumps(value, ensure_ascii=False)
        await redis_client.setex(key, expire, value)
        return True
    except Exception as e:
        print(f'设置缓存失败：{e}')
        return False