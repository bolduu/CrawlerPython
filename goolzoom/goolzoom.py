# -*- coding: cp1252 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import string
import csv

#print "Buscar pisos por:"
#print "1 - Venta "
#print "2 - Alquiler "
#opcion_metodo = input()

print "Como quieres buscar? "
print "---------------------------"
print "1 - por Referencia Catastral "
print "2 - por Direccion "
opcion_busqueda = input()

if opcion_busqueda == 2:
    print "Introduce la direccion a buscar: "
    entrada = raw_input()
elif opcion_busqueda == 1:
    print "Introduce la referencia Catastral a buscar: "
    entrada = raw_input()

wd = webdriver.Firefox()
wd.get("http://es.goolzoom.com/")

f = open("GOOLZOOM.csv", "w")
c = csv.writer(f,delimiter="\t")
c.writerow(["Tipo del piso\t","m2\t","Dormitorios\t",
            "Baños\t","€/m2\t","Precio\t","Enlace Web\t"])

if opcion_busqueda == 2:
    pdt = wd.find_element_by_id("panelLateralTopInmuebles")
    pdt.click()

    #wd.implicitly_wait(3) # seconds
    pdt1 = wd.find_element_by_id("submitAlert")
    pdt1.click()

    pdt2 = wd.find_element_by_id("TextDireccion")
    pdt2.send_keys(entrada)
    pdt2.send_keys(Keys.ENTER)

elif opcion_busqueda == 1:
    pdt = wd.find_element_by_id("panelLateralTopInmuebles")
    pdt.click()

    #wd.implicitly_wait(3) # seconds
    pdt1 = wd.find_element_by_id("submitAlert")
    pdt1.click()

    pdt2 = wd.find_element_by_id("inputTipoDeBusqueda")
    pdt2.click()

    pdt3 = wd.find_element_by_id("TipoDeBusqueda4")
    pdt3.click()

    #wd.implicitly_wait(4) # seconds

    pdt4 = wd.find_element_by_id("TextReferencia")
    pdt4.send_keys(entrada.encode("utf-8"))
    pdt4.send_keys(Keys.ENTER)

#wd.implicitly_wait(4) # seconds

##################### ALQUILER ###################
#if opcion_metodo == 2:
pdt6 = wd.find_element_by_id("divInmuebleVenta")
pdt6.find_element_by_tag_name("a").click()
##################################################
pisos = wd.find_elements_by_class_name("tableListadoInmueblesHover")

for piso in pisos:
    piso.click()
    info = wd.find_element_by_id("containerInfoWindowInmueble")
    enlace = info.find_element_by_tag_name("a").get_attribute("href")
    #print info.find_element_by_tag_name("a").text
    #print len(info.find_element_by_tag_name("a").text)
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
f.close()
#wd.quit()

print "FINAL"
