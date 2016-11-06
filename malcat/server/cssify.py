def template_per_series(template, series_list, list_type):
    list_type = list_type.lower()
    id_key = 'series_{}db_id'.format(list_type)
    for i, series in enumerate(series_list):
        yield template.safe_substitute(
            id=series[id_key],
            index=i,
            list=list_type,
            **series
        )

LIST_DATA_START_INDEX = 2


def template_per_status(template, *statuses):
    row_index = LIST_DATA_START_INDEX
    for header, total in statuses:
        if total != 0:
            yield template.safe_substitute(index=row_index, content=header)
        row_index += total
