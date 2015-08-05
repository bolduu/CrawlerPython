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
temp2 = temp[1].split(",")
poblacion = temp2[0]

tablas = soup.findAll("div", { "class" : "datatab" })

direcciones = []
for tabla in tablas:

    filas = tabla.findAll("tr", { "class" : "par" })
    for fila in filas:
        direcciones.append("calle " + fila.contents[0].contents[0] + "," + poblacion)

    filas = tabla.findAll("tr", { "class" : "impar" })
    for fila in filas:
        direcciones.append("calle " + fila.contents[0].contents[0] + "," + poblacion)

###################################################Direcciones creadas
#print direcciones


#f = open("IDEALISTA_POSTAL.csv", "w")
#c = csv.writer(f,delimiter="\t")
#c.writerow(["Nombre del piso\t","Enlace\t","Precio\t","Habitaciones\t",
#            "M2\t","Descripcion\t","Telefono\t"])
        
#for direccion in direcciones:
palabras = direcciones[1].split(" ")
direccion = ""
for palabra in palabras:
    direccion = direccion + "_" + palabra

url = "http://www.idealista.com/buscar/alquiler-viviendas/" + direccion[1:] + "/"

try:
    header = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request(url,headers=header)
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page)
except urllib2.HTTPError:
    print "La busqueda no se ha podido realizar"
    exit()


llista_items = soup.findAll("div", { "class" : "item-info-container" })

item = llista_items[0]

link = item.find("a", { "class" : "item-link" })
titulo = (link.get('title')).encode("utf-8") + "\t"
print titulo
enlace = "http://www.idealista.com" + link.get('href') + "\t"
print enlace


try:
    header2 = {'User-Agent': 'Mozilla/5.0'}
    req2 = urllib2.Request(enlace,headers=header2)
    page2 = urllib2.urlopen(req2)
    soup2 = BeautifulSoup(page2)
except urllib2.HTTPError:
    print "La busqueda no se ha podido realizar"
    exit()

telefono = soup2.find("p", { "class" : "txt-big txt-bold _browserPhone" }).contents[0]
print telefono

vendedor = soup2.find("div", { "class" : "advertiser-data txt-soft" })
print vendedor[0]
print vendedor[0].contents[0]
print vendedor[1].contents[0]









print "------------------------FINAL------------------------"
