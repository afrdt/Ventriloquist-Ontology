from logging import error
import os
import sys
import re
import argparse
import time
from typing import Set
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

#PDF to text Function. 
def pdf_to_text(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

def main():
  
  # pdf directory 
  textDir = clargs.directory

  # output directory 
  outputDir = clargs.output

  # list of all pdfs
  textList = os.listdir(textDir)
  
  # strings to be used for output filename
  textStr = ""
  keywordsStr = ""

  # keywords
  keywords = clargs.keywords

  for keyword in keywords:
    keywordsStr += keyword + "_"

  # get list of pdfs to scan
  if isinstance(clargs.text, list):
    textList = []
    for text in clargs.text:
      if (os.path.exists(textDir + text)):
        textList.append(text)
      else:
        print("Warning, the following file is not in the pdfs directory: " + text)
  
  for text in textList:
    textStr += text.replace(".txt", "_")
    textStr += text.replace(".pdf", "_")

  # set of all output from search results
  outputSet = {""}
  outputSet.remove("")
  resultList = []

  # find sentences containing specific output
  for i in range(len(textList)):
    text_output = textDir + textList[i]
    print("converting " + textList[i] + "...")
    extension = text_output[(len(text_output) - 3) : (len(text_output))]
    if extension == "txt":
      text_output = open(text_output)
      text_output = text_output.read()
    elif extension == "pdf":
      text_output = pdf_to_text(text_output)
    else:
      raise Exception("file must be either .pdf or .txt")
    print("searching " + textList[i] + " for...")
    for j in range(len(keywords)):
      print("  " + keywords[j], end=(''))
      resultSet = {""}
      resultSet.remove("")
      prog = re.compile("[^.?!]*(?<=[.?\s!])" + keywords[j] + "(?=[\s.?!])[^.?!]*[.?!]", re.IGNORECASE)
      result = prog.findall(text_output)
      print("  " + str(len(result)) + " matches")
      for k in range(len(result)):
        trimmedResult = result[k].replace("\n", "").strip()
        resultSet.add(trimmedResult)
        outputSet.add(trimmedResult)
      resultList.append(resultSet)

  # only keep results containing all words
  if clargs.searchmode == "and":
    print("finding results containing all words...")
    for i in range(len(resultList)):
      outputSet.intersection_update(resultList[i])

  # create timestamps
  reformattedTime = time.localtime(time.time())
  reformattedTime = time.asctime(reformattedTime)
  reformattedTime = reformattedTime.replace("  ", " ")
  reformattedTime = reformattedTime.replace(" ", "_")

  print("outputing results to " + reformattedTime + "./txt")
  outputStr = "date: " + reformattedTime + "\n"
  outputStr += "files: " + str(textList) + "\n"
  outputStr += "keywords: " + str(keywords) + "\n"
  outputStr += "searchmode: " + clargs.searchmode + "\n\n"

  outputStr += "output" + "\n"
  outputStr += "----------------------------" + "\n\n"

  # add found sentences
  for sentence in outputSet:
    outputStr += sentence + "\n\n"

  outputStr += "----------------------------" + "\n"

  # write results to output file
  f = open(outputDir + reformattedTime + ".txt", "w") 
  f.write(outputStr)
  f.close()

  print("parse complete")

def parse_args(defaults):
    """ 
    Parse command line arguments.

    Parameters
    ----------
    defaults : dict
        A dictionary with default values for the command line arguments

    Returns
    -------
    clargs : argparse.ArgumentParser 
        The object with the parsed command line arguments
    """

    # set up parser for command line arguments
    parser = argparse.ArgumentParser(description="Extracts sentences containing keywords from pdfs and txt. Output will be saved in output directory as text file with the following name -> [current time].txt.")

    # Name of text file / list of text files to be parsed, must be inside 'text' directory, by default will search all text files in 'text' directory
    parser.add_argument("-t", "--text", action="store", dest="text", type=str, nargs="+", required=False,
                        default=defaults["text"], 
                        help="Name of text file / list of text files to be parsed, must include extension."
                        + "By default will search all files")

    # Path of directory containing text files. Default is "/text/"
    parser.add_argument("-d", "--directory", action="store", dest="directory", type=str, required=False,
                        default=defaults["directory"], 
                        help="Name of directory containing pdf files. Default is \"./text/\"")

    # Path of directory containing output. Default is "./output/", 
    parser.add_argument("-o", "--output", action="store", dest="output", type=str, required=False,
                        default=defaults["output"], 
                        help="Output file path. Default is \"./output/\"")
    
    # Keyword / list of keywords to be searched for. 
    parser.add_argument("-k", "--keywords", action="store", dest="keywords", type=str, required=True, nargs="+",
                        default=defaults["keywords"], 
                        help="Keyword / list of keywords to be searched for. Must be included.")

    # search mode
    parser.add_argument("-s", "--searchmode", action="store", dest="searchmode", type=str, required=False,
                        default=defaults["searchmode"], 
                        help="Specifies how sentences will be extracted from pdf when multiple keywords are entered. Available modes:"
                        + " and - sentences extracted contain all specified keywords,"
                        + " or - sentences extracted contain any specified keyword."
                        + " Default is or")

    clargs = parser.parse_args()
    return clargs 

if __name__ == "__main__":

    # set some default values 
    defaults = {
      "text": "all",
      "keywords": "",
      "directory": "./text/",
      "output": "./output/",
      "searchmode": "or"
    }

    # parse the arguments
    clargs = parse_args(defaults)

    print("starting parser")
    
    # run main function
    main()
