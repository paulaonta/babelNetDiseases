import os, csv
from urllib.request import urlopen
import bs4

def createFile(path):
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)

def createDirectory(path):
    if not os.path.exists(path):
        os.mkdir(path)

def contains_disease(link):
    first = True
    contains = False
    mycsv_wikidata = csv.reader(open(mydirname))
    for line in mycsv_wikidata:
        if first:
            first = False
        else:
            text = line[0]
            if len(text) != 0:
                if str(text) == link:
                    contains = True
                    break

    return contains

i, errorCount = 0, 0

directory = "./results"
createDirectory(directory)

# create a file to save all links for each letter
file_name = 'babelNet_diseases.csv'
mydirname = directory + "/" + file_name
createFile(mydirname)

# open the csv file
myFile = open(mydirname, 'w')
writer = csv.writer(myFile)
writer.writerow(['Link', 'Name'])
partial_link = 'http://babelnet.org/rdf/values/skos:narrower/'
codes = ['s00027546n']
i = 0
while i <= len(codes):
    try:
        # open the link
        link = partial_link + codes[i]
        soup = bs4.BeautifulSoup(urlopen(link), features="lxml")
        # find tags by CSS class
        content = soup.find("ul", class_="multi property-values unstyle")
        errorCount = 0
        i += 1

        ul = soup.find_all("ul", id=content)
        u = ul[0]
        li = u.find_all_next("li")
        for elem in li:
            if "li" in str(elem):
                link_tag = elem.find_next('a')
                link = link_tag.get('href')
                if 'page' in link and not contains_disease(link):
                    name = link.split('http://babelnet.org/rdf/page/')[1]
                    if name not in codes:
                        codes.append(name)
                    row = [link, name]
                    writer.writerow(row)
        i += 1
    except:
        errorCount += 1
        if errorCount == 5:
            print("error: an error occurs while opening the link: "+ link)
            errorCount = 0
            i += 1
        pass