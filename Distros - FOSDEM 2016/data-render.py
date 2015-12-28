#!/usr/bin/env python
# coding: utf-8

import yaml

import sys


with open('data.yaml') as f:
    data = yaml.load(f)


# Ideas for outputs:
#
# - Feature matrix
# - Examples
# - Artifact caching


ALL_FEATURES = [
    dict(
        id='syntax',
        title="Syntax",
    ),
    dict(
        id='full-distro',
        title="Complete OS",
        type=bool,
    ),
    dict(
        id='artifact-caching',
        title="Artifact caching",
        type='list',
    ),
    dict(
        id='cross-compile',
        title="Cross compilation",
        type=bool,
    ),
]


def feature_is_enabled(feature_id, entry):
    if feature_id in entry:
        value = entry[feature_id]
        if value is False:
            return False
        else:
            return True
    else:
        return False


def feature_matrix(data, features=ALL_FEATURES):
    table = []

    headers_row = ['Name']
    for info in features:
        headers_row.append(info['title'])
    table.append(headers_row)

    for item in data:
        row = []
        row.append(item['name'])

        for feature in features:
            feature_type = feature.get('type', 'str')
            if feature_type == bool:
                if feature_is_enabled(feature['id'], item):
                    row.append('✔')
                else:
                    row.append('✘')
            elif feature_type == 'list':
                values = item.get(feature['id'], [])
                if type(values) == dict:
                    values = values.keys()
                if type(values) == bool:
                    values = []
                else:
                    row.append(', '.join(v for v in values))
            else:
                row.append(item[feature['id']])

        table.append(row)

    return table


def ikiwiki_markdown_table(table):
    text_items = []
    for row in table:
        text_items.append(' | '.join(str(item) for item in row))

    tag = '[[!table data="""' + '\n'.join(text_items) + '"""]]'
    return tag


table = feature_matrix(data)
text = ikiwiki_markdown_table(table)
sys.stdout.write(text + '\n')
