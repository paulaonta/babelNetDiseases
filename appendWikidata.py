from SPARQLWrapper import SPARQLWrapper, JSON, N3, XML, CSV
import os
import numpy
from qwikidata.sparql import (get_subclasses_of_item,
                              return_sparql_query_results)
from urllib.request import urlopen
import bs4
import csv

#define variables
languages = ['en', 'es', 'fr', 'ca', 'eu']
codes = ["disease", "symptoms", "treatment", "differentFrom" , "risk" , "cause", "diagnosis"]
babelnet_file = "./results/babelNet_diseases.csv"
errorsFile_path = "./results/errorsWikidata.csv"
link_first_part = "https://www.wikidata.org/w/index.php?search="
link_second_part  = "+-article+-trial&title=Special:Search&profile=advanced&fulltext=1&advancedSearch-current=" \
                    "{\"fields\"%3A{\"not\"%3A[\"article\"%2C\"trial\"]}}&ns0=1&ns120=1"

sparql = SPARQLWrapper("https://query.wikidata.org/")

mycsv = csv.reader(open(babelnet_file)) #open

myFile = open(errorsFile_path, 'a')
myErrorFile = csv.writer(myFile)
myErrorFile.writerow(['name', 'code'])

first = True

def convertDictToArray(res):
    select_term = ""
    i = 0
    first_row = []
    array = []
    for result in res["head"]["vars"]:
        select_term = result
        array.insert(i, [])
        # this is the first row of the csv file
        first_row.append(result)
        for r in res["results"]["bindings"]:
            try:
                string1 = r[select_term]["value"]
                array[i].append(string1)
            except:
                array[i].append(" ")
                pass
        i += 1

    return first_row, array

def getValues(first_row, array):
    lista = []
    lista.append(array[0][0])
    for j in range(1, len(first_row)):
        if first_row[j] in codes:
            unique_values = numpy.unique(array[j])
            if ' ' not in unique_values:
                aux = [elem.split("http://www.wikidata.org/entity/")[1] for elem in unique_values]
            else:
                aux = unique_values
        else:
            aux = numpy.unique(array[j])
        string = ",".join(aux)
        lista.append(string.replace(';', ','))
    return lista

def makeQuery(query):
    res = return_sparql_query_results(query)
    first_row, prop = convertDictToArray(res)
    return first_row, prop

def createFile(path):
    mydirname = './' + path
    if not os.path.exists(mydirname):
        os.makedirs(os.path.dirname(mydirname), exist_ok=True)

def main_query(prop_num, lang):
    return  '''SELECT DISTINCT ?diseaseLabel ?disease ?symptomsLabel ?symptoms ?treatmentLabel ?treatment 
            ?differentFromLabel ?differentFrom ?riskLabel ?risk ?causeLabel ?cause  ?diagnosisLabel ?diagnosis
            ?icd9 ?icd10 ?umls ?mesh ?nci ?link ?description ?alsoKnownAs
             WHERE {
                ?disease wdt:* wd:''' + prop_num + '''.
              OPTIONAL { ?disease wdt:P780 ?symptoms. }
              OPTIONAL { ?disease wdt:P2176 ?treatment. }
              OPTIONAL { ?disease wdt:P1889 ?differentFrom. }
              OPTIONAL { ?disease wdt:P5642 ?risk. }
              OPTIONAL { ?disease wdt:P828 ?cause. }
              OPTIONAL { ?disease wdt:P923 ?diagnosis. }
              OPTIONAL { ?disease wdt:P1692 ?icd9. }
              OPTIONAL { ?disease wdt:P4229 ?icd10. }
              OPTIONAL { ?disease wdt:P2892 ?umls. }
              OPTIONAL { ?disease wdt:P486 ?mesh. }
              OPTIONAL { ?disease wdt:P1748 ?nci. } 
              OPTIONAL {
              ?link schema:about ?disease .
              ?link schema:inLanguage "''' + lang + '''".
              ?link schema:isPartOf <https://''' + lang + '''.wikipedia.org/> .
              }
              OPTIONAL{
              ?disease schema:description ?description. 
              FILTER(LANG(?description) = "''' + lang + '''")
              }
              OPTIONAL{
              ?disease skos:altLabel ?alsoKnownAs. 
              FILTER(LANG(?alsoKnownAs) = "''' + lang + '''")
              }
                SERVICE wikibase:label { bd:serviceParam wikibase:language "''' + lang + '''". }
            }           
            '''

def not_codes():
    sparql_query = ''' SELECT ?item2 ?itemLabel 
                            WHERE {                                    
                               { ?item (wdt:P279*) wd:Q65091757.}
                                UNION
                               { ?item (wdt:P279*) wd:Q8294850.}#physiological plant disorders 
                               UNION
                               { ?item (wdt:P279*) wd:Q9190427.} #animal diseases
                               UNION
                               {?item (wdt:P279*) wd:Q207791.} 
                               UNION
                                {?item (wdt:P279*) wd:Q31208391.} 
                                UNION
                                {?item (wdt:P279*) wd:Q133780.} 
                                 UNION
                                {?item (wdt:P279*) wd:Q3241045.} 
                                UNION
                                {?item (wdt:P279*) wd:Q223393.} 
                               ?item2 (wdt:P31) ?item. # instance of
                            }'''
    first_row, prop = makeQuery(sparql_query)
    final_prop_code = [elem.split("http://www.wikidata.org/entity/")[1] for elem in prop[0]]
    # we want to delete the diseases with this codes because there aren't human diseases
    codes = ['Q102322953', 'Q17450153', 'Q7002141', 'Q2662861', 'Q26842138', 'Q2040895', 'Q3049298', 'Q749342',
             'Q30912812', \
             'Q109270553', 'Q109353029', 'Q2597715', 'Q96414735', 'Q1553361', 'Q97184013', 'Q738101', 'Q89498598',
             'Q66424263', \
             'Q4684101', 'Q66424104', 'Q1329680', 'Q207066', 'Q1092510', 'Q1759544', 'Q7822519', 'Q492728', 'Q24628669', \
             'Q1758551', 'Q5467519', 'Q1799748', 'Q41808675', 'Q75393351', 'Q43405', 'Q5142432', 'Q5750929', 'Q315940', \
             'Q29310572', 'Q57620918', 'Q7263711', 'Q20917015', 'Q7272353', 'Q15761553', 'Q7272353']
    final_prop_code.extend(codes)
    return final_prop_code

def getDisease(prop_code):
    for lang in languages:
        csv_path = './results/diseases_info_' + lang + '.csv'
        errors_path = './results/errors_log_' + lang
        first = True
        i, errorCount = 0, 0
        lista2 = []

        # create csv file for each language
        createFile(csv_path)
        # create file to save the errors for each language
        createFile(errors_path)

        # open the csv file
        myFile = open(csv_path, 'a')
        writer = csv.writer(myFile)

        # for each property
        while i < len(prop_code):
            prop_num = prop_code[i]  # get the property
            try:
                sparql_query_main = main_query(prop_num, lang)
                first_row, array = makeQuery(sparql_query_main)

                if first:
                    first = False
                errorCount = 0
                i += 1
                if array[0]:  # if it is not empty
                    lista = getValues(first_row, array)
                    lista2.append(lista)
            except:
                errorCount += 1
                if errorCount == 10:
                    # append in the logger
                    myErrorFile = open(errors_path, 'a')
                    myErrorFile.write("This disease: " + prop_num + " can't be load\n")
                    errorCount = 0
                    i += 1
                print("error")
                pass

        writer.writerows(lista2)

#iterate the csv file
prop_code = []

#first define the codes which we are not interested in
not_codes = not_codes()

for line in mycsv:
    if first:
        first = False
    else:
        name_parts = line[2].split("_")
        wikidata_in = line[3]
        index = 0
        if wikidata_in != "Yes": #search only the diseases that are not in Wikidaa corpus
            link_disease_part = ""
            while index < len(name_parts):
                if index == len(name_parts)-1:
                    link_disease_part += name_parts[index].lower()
                else:
                    link_disease_part += name_parts[index].lower() + "+"
                index += 1

            link = link_first_part + link_disease_part[0:len(link_disease_part)] + link_second_part

            try:
                # open the link
                soup = bs4.BeautifulSoup(urlopen(link), features="lxml")
                # find tags by CSS class
                content = soup.find("ul", class_="mw-search-results").find_all('a')[0]
                code = content.getText().split('(')[1].split(')')[0]
                if code not in not_codes:
                    prop_code.append(code)

            except:
                print("error: an error occurs while searching the disease")
                # append in the logger
                myFile = open(errorsFile_path, 'a')
                myErrorFile = csv.writer(myFile)
                myErrorFile.writerow([line[2], line[1]])
                pass

getDisease(prop_code)
