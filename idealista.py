import urllib, urllib2 
from bs4 import BeautifulSoup
import string


print "Menu de busqueda de viviendas en idealista:"
print "-----------------------------------------"
print "introduce la direccion a buscar: "
entrada = raw_input()
palabras = entrada.split(" ")
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
    print "busqueda no trobada"
    exit()


llista_items = soup.findAll("div", { "class" : "item-info-container" })

f = open ("idealista.txt", "w")

for item in llista_items:
    link = item.find("a", { "class" : "item-link" })
    x = link.get('title') + "\n"
    f.write(x.encode("utf-8"))
    
    link = "enlace: http://www.idealista.com" + link.get('href')
    f.write(link + "\n")

    preu = item.find("span", { "class" : "item-price" })
    sub_llista = item.findAll("span", { "class" : "item-detail" })
    descripcio = item.find("p", { "class" : "item-description" })
    telefono = item.find("span", { "class" : "icon-phone item-not-clickable-phone" })

    try:
        x = (preu.contents[0] + " euros/mes   " + sub_llista[0].contents[0] + "habitaciones   " + sub_llista[1].contents[0] + "m2   " + sub_llista[2].contents[0] + "planta\n")
        f.write(x.encode("utf-8"))
        x = (descripcio.contents[0] + "\n")
        f.write(x.encode("utf-8"))
        f.write("telefono: " + telefono.contents[0] + "\n\n")
        f.write("----------------------------------------------------------------------------------------------------------------------------------------------------------\n\n")
    except Exception,e:
        print ""

f.close()
print "FINAL"

#raw_input()




    
    
    
