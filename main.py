import sys
from pathlib import Path

import textwrap

import yaml
from tomark import Tomark


import json
# path to sigma rules
rules_path = sys.argv[1]

print('page vs table: page extracts selected fields and is availabe also as a PDF, '
      'table prints all fields and is available only as a markdown')
md_format = input('Specify markdown format: ("page" or "table"): ')
while md_format not in ['page', 'table']:
    print('You have specified markdown format: ', md_format)
    print('You have entered invalid option, type "page" or "table"')
    md_format = input('Specify markdown format: (page or table): ')


def load_yaml(path_string):
    path_iterable = Path(path_string).rglob('*.yml')
    final_list = []
    for p in path_iterable:
        with open(p) as yamlfile:
            d = yaml.load(yamlfile, Loader=yaml.FullLoader)

            parentpath = str(p.parent)
            parentpath = parentpath.split('/rules/')[-1]
            d['parent'] = parentpath

            rulepath = str(p)
            rulepath = rulepath.split('/rules/')[-1]
            d['path'] = rulepath

            final_list.append(d)
    return final_list


def yaml_list_to_md_table(yaml_list):
    markdown = Tomark.table(yaml_list)
    return markdown


def yaml_list_to_md_page(yaml_list):
    markdown_output_string = ''

    header_string = '''# Sigma Rules (Sigma HQ)
    '''

    category_template = '\n\n## {category}\n'

    rule_template = ('\n\n'
                     '### {title}\n'
                     '\n'
                     '{description}\n'
                     '\n'
                     '* Level: {level}\n'
                     )

    mitre_tags_template = '* MITRE: {tag}\n'
    mitre_tags_template_link = '* MITRE: [{tag_desc}]({tag_link})\n'

    references_template = '\n* [{reference}]({reference})'

    prev_category_string = ''
    new_category_string = ''


    markdown_output_string += header_string

    for i in yaml_list:

        new_category_string = i['parent']

        rule_string = rule_template.format(
            title=i['title'],
            description=i['description'],
            parent=i['parent'],
            level=i['level'],
            id=i['id'],
        )
        # print(i)
        # print('\n\n\n')

        references_string = ''
        if i.get('references') is not None:
            for j in i['references']:
                single_reference = references_template.format(reference=j)
                references_string += single_reference

        sigma_hq_reference = ('* [https://github.com/SigmaHQ/sigma/tree/master/rules/{path_desc}]'
                              ' (https://github.com/SigmaHQ/sigma/tree/master/rules/{path_link})'
                              .format(
                                path_desc=i['path'].replace('_', '\_'),
                                path_link=i['path']
                                ))

        mitre_string = ''
        if i.get('tags') is not None:
            for k in i['tags']:

                if k.split('.')[1][0] == 't':
                    ksplitted = k.split('.')
                    if len(ksplitted) == 3:
                        attack_link='https://attack.mitre.org/techniques/{tnum}/{tsubnum}'\
                            .format(tnum=ksplitted[1].capitalize(), tsubnum=ksplitted[2])
                    elif len(ksplitted) == 2:
                        attack_link = 'https://attack.mitre.org/techniques/{tnum}/'.format(tnum=ksplitted[1].capitalize())
                    else:
                        raise ValueError('Mitre tag is longer than expected: ', ksplitted)
                    mitre_link = mitre_tags_template_link.format(tag_desc=k.replace('_','\_'), tag_link=attack_link)
                    mitre_string += mitre_link

                elif k.split('.')[1][0] == 's':
                    sw_link='https://attack.mitre.org/software/{snum}/'.format(snum=ksplitted[1].capitalize())
                    mitre_link = mitre_tags_template_link.format(tag_desc=k.replace('_','\_'), tag_link=sw_link)
                    mitre_string += mitre_link

                else:
                    mitre_string += mitre_tags_template.format(tag=k).replace('_', '\_')

        final_string = ''

        if prev_category_string != new_category_string:
            final_string += category_template.format(category=new_category_string).replace('/', ' / ')
            prev_category_string = new_category_string

        final_string += rule_string
        final_string += mitre_string
        final_string += '\nReferences: \n\n'
        final_string += sigma_hq_reference
        final_string += references_string


        markdown_output_string += final_string

    return markdown_output_string

def write_to_file(markdown):
    with open('sigma_rules_summary.txt', 'w+') as final_file:
        final_file.write(markdown)


if __name__ == '__main__':
    loaded_yaml = load_yaml(rules_path)

    markdown = None

    if md_format == 'page':
        markdown = yaml_list_to_md_page(loaded_yaml)
    else:
        markdown = yaml_list_to_md_table(loaded_yaml)

    write_to_file(markdown)
    print('Your markdown file is ready in this directory under "sigma_rules_summary.txt" name')


