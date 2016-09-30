"""Parse MAL data to Python structures."""

import io
from collections import OrderedDict

from lxml import etree


def selectively_parse(xml, tag=None):
    """
    Grab specific nodes from XML so that the entire document doesn't
    need to be brought into memory at once.
    """
    for _, node in etree.iterparse(io.BytesIO(xml), tag=tag):
        yield OrderedDict((elm.tag, elm.text) for elm in node)
        node.clear()
