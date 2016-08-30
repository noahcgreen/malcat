"""Functions for scraping data from MyAnimeList.net."""

from io import BytesIO
from collections import OrderedDict

import requests
from lxml import etree

from malcat import cache  # Enable requests_cache

MAL_API = 'https://myanimelist.net/malappinfo.php?u={user}&type={type}'


def request_user_list(username, list_type):
    url = MAL_API.format(user=username, type=list_type)
    return requests.get(url)


def get_select_list_nodes(username, list_type, tag=None):
    """Shortcut for grabbing specific elements from a list."""
    request = request_user_list(username, list_type)
    stream = BytesIO(request.content)
    for _, elm in etree.iterparse(stream, tag=tag):
        yield elm
        elm.clear()
