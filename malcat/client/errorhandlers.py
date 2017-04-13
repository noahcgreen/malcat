import werkzeug.exceptions
from google.appengine.api import urlfetch_errors

from malcat.client import app
from malcat.server import parse


# MalCat Errors


@app.errorhandler(parse.ParseError)
def handle_parsing_error(e):
    return 'Error occurred while parsing list information: {}'.format(e.args[0])


# Flask errors


@app.errorhandler(werkzeug.exceptions.BadRequestKeyError)
def handle_missing_argument(e):
    return 'Argument is missing or invalid: {}'.format(e.args[0])


# Google App Engine errors


@app.errorhandler(urlfetch_errors.DownloadError)
def handle_urlfetch_connection_closed(e):
    return 'An error occurred while downloading list information: {}'.format(e.args[0])


@app.errorhandler(urlfetch_errors.DeadlineExceededError)
def handle_urlfetch_connection_closed(e):
    return 'Your list information took too long to download: {}'.format(e.args[0])
