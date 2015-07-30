# -*- coding: cp1252 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import string
import csv

print "Buscar pisos por:"
print "-------------------"
print "1 - Venta "
print "2 - Alquiler "
opcion_metodo = input()

print "Como quieres buscar? "
print "---------------------------"
print "1 - por Referencia Catastral "
print "2 - por Direccion "
opcion_busqueda = input()

if opcion_busqueda == 2:
    print "Introduce la direccion a buscar: "
    entrada = unicode(raw_input(),"ISO-8859-1")
elif opcion_busqueda == 1:
    print "Introduce la referencia Catastral a buscar: "
    entrada = raw_input()

wd = webdriver.Firefox()
wd.get("http://es.goolzoom.com/")

f = open("GOOLZOOM.csv", "w")
c = csv.writer(f,delimiter="\t")
c.writerow(["Tipo del piso\t","m2\t","Dormitorios\t",
            "Baños\t","€/m2\t","Precio\t","Enlace Web\t"])

wd.find_element_by_id("panelLateralTopInmuebles").click()

wd.find_element_by_id("submitAlert").click()

if opcion_busqueda == 2:
    pdt = wd.find_element_by_id("TextDireccion")
    pdt.send_keys(entrada)
    pdt.send_keys(Keys.ENTER)

elif opcion_busqueda == 1:
    wd.find_element_by_id("inputTipoDeBusqueda").click()
    wd.find_element_by_id("TipoDeBusqueda4").click()

    pdt = wd.find_element_by_id("TextReferencia")
    pdt.send_keys(entrada.encode("utf-8"))
    pdt.send_keys(Keys.ENTER)

##################### ALQUILER ###################
if opcion_metodo == 2:
    pdt1 = wd.find_element_by_id("divInmuebleVenta")
    pdt1.find_element_by_tag_name("a").click()
##################################################

############DESCARGA AUTOMATICA##############################
#pdt2 = wd.find_element_by_id("divDownloadListadoInmuebles")
#pdt2.find_element_by_tag_name("a").click()

#wd.find_element_by_id("selectorTasacion").click()

#username = wd.find_element_by_id("emailSuscrito")
#username.send_keys("xavier.montoya@altaviviendas.com")
#password = wd.find_element_by_id("constrasenaSuscrito")
#password.send_keys("Taurus2015")
#wd.find_element_by_class_name("button").click()
#############################################################
    
pisos = wd.find_elements_by_class_name("tableListadoInmueblesHover")

for piso in pisos:
    piso.click()
    info = wd.find_element_by_id("containerInfoWindowInmueble")
    enlace = info.find_element_by_tag_name("a").get_attribute("href")
    temp = (piso.text).split(' ')

    if len(temp) == 7:
        c.writerow([(temp[0] + "\t").encode("utf-8"),(temp[1] + "\t").encode("utf-8"),
                    (temp[2] + "\t").encode("utf-8"),(temp[3] + "\t").encode("utf-8"),
                    (temp[4] + "\t").encode("utf-8"),(temp[5] + "\t").encode("utf-8"),
                    (enlace + "\t").encode("utf-8")])
    else:
        c.writerow([(temp[0] + "\t").encode("utf-8"),"\t","\t","\t",
                    "\t",(temp[len(temp)-2] + "\t").encode("utf-8"),
                    (enlace + "\t").encode("utf-8")])

precio_medio = wd.find_elements_by_class_name("textoGris")
precio = (precio_medio[1].text).split(' ')
c.writerow(["\t","\t","\t","\t","\t","\t",("Precio Medio:    " + precio[0] + " Euros  -  " + precio[4] + " Euros\m2 \t").encode("utf-8")])
f.close()
#wd.quit()

print "FINAL"
