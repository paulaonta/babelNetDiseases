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
request = True
csv_array = []
#for each line in the csv file
for line in mycsv:
    errorCount = 0
    if first:
        first = False
        line.insert(code_pos+1, "Disease Name")
    else:
        if request:
            text = line[code_pos] #get the code
            try:
                # open the link
                link = partial_link + text[1:] + partial_link2
                soup = bs4.BeautifulSoup(urlopen(link), features="lxml")
                # find tags by CSS class
                if soup.find("span", class_="synonim") != None:
                    content = soup.find("span", class_="synonim")
                    #print(soup.find_all("div", class_="alert alert-danger")[0].text)
                    name = content.text
                    errorCount = 0
                    print("sa")
                    #span = soup.find_all_next("span", class_="synonim")
                    #print(span)
                    #name = span[0].text
                    line.insert(code_pos + 1, name)

                elif "Daily request limit reached" in soup.find_all("div", class_="alert alert-danger")[0].text:
                    print("Daily request limit reached")
                    request = False
                else:
                    print("An other problem")
            except:
                errorCount += 1
                if errorCount == 5:
                    print("error: an error occurs while opening the link: " + link)
                    errorCount = 0
                pass
        else:
            line.insert(code_pos + 1, "null")
    csv_array.append(line)

# insert the new symptoms in the csv
myFile = open(mydirname, 'w')
writer = csv.writer(myFile)
writer.writerows(csv_array)
