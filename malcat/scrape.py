"""Functions for scraping data from MyAnimeList.net."""

import requests
from io import BytesIO
from lxml import etree
from collections import OrderedDict


def list_nodes(username, list_type, target):
    """Yield target nodes from a user's list as dictionaries.

    TODO:
        * Learn more about streaming and implement a better method.
    """
    base_url = 'http://myanimelist.net/malappinfo.php?u={}&status=all&type={}'
    response = requests.get(base_url.format(username, list_type))
    stream = BytesIO(response.content)
    dom = etree.iterparse(stream, tag=target)
    for event, node in dom:
        odict = OrderedDict([(elm.tag, elm.text) for elm in node])
        yield odict
        node.clear()
