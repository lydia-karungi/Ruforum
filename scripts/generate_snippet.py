import re


def generate_html(field_defs):
    snippet = open('file_field.html').read()
    generated = []
    for field_def in field_defs:
        print("field_def", field_def)
        output = snippet.replace('%label%', field_def['label'])
        output = output.replace('%name%', field_def['field_name'])
        generated.append(output)
    print('\n'.join(generated))


def run():
    f = open('fields.txt')
    label_regex = '\<label for=".*".*\>(?P<label>[^{]*)'
    label_regex = '\<legend.*\>(?P<label>.*)\</legend\>'
    field_name_regex = '\{\{.*form\.(?P<field_name>.*).*\}\}'
    field_defs = []
    field_def = {}
    for line in f:
        line = line.strip()
        match = re.search(label_regex, line)
        if match:
            label = match.group('label').strip()
            print(line)
            print("LABEL", label)
            field_def['label'] = label
        match = re.search(field_name_regex, line)
        if match and 'span' not in line:
            field_name = match.group('field_name').strip()
            print(line)
            print("FIELD NAME", field_name)
            field_def['field_name'] = field_name
            field_defs.append(field_def)
            field_def = {}

    print(field_defs)
    generate_html(field_defs)