import io

from lxml import etree, html

import malcat


LIST_TYPES = malcat.config['list types']

STATUS_SELECTOR = '.stats-status li a + span'


def _remove_commas(string):
    return string.translate(None, ',')


class ParseError(Exception):
    pass


def list_nodes(xml, list_type):
    try:
        for _, node in etree.iterparse(io.BytesIO(xml), tag=list_type.lower()):
            yield {elem.tag: elem.text for elem in node}
            node.clear()
    except etree.XMLSyntaxError as e:
        raise ParseError(*e.args)


def status_info(page_html):
    page = html.fromstring(page_html)
    statuses = page.cssselect(STATUS_SELECTOR)
    return {
        media_type: [
            int(_remove_commas(status.text))  # remove commas
            for status in statuses[i * 5: (i + 1) * 5]
            ]
        for i, media_type in enumerate(LIST_TYPES)
        }
