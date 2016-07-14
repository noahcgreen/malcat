from flask import Flask
from .cache import cache

app = Flask('malcat')
cache.init_app(app)
