import werkzeug.exceptions
from google.appengine.api import urlfetch_errors

from malcat.client import app


@app.errorhandler(werkzeug.exceptions.BadRequestKeyError)
def handle_missing_argument(e):
    return 'Argument is missing or invalid: {}'.format(e.args[0])


@app.errorhandler(urlfetch_errors.DeadlineExceededError)
def handle_urlfetch_deadline_exceeded(e):
    return 'The requested page took too long to load.'
