import urllib, urllib2 
from bs4 import BeautifulSoup
import string
import csv


print "Menu de busqueda de viviendas en HABITACLIA:"
print "-----------------------------------------"

print "introduce la direccion a buscar: "
entrada = raw_input()
palabras = entrada.split(" ")
direccion = ""
for palabra in palabras:
    direccion = direccion + "-" + palabra

url = "http://www.habitaclia.com/q/" + direccion[1:]

try:
    header = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request(url,headers=header)
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page)
except urllib2.HTTPError:
    print "la busqueda no se ha podido realizar"
    exit()

c = csv.writer(open("HABITACLIA.csv", "wb"),delimiter="\t")
c.writerow(["Nombre del piso\t","Enlace\t","Precio\t","Parametros\t","Descripcion\t"])

llista_items = soup.findAll("li", { "itemtype" : "http://schema.org/Product" })

for item in llista_items:

    try:
        precio = item.find("span", { "class" : "eur" })
        x3 = (precio.contents[0] + "\t")
    except Exception,e:
        precio = item.find("span", { "class" : "eur_m" })
        x3 = (precio.contents[0] + "\t")

    dades = item.find("div", { "class" : "datos" })
    link = dades.find("a", { "itemprop" : "name" })
    temp = link.get('title')
    x2 = (link.get('href') + "\t")
    direccion = dades.find("span", { "class" : "dir" })
    direccion = direccion.find("div")
    x1 = (temp + " , " +  direccion.contents[0] + "\t")
    parametres = dades.find("i")
    x4 = (parametres.contents[0] + "2" + parametres.contents[2] + "\t")
    descripcion = dades.find("span", { "class" : "descripcion" })
    calle = descripcion.find("strong")

    try:
        x5 = (descripcion.contents[0] + calle.contents[0] + descripcion.contents[2] + "\t")
    except Exception,e1:
        x5 = (descripcion.contents[0] + "\t")

    c.writerow([x1.encode("utf-8"),x2.encode("utf-8"),x3.encode("utf-8"),x4.encode("utf-8"),x5.encode("utf-8")])

print "FINAL"

    





    
    
    
