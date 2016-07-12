"""Generators for processing list data.

TODO:
    * Remove extra for loops.
"""


def css_per_series(user_list, list_type, template):
    """Yield a copy of template for each series in user_list,
    filled in with the appropriate values."""
    id_key = 'series_{}db_id'.format(list_type)
    for i, series in enumerate(user_list):
        yield template.safe_substitute(**series,
                                       id=series[id_key],
                                       image=series['series_image'],
                                       index=i,
                                       list=list_type)


def status_headers(categories, template):
    """Yield a copy of template for each non-empty category,
    filled in with the category's header and index."""
    row_index = 2
    for header, total in categories:
        if total != 0:
            yield template.format(n=row_index, content=header)
        row_index += total
