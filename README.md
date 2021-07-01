# Ventriloquist-Ontology
Art project exploring biopolitics and the algorithmic governance of the human body

## Installation
1. Install most recent version of [python](https://www.python.org)
2. Be sure to run the command files inside of the python directory
3. Once python is install type in the following commands in your terminal 

`sudo pip3 install venv`

4. Clone this repository
5. In your terminal, navigate to this repo
6. In the same terminal type and enter the following sequences of commands

`python3 venv env`

`source env/bin/activate`

`pip3 install pdfminer.six`

`mkdir output`

`mkdir text`


7. Try running the following commands

This command will show you the available command line arguments and their functions

`python3 pdfparser.py -h`

This command should create an output file containing following sentence "I love to go swimming."

`python3 pdfparser.py -k love`

8. When finished with parser, type the following command

`deactivate`

## Running 

To start the venv navigate to the repository in your terminal and run following command 

`conda activate env`

To use the pdfparser run following command 

`conda deactivate`


