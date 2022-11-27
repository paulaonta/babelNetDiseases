import os, csv
from urllib.request import urlopen
import bs4
i, errorCount = 0, 0

mydirname = "./results/babelNet_diseases.csv"
partial_link = 'https://babelnet.org/synset?id=bn%3A'
partial_link2 = '&lang=EN'
code_pos = 1
i = 0

mycsv = csv.reader(open(mydirname))
first = True
csv_array = []
#for each line in the csv file
for line in mycsv:
    i, errorCount = 0, 0
    if first:
        first = False
        line.insert(code_pos+1, "Disease Name")
    else:
        text = line[code_pos] #get the code
        try:
            # open the link
            link = partial_link + text[1:] + partial_link2
            soup = bs4.BeautifulSoup(urlopen(link), features="lxml")
            # find tags by CSS class
            content = soup.find("span", class_="synonim")
            errorCount = 0
            i += 1

            span = soup.find_all("span", id=content,  class_="synonim")
            name = span[0].text
            line.insert(code_pos + 2, name)
        except:
            errorCount += 1
            if errorCount == 5:
                print("error: an error occurs while opening the link: " + link)
                errorCount = 0
                i += 1
            pass
    csv_array.append(line)

# insert the new symptoms in the csv
myFile = open(mydirname, 'w')
writer = csv.writer(myFile)
writer.writerows(csv_array)
