from bs4 import BeautifulSoup
import csv
import urllib

# Script for getting all the ideas, from the vosLoHaces contest
categories = { "diseno": 0, "educacion": 0, "imp. ambiental": 0, "imp. social": 0, "turismo y gastronomia": 0 }

outputFile  = open('vosLoHaces.csv', "wb")
writer = csv.writer(outputFile, delimiter='|', quotechar='"', quoting=csv.QUOTE_ALL)

print "Se estan recopilando las ideas... aguarde."

for i in range(0, 2000):
    r = urllib.urlopen('https://voslohaces.buenosaires.gob.ar/ideas/view/' + str(i)).read()
    webPage = BeautifulSoup(r, "lxml")

    try:
        proy_descript = webPage.find("div", class_="info-proyecto").get_text()
    except Exception:
        continue

    members = webPage.find("div", class_="perfil-proyecto")

    metaDataTitulo = webPage.find("div", class_="col-xs-12 proyecto-individual-top textWhite cat")
    
    try:
        categoria = metaDataTitulo.find_all('span')[1].get_text()
        proy_nombre = metaDataTitulo.find('h3').get_text()
        socio1 = members.find('h4').get_text()
        try:
            socio2 = members.find('li').get_text()
        except Exception:
            socio2 = "Sin socio"
    except Exception:
        continue

    if categoria[0] == "D":
        categories["diseno"] += 1
    if categoria[0] == "E":
        categories["educacion"] += 1
    if categoria[0] == "I":
        if categoria[8] == "A":
            categories["imp. ambiental"] += 1
        if categoria[8] == "S":
            categories["imp. social"] += 1
    if categoria[0] == "T":
        categories["turismo y gastronomia"] += 1

    # writting the output file
    writer.writerow([i, categoria.encode('utf-8'), proy_nombre.encode('utf-8'), proy_descript.encode('utf-8'), socio1.encode('utf-8'), socio2.encode('utf-8')])

outputFile.close()
print "Se finalizo el proceso de recopilado."
print categories    
    