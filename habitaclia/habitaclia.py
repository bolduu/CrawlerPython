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
    print "la busqueda no se ha posido realizar"
    exit()

llista_items = soup.findAll("div", { "class" : "datos" })
#c = csv.writer(open("IDEALISTA.csv", "wb"),delimiter="\t")

#**************************************************************************


#c.writerow(["Nombre del piso\t","Enlace\t","Precio\t","Habitaciones\t","M2\t","Planta\t","Descripcion\t","Telefono\t"])

#for item in llista_items:
link = llista_items[0].find("a", { "itemprop" : "name" })
x1 = (link.get('title')).encode("utf-8") + "\t"
x2 = link.get('href') + "\t"






    





    
    
    
