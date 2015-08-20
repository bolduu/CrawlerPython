# -*- coding: cp1252 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import string, csv, time,urllib, urllib2
from bs4 import BeautifulSoup

def procesoTabla1(soup):
    temp = soup.find("table", { "id" : "ctl00_body_tblInmueble" })
    temp = temp.findAll("tr")
    del temp[0]
    i=0
    tabla1=[]
    for item in temp:
        temp2 = item.findAll("td")
        if i == 1:
            tabla1.append(temp2[1].find("span").contents)
        else:
            tabla1.append(temp2[1].find("span").contents[0])
        i+=1
    
    tabla1[1]=tratarString(tabla1[1])
    return tabla1

def procesoTabla2(soup):
    temp = soup.find("table", { "id" : "ctl00_body_tblFinca" })
    temp = temp.findAll("tr")
    del temp[0]

    i=0
    tabla2=[]
    for item in temp:
        temp2 = item.findAll("td")
        if i == 0:
            tabla2.append(temp2[2].find("span").contents)
        else:
            tabla2.append(temp2[1].find("span").contents[0])
        i+=1
    tabla2[0]=tratarString(tabla2[0])
    return tabla2

def procesoAlmacenElementosComunes(soup):
    temp = soup.find("table", { "id" : "ctl00_body_tblLocales" })
    temp = temp.findAll("tr")
    del temp[0]
    del temp[0]
    i=0
    almacen_elementosComunes=[]
    for fila in temp:
        temp2 = fila.findAll("td")
        for item in temp2:
            try:
                almacen_elementosComunes.append(item.find("span").contents[0])
            except:
                almacen_elementosComunes.append(" ")
    return almacen_elementosComunes

def tratarString(cadena):
    trozos = ""
    for item in cadena:
        if ">" not in (str(item.encode('utf-8'))):
            trozos = trozos + " " + str(item.encode('utf-8'))
    print trozos
    return trozos

###################################################################
referencia = "9995701YH1499F0024EG"
#print "Introduce la Referencia Catastral a buscar:"
#referencia = input()

driver = webdriver.Firefox()
#driver.maximize_window()


driver.get("https://www1.sedecatastro.gob.es/OVCFrames.aspx?TIPO=Consulta")
driver.switch_to_default_content()
driver.switch_to_frame("registrado") 
driver.find_element_by_id("txtRC").send_keys(referencia)
driver.find_element_by_id("btnAlfanumerico").click()

########################Conexion y consulta####################

html = driver.page_source
soup = BeautifulSoup(html)

tabla1 = procesoTabla1(soup)
# Referencia catastral / Localización / Clase / Superficie (*) / Coeficiente de participación / Uso / Año construcción local principal
print "----Datos del Bien Inmueble----"
print tabla1

tabla2 = procesoTabla2(soup)
# Localización / Superficie construida / Superficie suelo / Tipo / Finca
print "----Datos de la Finca en la que se integra el Bien Inmueble----"
print tabla2

almacen_elementosComunes = procesoAlmacenElementosComunes(soup)
#Uso / Escalera / Planta / Puerta / Superficie catastral (m2) / Tipo Reforma / Fecha Reforma
print "----Elementos Construidos del Bien Inmueble----"
print almacen_elementosComunes




print "------------------------FINAL------------------------"
