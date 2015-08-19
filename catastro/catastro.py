# -*- coding: cp1252 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import string, csv, time,urllib, urllib2
from bs4 import BeautifulSoup

referencia = "0990511VL5009S0030AL"
#print "Introduce la Referencia Catastral a buscar:"
#referencia = input()

driver = webdriver.Firefox()
driver.maximize_window()
driver.get("https://www1.sedecatastro.gob.es/OVCFrames.aspx?TIPO=Consulta")
driver.switch_to_default_content()
driver.switch_to_frame("registrado") 
driver.find_element_by_id("txtRC").send_keys(referencia)
driver.find_element_by_id("btnAlfanumerico").click()

########################Conexion y consulta####################

html = driver.page_source
soup = BeautifulSoup(html)
print "----Datos del Bien Inmueble----"
temp = soup.find("table", { "id" : "ctl00_body_tblInmueble" })

temp = temp.findAll("tr")
del temp[0]
i=0
aux=[]
for item in temp:
    temp2 = item.findAll("td")
    if i == 1:
        aux.append(temp2[1].find("span").contents)
    else:
        aux.append(temp2[1].find("span").contents[0])
    i+=1

print aux

print "----Datos de la Finca en la que se integra el Bien Inmueble----"
temp = soup.find("table", { "id" : "ctl00_body_tblFinca" })
temp = temp.findAll("tr")
del temp[0]
print "------------------------FINAL------------------------"
