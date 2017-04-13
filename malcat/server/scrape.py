from google.appengine.api import urlfetch, urlfetch_errors

import malcat
from malcat.server import parse
from . import cache

URLFETCH_TIMEOUT = malcat.config.get('URLFETCH_TIMEOUT')
URLFETCH_USE_HTTPS = malcat.config.get('URLFETCH_USE_HTTPS')

MAL_API_URL = 'https://myanimelist.net/malappinfo.php'
MAL_API_USER_URL = MAL_API_URL + '?u={username}&type={list_type}&status=all'
MAL_USER_PROFILE_URL = 'https://myanimelist.net/profile/{username}'


def get(url):
    try:
        return urlfetch.fetch(
            url,
            deadline=URLFETCH_TIMEOUT,
            validate_certificate=URLFETCH_USE_HTTPS
        )
    except urlfetch_errors.InternalTransientError:
        # Oh, Google... Why...
        return get(url)


def user_list_url(username, list_type):
    return MAL_API_USER_URL.format(username=username, list_type=list_type)


def user_profile_url(username):
    return MAL_USER_PROFILE_URL.format(username=username)


@cache.memcache.decorate
def get_list(username, list_type):
    url = user_list_url(username, list_type)
    xml = get(url).content
    return parse.list_nodes(xml, list_type)


@cache.memcache.decorate
def get_status_info(username):
    url = user_profile_url(username)
    page_html = get(url).content
    return parse.status_info(page_html)
