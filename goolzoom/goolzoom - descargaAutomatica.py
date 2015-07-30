# -*- coding: cp1252 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import string

##################### MENU ###############################
print "Buscar pisos por:"
print "-------------------"
print "1 - Venta "
print "2 - Alquiler "
opcion_metodo = input()

print "Como quieres buscar? "
print "--------------------------------"
print "1 - Por Referencia Catastral "
print "2 - Por Direccion "
opcion_busqueda = input()

if opcion_busqueda == 2:
    print "Introduce la direccion a buscar: "
    entrada = unicode(raw_input(),"ISO-8859-1")
elif opcion_busqueda == 1:
    print "Introduce la referencia Catastral a buscar: "
    entrada = raw_input()
###########################################################

wd = webdriver.Firefox()
wd.get("http://es.goolzoom.com/")

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
    pdt.send_keys(entrada)
    pdt.send_keys(Keys.ENTER)

##################### ALQUILER #######################
if opcion_metodo == 2:
    pdt2 = wd.find_element_by_id("divInmuebleVenta")
    pdt2.find_element_by_tag_name("a").click()
######################################################

############DESCARGA AUTOMATICA##############################
pdt3 = wd.find_element_by_id("divDownloadListadoInmuebles")
pdt3.find_element_by_tag_name("a").click()

wd.find_element_by_id("selectorTasacion").click()

username = wd.find_element_by_id("emailSuscrito")
username.send_keys("xavier.montoya@altaviviendas.com")

password = wd.find_element_by_id("constrasenaSuscrito")
password.send_keys("Taurus2015")

wd.find_element_by_class_name("button").click()
#############################################################

precio_medio = wd.find_elements_by_class_name("textoGris")
print precio_medio[1].text

#raw_input()
#wd.quit()

print "FINAL"
