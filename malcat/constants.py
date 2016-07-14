"""Constant string values used by the generators."""

from collections import OrderedDict

series_css_presets = {
    'more': '#more${id} { background-image: url($series_image); }',
    'animetitle': '.animetitle[href*="$list/$id/"] '
                  '{ background-image: url($series_image); }',
    'animetitlebefore': '.animetitle[href*="$list/$id/"]:before '
                        '{ background-image: url($series_image); }',
    'datatitle': '.data.title [href^="/$list/$id/"] '
                 '{ background-image: url($series_image); }',
    'datatitlebefore': '.data.title [href^="/$list/$id/"]:before '
                       '{ background-image: url($series_image); }'
}

status_header_templates = {
    'css': 'body[data-query*=\'"status":7\'] .list-item:nth-child({n}) '
           '.data.status:before {{ content: "{content}"; }}',
    'anime': OrderedDict([
        ('cw', 'Watching'),
        ('co', 'Completed'),
        ('oh', 'On Hold'),
        ('dr', 'Dropped'),
        ('ptw', 'Plan to Watch')
    ]),
    'manga': OrderedDict([
        ('cr', 'Reading'),
        ('co', 'Completed'),
        ('oh', 'On Hold'),
        ('dr', 'Dropped'),
        ('ptr', 'Plan to Read')
    ])
}

output_header = """\
/* MalCat - CSS generator for MyAnimeList.net */
/* Username: {username} | List type: {list_type} */
/* Template: {template} */
"""
