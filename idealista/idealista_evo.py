import urllib, urllib2, string, csv
from bs4 import BeautifulSoup

print "Introduce el Codigo Postal:"
opcion = raw_input()

url = "http://distritopostal.es/" + opcion

try:
    header = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request(url,headers=header)
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page)
except urllib2.HTTPError:
    print "La busqueda no se ha podido realizar"
    exit()


poblacion = soup.find("h2", {"id":"map_title"}).contents[0]
temp = poblacion.split("-")
poblacion = temp[1][:-2]
print poblacion

tablas = soup.findAll("div", { "class" : "datatab" })

#f = open("IDEALISTA.csv", "w")

direcciones = []
for tabla in tablas:

    filas = tabla.findAll("tr", { "class" : "par" })
    for fila in filas:
        direcciones.append("calle " + fila.contents[0].contents[0] + "," + poblacion)

    filas = tabla.findAll("tr", { "class" : "impar" })
    for fila in filas:
        direcciones.append("calle " + fila.contents[0].contents[0] + "," + poblacion)

print direcciones

print "------------------------FINAL------------------------"
