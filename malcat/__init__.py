import os

from flask import Flask, Response
import yaml

app = Flask(__name__.split()[0])

BASE_DIR = os.getcwd()
_CONFIG_FILE_PATH = os.path.join(BASE_DIR, 'malcat.config.yaml')
with open(_CONFIG_FILE_PATH) as f:
    CONFIG = yaml.load(f)

import malcat.views

#####

# from werkzeug.contrib.profiler import ProfilerMiddleware
#
# app.config['PROFILE'] = True
# app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[50])
