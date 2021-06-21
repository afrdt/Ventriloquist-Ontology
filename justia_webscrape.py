import requests
from bs4 import BeautifulSoup


baseURL = 'https://law.justia.com'
laws = {""}
laws.remove("")

def printAllListings(base, extension, laws):
  url = base + extension
  page = requests.get(url)
  soup = BeautifulSoup(page.content, 'html.parser')
  lawUrls = soup.find('div', {"class": "codes-listing"})
  if lawUrls is not None:
    codeUrls = lawUrls.find_all('a')
    if codeUrls is not None:
      for codeUrl in codeUrls:
        printAllListings(base, codeUrl['href'], laws)
  else: 
    law = soup.find('div', {"id": "codes-content"})
    if law is not None:
      pLaws = law.find_all('p')
      if pLaws is not None:
        lawTxt = ""
        for p in pLaws:
          lawTxt += p.text + "\n"
        print(lawTxt)
        laws.add(lawTxt)

printAllListings(baseURL, '/codes/washington/2019/', laws)

lawOutput = ""
for law in laws:
  lawOutput += law

f = open('./txt/justia_output.txt', 'w')
f.write(lawOutput)
f.close()

# lawURLs = soup.find('div', {"class": "codes-listing"})

# while (len(codeUrls()) != 0)
# codeUrls = lawURLs.find_all('a')

# for codeURL in codeUrls:
#   print(codeURL['href'])

