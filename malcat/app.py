from flask import Flask
from flask_cache import Cache
import os

app = Flask('malcat')
app.config.update({
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': os.getenv('REDIS_URL', 'redis://localhost:6379'),
    'DEBUG': True
})
cache = Cache(app)
