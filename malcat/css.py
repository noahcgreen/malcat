import string


def template_per_series(template, series_list, list_type):
    template = string.Template(template)
    list_type = list_type.lower()
    id_key = 'series_{}db_id'.format(list_type)
    for i, series in enumerate(series_list):
        yield template.safe_substitute(
            id=series[id_key],
            index=i,
            list=list_type,
            **series
        )


def template_per_status(template, statuses):
    template = string.Template(template)
    # Start at second row (first is sort menu)
    row_index = 2
    for header, total in statuses.items():
        if total != 0:
            yield template.safe_substitute(i=row_index, content=header)
        # Advance to next status
        row_index += total
