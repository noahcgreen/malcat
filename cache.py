import os
from flask_cache import Cache
import redis
import requests_cache

config = {
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': os.getenv('REDIS_URL', 'redis://localhost:6379')
}

cache = Cache(config=config)
redis_conn = redis.from_url(config['CACHE_REDIS_URL'])
requests_cache.install_cache('malcat',
                             backend='redis',
                             expire_after=900,
                             old_data_on_error=True,
                             connection=redis_conn)
