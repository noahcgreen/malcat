from collections import OrderedDict


def lxml_to_odict(elm):
    return OrderedDict([
        (node.tag, node.text)
        for node in elm
    ])
