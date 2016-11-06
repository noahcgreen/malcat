import urlparse
import collections

import flask
import werkzeug.exceptions

import malcat


def list_identifiers():
    try:
        username = flask.request.args['user']
        list_type = flask.request.args['list']
    # Hold on to the original error so that the missing argument can be
    # determined.
    except KeyError as e:
        try:
            referer = flask.request.headers['REFERER']
        except KeyError:
            raise e
        else:
            url_path = urlparse.urlparse(referer).path
            username = url_path[11:]
            list_type = url_path[1:6]
    list_type = list_type.lower()
    if list_type not in malcat.config['list types']:
        raise werkzeug.exceptions.BadRequestKeyError('list')
    return username, list_type


def series_template():
    try:
        template = flask.request.args['template']
    except KeyError as e:
        try:
            preset = flask.request.args['preset']
        except KeyError:
            raise e
        else:
            try:
                template = malcat.config['series template presets'][preset]
            except KeyError:
                raise werkzeug.exceptions.BadRequestKeyError('preset')
    return template


def status_template():
    return flask.request.args.get('template', malcat.config['default header css'])


def status_args(list_type):
    statuses = collections.OrderedDict(
        (k, flask.request.args.get(k, v)) for k, v
        in malcat.config['list types'][list_type.lower()]['statuses']
    )
    return statuses