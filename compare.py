import os, csv


def createFile(path):
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)


def contains_disease(name):
    first = True
    contains = False
    mycsv_wikidata = csv.reader(open(compare_directory))
    for line in mycsv_wikidata:
        if first:
            first = False
        else:
            name1 = line[0]
            if name1.lower() == name.lower():
                contains = True
                break

    return contains

def also_known_diseases(name):
    first = True
    contains = False
    mycsv_wikidata = csv.reader(open(compare_directory))
    # iterate the csv file
    for line in mycsv_wikidata:
        if first:
            first = False
        else:
            also_known = line[also_pos] #get the name
            also_known_diseases = [elem.lower().replace(" ", "") for elem in also_known.split(",")]
            names = [elem.lower().replace(" ", "") for elem in name.split(",")]
            if len(names) == 1:
                if name.lower().replace(" ", "") in also_known_diseases:
                    contains = True
                    break
            else:
                for n in names:
                    if n.replace(" ", "") in also_known_diseases:
                        contains = True
                    else:
                        contains = False
                        break

    return contains


main_directory = "./results/babelNet_diseases (copia).csv"
compare_directory = "./results/diseases_info_en.csv"

#open csv files
mycsv_wikipedia = csv.reader(open(main_directory))
first = True
disease_name_pos = 2
also_pos = 21

rows = []
for line in mycsv_wikipedia:
    if first:
        first = False
        line.insert(disease_name_pos + 1, "Is it in Wikidata?")
        rows.append(line)
    else:
        name = line[disease_name_pos]
        if contains_disease(name) or also_known_diseases(name):
            line.insert(disease_name_pos + 1, "Yes")
        rows.append(line)

file_name = open(main_directory, 'w')
writer = csv.writer(file_name)
writer.writerows(rows)

