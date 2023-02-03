#!/usr/bin/env python
# coding: utf-8

import yaml

import os
import re
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


def the_7_commandments_pinpoint(entry):
    '''Mark a build+integration language against the "7 commandments":

        - Keep all data in one place
        - Use YAML
        - Version the format
        - Write multiple tools
        - Specify the syntax/structure
        - Specify the data model
        - Keep track of variance

    '''
    def strip_markdown(text):
        markdown_link_match = '(.*)\[(.*)\]\(.*\)(.*)'
        match = re.match(markdown_link_match, text)
        if match:
            return strip_markdown(match.group(1) + match.group(2) + match.group(3))
        else:
            return text

    def good(text):
        return '<span color="lightgreen">✔ ' + text + '</span>'
    def bad(text):
        return '<span color="red">✘ ' + text + '</span>'
    def ok(text):
        return text

    text_lines = []

    name = strip_markdown(entry['name'])

    images = entry.get('images', [])
    image = None
    for image in images:
        if not os.path.exists(image):
            raise RuntimeError("Image missing: %s" % image)

        text_lines.append('--- [%s]' % image)
        text_lines.append(name)

    text_lines.append('---')
    text_lines.append('<b><u>%s</u></b>\n' % name)

    # This one's for the speaker
    users = entry.get('users')
    text_lines.append("# %s" % users)

    data_in_one_place = entry.get('data-in-one-place')
    if data_in_one_place:
        text_lines.append(good('Data all in one place'))
    else:
        text_lines.append(bad('Data in different repos'))

    syntax_list = entry.get('syntax')
    if type(syntax_list) == str:
        syntax_list = [syntax_list]
    for syntax in syntax_list:
        syntax = strip_markdown(syntax)
        if syntax == 'YAML':
            text_lines.append(good('Syntax: YAML'))
        elif syntax in ['XML', 'JSON', 'XML or YAML'] or syntax.startswith('Key-value'):
            text_lines.append(ok('Syntax: %s' % syntax))
        else:
            text_lines.append(bad('Syntax: %s' % syntax))

    versioned = entry.get('versioned')
    if versioned:
        if versioned.startswith('yes'):
            text_lines.append(good('Versioned: %s' % versioned))
        elif versioned.startswith('no'):
            text_lines.append(bad('Versioned: %s' % versioned))
        else:
            text_lines.append(ok('Versioned: %s' % versioned))

    structure_specified = entry.get('schemas')
    if structure_specified == '?':
        pass
    elif structure_specified:
        text_lines.append(good('Structure specified'))
    else:
        text_lines.append(bad('Syntax/structure not specified'))

    data_model_specified = entry.get('data-model')
    if data_model_specified:
        text_lines.append(good('Data model specified'))
    else:
        text_lines.append(bad('Data model not specified'))

    return '\n'.join(text_lines)


def the_7_commandments_table(data):
    features = [
        'Data in one place',
        'Syntax',
        'Versioned',
        'Syntax/structure',
        'Data model'
    ]

    def yes():
        return "✔"
    def no():
        return "✘"

    table = []

    headers_row = ['Name']
    for info in features:
        headers_row.append(info)
    table.append(headers_row)

    for item in data:
        row = []
        row.append(item['name'])

        data_in_one_place = item.get('data-in-one-place')
        if data_in_one_place:
            row.append(yes())
        else:
            row.append(no())

        syntax_list = item.get('syntax')
        if type(syntax_list) == str:
            syntax_list = [syntax_list]
        row.append(', '.join(syntax_list))

        versioned = item.get('versioned')
        if versioned:
            if versioned.startswith('yes'):
                row.append(yes())
            elif versioned.startswith('no'):
                row.append(no())

        structure_specified = item.get('schemas')
        if type(structure_specified) == list:
            structure_list = structure_specified
        else:
            structure_list = [structure_specified]
        items = []
        for structure in structure_list:
            if structure == '?':
                items.append('?')
            elif structure:
                if str(structure).startswith('http://'):
                    items.append('[%s](%s)' % (yes(), str(structure)))
                else:
                    items.append(str(structure))
            else:
                items.append(no())
        row.append(', '.join(items))

        data_model_specified = str(item.get('data-model'))
        if data_model_specified:
            if data_model_specified.startswith('http://'):
                items.append('[%s](%s)' % (yes(), data_model_specified))
            else:
                items.append(data_model_specified)
        else:
            row.append(no())

        table.append(row)
    return table


# Dump the feature matrix table to ikiwiki markdown
#
#table = feature_matrix(data)
#text = ikiwiki_markdown_table(table)
#sys.stdout.write(text + '\n')

# Create a pinpoint slideshow of distro build+integration languages
#pages = []
#for entry in data:
#    if 'images' in entry:
#        text = the_7_commandments_pinpoint(entry)
#        pages.append(text)
#sys.stdout.write('\n'.join(pages) + '\n')


table = the_7_commandments_table(data)
text = ikiwiki_markdown_table(table)
sys.stdout.write(text + '\n')
