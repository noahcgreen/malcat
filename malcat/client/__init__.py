import flask

app = flask.Flask(__name__.split('.')[0])

from malcat.client import views, errorhandlers
