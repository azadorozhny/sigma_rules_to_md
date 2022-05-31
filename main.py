import sys
from pathlib import Path

import textwrap
from fpdf import FPDF

import yaml
from tomark import Tomark

# path to sigma rules
rules_path = sys.argv[1]

print('Page format extracts selected fields, table format prints all fields')
md_format = input('Specify markdown format: (page or table): ')
while md_format not in ['page', 'table']:
    print('You have specified markdown format: ', md_format)
    print('You have entered invalid option, type "page" or "table"')
    md_format = input('Specify markdown format: (page or table): ')

pdf_output = input('Do you want also a PDF output? ')
while pdf_output not in ['yes','no']:
    print('You have specified PDF option: ', pdf_output)
    print('You have entered invalid option, type "yes" or "no"')
    pdf_output = input('Specify if you want also a PDF output: (yes or no): ')

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
        # print(rule_in_md)
        final_string += rule_in_md
    return final_string

def text_to_pdf(text, filename):
    a4_width_mm = 210
    pt_to_mm = 0.35
    fontsize_pt = 10
    fontsize_mm = fontsize_pt * pt_to_mm
    margin_bottom_mm = 10
    character_width_mm = 7 * pt_to_mm
    width_text = a4_width_mm / character_width_mm

    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(True, margin=margin_bottom_mm)
    pdf.add_page()
    pdf.set_font(family='Courier', size=fontsize_pt)
    splitted = text.split('\n')

    for line in splitted:
        lines = textwrap.wrap(line, width_text)

        if len(lines) == 0:
            pdf.ln()

        for wrap in lines:
            pdf.cell(0, fontsize_mm, wrap, ln=1)

    pdf.output(filename, 'F')

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
    if pdf_output == 'yes':
        text_to_pdf(markdown, 'sigma_rules_summary.pdf')
        print('Your PDF file is ready in this directory under "sigma_rules_summary.pdf" name')
