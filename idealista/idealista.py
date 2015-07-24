import urllib, urllib2 
from bs4 import BeautifulSoup
import string
import csv

print "Menu de busqueda de viviendas en idealista:"
print "-----------------------------------------"
opcion = 0
while opcion == 0:
    print "que quieres hacer? "
    print "1 - Alquilar viviendas "
    print "2 - Comprar viviendas "
    opcion = input()
    if opcion == 1:
        accion = "alquiler-viviendas"
    elif opcion == 2:
        accion = "venta-viviendas"

print "introduce la direccion a buscar: "
entrada = raw_input()
palabras = entrada.split(" ")
direccion = ""
for palabra in palabras:
    direccion = direccion + "_" + palabra

url = "http://www.idealista.com/buscar/" + accion + "/" + direccion[1:] + "/"

try:
    header = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request(url,headers=header)
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page)
except urllib2.HTTPError:
    print "la busqueda no se ha podido realizar"
    exit()

llista_items = soup.findAll("div", { "class" : "item-info-container" })

c = csv.writer(open("IDEALISTA.csv", "wb"),delimiter="\t")
c.writerow(["Nombre del piso\t","Enlace\t","Precio\t","Habitaciones\t","M2\t","Planta\t","Descripcion\t","Telefono\t"])

for item in llista_items:
    link = item.find("a", { "class" : "item-link" })
    x1 = (link.get('title')).encode("utf-8") + "\t"
    x2 = "http://www.idealista.com" + link.get('href') + "\t"

    preu = item.find("span", { "class" : "item-price" })
    sub_llista = item.findAll("span", { "class" : "item-detail" })
    descripcio = item.find("p", { "class" : "item-description" })
    telefono = item.find("span", { "class" : "icon-phone item-not-clickable-phone" })

    try:
        x3 = preu.contents[0] + "\t"
        x4 = sub_llista[0].contents[0] + "\t"
        x5 = sub_llista[1].contents[0] + "\t"
        x6 = sub_llista[2].contents[0] 
        x7 = descripcio.contents[0] 
        x8 = telefono.contents[0] + "\t"
        c.writerow([x1,x2,x3,x4,x5,x6.encode("utf-8") + "\t",x7.encode("utf-8")+ "\t",x8])
    except Exception,e:
        print "-"

print "FINAL"





    
    
    
