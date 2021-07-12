# Ventriloquist-Ontology
Art project exploring biopolitics and the algorithmic governance of the human body

## Installation
1. Install most recent version of [anaconda](https://www.anaconda.com)
2. Install most recent version of [python](https://www.python.org)
3. Run scripts inside of python application directory
4. Type in the following command in your terminal to verify conda and python are installed

`conda -V`

`python3`

3. If conda is not found, type in the following command in your terminal 

`export PATH=~/opt/anaconda3/bin`

4. Clone this repository

`git clone https://github.com/afrdt/Ventriloquist-Ontology.git`

6. In your terminal, navigate to this repo
7. In the same terminal type and enter the following sequences of commands

`conda create --name env python=3.9`

`source activate env`

`conda install pip`

`sudo pip install pdfminer.six`

7. Verify pdfminer.six is install by running the following command and looking for **pdfminer.six**

`conda list`

8. Try running the following commands

This command will show you the available command line arguments and their functions

`python3 parse.py -h`

This command should create an output file containing following sentence "I love to go swimming."

`python3 parse.py -t (name of text file / list of text files to be parsed, must include extension) -k love`

9. When finished with parser, type the following command

`conda deactivate`

## Running 

To start the venv navigate to the repository in your terminal and run following command 

`conda activate env`

To exit the pdfparser run following command 

`conda deactivate`


