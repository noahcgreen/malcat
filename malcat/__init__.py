from flask import Flask

from malcat.cache import cache

app = Flask('malcat')
cache.init_app(app)

from malcat.views import CSSGeneratorView

app.add_url_rule('/s_test', view_func=CSSGeneratorView.as_view('s_test'))
