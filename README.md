# Ventriloquist-Ontology
Art project exploring biopolitics and the algorithmic governance of the human body

## Installation
1. Install most recent version of [python](https://www.python.org)
2. Once python is install type in the following command in your terminal `sudo pip install virtualenv`
3. Clone this repository
4. In your terminal, navigate to this repo
5. In the same terminal type and enter the following sequences of commands

`python3 virtualenv env`

`source env/bin/activate`

`pip install pdfminer.six`

`mkdir output`


6. Try running the following commands

This command will show you the available command line arguments and their functions

`python3 pdfparser.py -h`

This command should create an output file containing following sentence "I love to go swimming."

`python3 pdfparser.py -k love`

7. When finished with parser, type the following command

`deactivate`

## Running 

To start the venv navigate to the repository in your terminal and run following command 

`source env/bin/active`

To use the pdfparser run following command 

`python3 pdfparser.py [your args here]`

Once finished, run the following line

`deactivate`

