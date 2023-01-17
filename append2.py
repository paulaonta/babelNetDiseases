from babelnetpy.babelnet import BabelNet
import csv
bn = BabelNet('c827b8cc-2c5b-4fe1-b23d-ca9fd9455707')

mydirname = "./results/babelNet_diseases.csv"
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
        try:
            text = line[code_pos] #get the code
            synset = bn.getSynsets("bn:"+text[1:])
            name = synset[0].senses[0]['properties']['fullLemma']
            line.insert(code_pos + 1, name)
        except:
            print(text)
            pass

    csv_array.append(line)

# insert the new symptoms in the csv
myFile = open(mydirname, 'w')
writer = csv.writer(myFile)
writer.writerows(csv_array)

