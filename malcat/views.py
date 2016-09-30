from collections import OrderedDict

from flask import request, render_template
from werkzeug.exceptions import BadRequestKeyError

from malcat import app, CONFIG
from malcat.cache import client_cache
from malcat.helpers import (
    package_css,
    get_list_identifiers,
    get_series_template,
    get_status_args
)
from malcat.scrape import MALScraper
from malcat.css import template_per_series, template_per_status


@app.route('/')
@client_cache()
def index():
    return render_template('index.html')


@app.route('/series')
@client_cache(max_age=900)
@package_css
def series():
    username, list_type = get_list_identifiers()
    template = get_series_template()
    user_list = MALScraper.user_list(username, list_type)
    css = template_per_series(template, user_list, list_type)
    return '\n'.join(css)


@app.route('/headers')
@client_cache(max_age=900)
@package_css
def headers():
    username, list_type = get_list_identifiers()
    user_info = MALScraper.user_info(username, list_type)
    statuses = OrderedDict(
        (header, total) for header, total in zip(
            get_status_args(list_type).values(),
            map(int, user_info.values()[2:7])
        )
    )
    template = request.args.get('template', CONFIG['default header css'])
    css = template_per_status(template, statuses)
    return '\n'.join(css)


@app.errorhandler(BadRequestKeyError)
@package_css
def handle_missing_argument(e):
    return 'Missing argument: {}'.format(e.args[0])
