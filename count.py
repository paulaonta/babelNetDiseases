import csv

file_name = './results/babelNet_diseases.csv'
mycsv = csv.reader(open(file_name))
first = True
cont = 0
#for each line in the csv file
for line in mycsv:
    if first:
        first = False
    else:
        wikidata = line[3]
        if wikidata != "Yes":
            cont += 1

print(cont)
