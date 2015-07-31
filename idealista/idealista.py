import urllib, urllib2, string, csv
from bs4 import BeautifulSoup

print "Menu de busqueda de viviendas en Idealista:"
print "----------------------------------------------"
print "Que quieres buscar? "
print "1 - Alquiler de viviendas "
print "2 - Venta de viviendas "
opcion = input()
if opcion == 1:
    accion = "alquiler-viviendas"
elif opcion == 2:
    accion = "venta-viviendas"

print "Introduce la direccion a buscar: "
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
    print "La busqueda no se ha podido realizar"
    exit()

llista_items = soup.findAll("div", { "class" : "item-info-container" })

f = open("IDEALISTA.csv", "w")
c = csv.writer(f,delimiter="\t")
c.writerow(["Nombre del piso\t","Enlace\t","Precio\t","Habitaciones\t",
            "M2\t","Descripcion\t","Telefono\t"])

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
        x6 = descripcio.contents[0] 
        x7 = telefono.contents[0] + "\t"
        c.writerow([x1,x2,x3,x4,x5,x6.encode("utf-8")+ "\t",x7])
    except Exception,e:
        print "-"

try:        
    precio_medio = soup.find("p", { "class" : "items-average-price" })
    c.writerow(["\t",(precio_medio.contents[0] + "\t").encode("utf-8")
                ,"\t","\t","\t","\t","\t"])
except Exception,e:
        print "No hay pisos a mostrar en esta direccion"
        
f.close()
print "FINAL"
