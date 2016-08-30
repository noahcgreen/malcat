from werkzeug.contrib.profiler import ProfilerMiddleware
from malcat import app

app.config['PROFILE'] = True
app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[50])
