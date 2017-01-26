import werkzeug.exceptions
from google.appengine.api import urlfetch_errors

from malcat.client import app


@app.errorhandler(werkzeug.exceptions.BadRequestKeyError)
def handle_missing_argument(e):
    return 'Argument is missing or invalid: {}'.format(e.args[0])


@app.errorhandler(urlfetch_errors.DownloadError)
def handle_urlfetch_connection_closed(e):
    return 'An uncontrollable error (i.e., not Doom\'s fault) occurred: {}'.format(e.args[0])
