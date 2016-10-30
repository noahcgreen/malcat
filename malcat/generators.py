import string


def css_per_series(user_list, list_type, template):
    """
    Yield a copy of template for each series in user_list,
    filled in with the appropriate values.

    PARAMS:
        * user_list: List of Dicts representing series.
        * list_type: anime or manga.
        * template: CSS string.
    """
    template = string.Template(template)
    id_key = 'series_{}db_id'.format(list_type)
    for i, series in enumerate(user_list):
        yield template.safe_substitute(
            **series,
            id=series[id_key],
            index=i,
            list=list_type
        )


def status_headers(headers, totals, template):
    """Yield a copy of template for each non-empty category,
    filled in with the category's header and index."""
    row_index = 2
    for header, total in zip(headers, totals):
        if total != 0:
            yield template.format(n=row_index, content=header)
            row_index += total
