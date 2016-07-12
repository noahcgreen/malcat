"""Functions for scraping data from MyAnimeList.net."""

import requests
import requests_cache
from io import BytesIO
from lxml import etree
from collections import OrderedDict
import redis
import os

redis_conn = redis.from_url(os.environ['REDIS_URL'])


requests_cache.install_cache('malcat_cache',
                             backend='redis',
                             expire_after=900,
                             old_data_on_error=True,
                             connection=redis_conn)


def list_nodes(username, list_type, target):
    """Yield target nodes from a user's list as dictionaries.

    TODO:
        * Learn more about streaming and implement a better method.
    """
    base_url = 'http://myanimelist.net/malappinfo.php?u={}&status=all&type={}'
    response = requests.get(base_url.format(username, list_type))
    stream = BytesIO(response.content)
    for event, node in etree.iterparse(stream, tag=target):
        yield OrderedDict([(elm.tag, elm.text) for elm in node])
