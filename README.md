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
Script can output parsed info in a  markdown format in "page" or "table" style as a txt file and pdf file.  
After you run the script, it will prompt you for the output style and format.  


**Script prompt example**:


`$ python main.py ./data/test/`

`Page format extracts selected fields, table format prints all fields`

`Specify markdown format: (page or table): page`

`Do you want also a PDF output? yes`

`Your markdown file is ready in this directory under "sigma_rules_summary.txt" name`

`Your PDF file is ready in this directory under "sigma_rules_summary.pdf" name`

### How to generate a Mitre att&ck navigator heatmap
(1) Install sigma tools: `pip3 install sigmatools`

(2) Run sigma2attack:

**Use the default "rules" directory**
 `sigma2attack`

**... or specify your own directory**
`sigma2attack --rules-directory ~/hunting/rules`

more info about sigma2attack is available on their repo: [sigma2attack repo](https://github.com/SigmaHQ/sigma#sigma2attack)
