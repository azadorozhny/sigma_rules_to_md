# Sigma rules to markdown summary


### How to run the script
Script takes a path to a directory containing sigma rules in the yaml format and outputs a single ''sigma_rules_summary.txt''' markdown file to the current directory.


<code>$ source venv/bin/activate </code>

<code>$ python main.py ./data/rules </code>

Output file contains:
- **rule name**
- **description** 
- **category level**
- **rule id**

### Input format
Script expects a directory with Sigma rules written in yaml format: [Sigma rules](https://github.com/SigmaHQ/sigma) 

### Output options
Output could be either a markdown file or a markdown table
To switch to a table output comment/uncomment yaml_list_to_page vs yaml_list_to_md_table in the code:

<code>
  if __name__ == '__main__':
    
    loaded_yaml = load_yaml(rules_path)

    # 2 options: page or table output
    markdown = yaml_list_to_md_page(loaded_yaml)
    # markdown = yaml_list_to_md_table(loaded_yaml)

    write_to_file(markdown)
</code>
