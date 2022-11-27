import os, csv

diseases_left = './results/diseasesLeft'
myErrorFile = open(errors_path, 'a')
writerP = csv.writer(myErrorFile)
writerP.writerow(['name', 'link'])

def contains_disease(name_wiki, link):
    first = True
    contains = False
    mycsv_wikidata = csv.reader(open(mydirname))
    for line in mycsv_wikidata:
        if first:
            first = False
        else:
            text = line[wikiD_link_pos]
            name = line[0]
            if len(text) != 0:
                if str(text) == link or name.lower() == name_wiki.lower():
                    contains = True
                    break

    return contains

#open csv files
mycsv_wikipedia = csv.reader(open(wiki_directory))

rows = []
for line in mycsv_wikipedia:
    if first:
        first = False
        line.insert(wikiP_link_pos + 1, "Is it in Wikidata?")
        rows.append(line)
    else:
        link = line[wikiP_link_pos]
        name_wiki = line[0]
        if contains_disease(name_wiki, link) or also_known_diseases(name_wiki):
            line.insert(wikiP_link_pos + 1, "Yes")
        rows.append(line)

file_name = open(wiki_directory, 'w')
writer = csv.writer(file_name)
writer.writerows(rows)

#get diseases which are in wikipedia but not in wikidata
get_wikipedia_diseases()