import urllib, urllib2 
from bs4 import BeautifulSoup
import string

#opcio = 0
#while(opcio!=5):
print "Menu de busqueda en idealista"
print "-----------------------------------------"
print "introduce la direccion a buscar: "
entrada = raw_input()
listas = entrada.split(" ")
direccion = ""
for lista in listas:
    direccion = direccion + "_" + lista

url = "http://www.idealista.com/buscar/alquiler-viviendas/" + direccion[1:] + "/"

#page = urllib2.urlopen(url)
#soup = BeautifulSoup(page.read())

try:
    header = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request(url,headers=header)
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page)
except urllib2.HTTPError:
    print "busqueda no trobada"

llista_items = soup.findAll("div", { "class" : "item-info-container" })

print llista_items[1].findAll("span", { "class" : "item-price" })
#for items in llista_items:
    
    
    

print "FINAL"






    
    
    
