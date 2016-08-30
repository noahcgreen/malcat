from flask import Flask

from malcat.cache import cache

app = Flask('malcat')
cache.init_app(app)

from . import views
