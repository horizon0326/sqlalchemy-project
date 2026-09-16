from config.cache_config import get_json_cache, set_cache
from typing import Optional

CATEGORIES_KEY = 'news:categories'
NEWS_LIST_PREFIX = 'news_list'

async def get_cache_categories():
    return await get_json_cache(CATEGORIES_KEY)

async def set_cache_categories(data: list[dict[str, any]], expire: int = 7200):
    return await set_cache(CATEGORIES_KEY, data, expire)

async def set_cache_news_list(category_id: Optional[int], page: int, size: int, news_list: list[dict[str, any]], expire: int = 1800):
    if not category_id:
        category_id = 'all'
    key = f'{NEWS_LIST_PREFIX}:{category_id}:{page}:{size}'
    return await set_cache(key, news_list, expire)

async def get_cache_news_list(category_id: Optional[int], page: int, size: int):
    if not category_id:
        category_id = 'all'
    key = f'{NEWS_LIST_PREFIX}:{category_id}:{page}:{size}'
    return await get_json_cache(key)