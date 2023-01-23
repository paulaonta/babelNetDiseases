import os, csv


def createFile(path):
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)


def contains_disease(name, directory):
    first = True
    contains = False
    mycsv_wikidata = csv.reader(open(directory))
    for line in mycsv_wikidata:
        if first:
            first = False
        else:
            name1 = line[0]
            if name1.lower().replace(" ","") == name.lower().replace("_",""):
                contains = True
                break

    return contains

def also_known_diseases(name, directory):
    first = True
    contains = False
    mycsv_wikidata = csv.reader(open(directory))
    # iterate the csv file
    for line in mycsv_wikidata:
        if first:
            first = False
        else:
            also_known = line[also_pos] #get the name
            also_known_diseases = [elem.lower().replace(" ", "") for elem in also_known.split(",")]
            if name.lower().replace("_", "") in also_known_diseases:
                contains = True
                break


    return contains


main_directory = "./results/babelNet_diseases.csv"
compare_directory = ["./results/diseases_info_en.csv","./results/diseases_info_es.csv", "./results/diseases_info_fr.csv"]

#open csv files
mycsv_wikipedia = csv.reader(open(main_directory))
first = True
disease_name_pos = 2
also_pos = 21

for directory in compare_directory:
    rows = []
    for line in mycsv_wikipedia:
        if first:
            first = False
            line.insert(disease_name_pos + 1, "Is it in Wikidata?")
            rows.append(line)
        else:
            name = line[disease_name_pos]
            if directory == "./results/diseases_info_en.csv":
                if contains_disease(name, directory) or also_known_diseases(name, directory):
                    line.insert(disease_name_pos + 1, "Yes")
            else: #see if the disease is in other language
                wikidata = line[disease_name_pos + 1]
                if wikidata != "Yes":
                    if contains_disease(name) or also_known_diseases(name):
                        line.insert(disease_name_pos + 1, "Yes")
            rows.append(line)

    file_name = open(main_directory, 'w')
    writer = csv.writer(file_name)
    writer.writerows(rows)

