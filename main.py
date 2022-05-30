import sys
from pathlib import Path

import yaml
from tomark import Tomark

# path to sigma rules
rules_path = sys.argv[1]


def load_yaml(path_string):
    path_iterable = Path(path_string).rglob('*.yml')
    final_list = []
    for p in path_iterable:
        with open(p) as yamlfile:
            d = yaml.load(yamlfile, Loader=yaml.FullLoader)
            d['parent'] = p.parent
            final_list.append(d)
    return final_list


def yaml_list_to_md_table(yaml_list):
    markdown = Tomark.table(yaml_list)
    return markdown


def yaml_list_to_md_page(yaml_list):
    rule_template = '''
    ### {title}
    - **description**: {description}
    - **category**: {parent}
    - **level**: {level}
    - **id**: {id}
    '''
    final_string = '''
    # List of covered sigma rules
    '''
    for i in yaml_list:
        rule_in_md = rule_template.format(
            title=i['title'],
            description=i['description'],
            parent=i['parent'],
            level=i['level'],
            id=i['id']
        )
        print(rule_in_md)
        final_string += rule_in_md
    return final_string



def write_to_file(markdown):
    with open('final_file.txt', 'w+') as final_file:
        final_file.write(markdown)


if __name__ == '__main__':
    loaded_yaml = load_yaml(rules_path)

    # 2 options: page or table output
    markdown = yaml_list_to_md_page(loaded_yaml)
    # markdown = yaml_list_to_md_table(loaded_yaml)

    write_to_file(markdown)



