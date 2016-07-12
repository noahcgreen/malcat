from werkzeug.contrib.profiler import ProfilerMiddleware
from malcat import app

if __name__ == '__main__':
    app.config['PROFILE'] = True
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[50])
    app.run(debug=True)
