import io

from google.appengine.api import urlfetch, urlfetch_errors
from lxml import etree, html

import malcat
from malcat.server import cache


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


@cache.cache_list
def get_list(username, list_type):
    url = user_list_url(username, list_type)
    xml = get(url).content
    for _, node in etree.iterparse(io.BytesIO(xml), tag=list_type.lower()):
        yield {elem.tag: elem.text for elem in node}
        node.clear()


@cache.cache_status_info
def get_status_info(username):
    url = user_profile_url(username)
    page_html = get(url).content
    page = html.fromstring(page_html)
    statuses = page.cssselect('.stats-status li a + span')
    return {
        media_type: [
            int(status.text.translate(None, ','))  # remove commas
            for status in statuses[i * 5: (i + 1) * 5]
            ]
        for i, media_type in enumerate(malcat.config['list types'])
    }
