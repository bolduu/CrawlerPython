# -*- coding: cp1252 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import string
import csv

wd = webdriver.Chrome()
wd.get("http://es.goolzoom.com/")

#pdt = wd.find_element_by_id("BuscarDireccion")
#pdt.submit()

#pdt4 = wd.find_element_by_id("TextDireccion")
#pdt4.send_keys('Carrer Muntaner, 262')
#pdt4.send_keys(Keys.ENTER)

#pdt2 = wd.find_element_by_id("panelLateralTopInmuebles")
#pdt2.click()

#wd.implicitly_wait(1) # seconds
#pdt3 = wd.find_element_by_id("submitAlert")
#pdt3.click()

c = csv.writer(open("GOOLZOOM.csv", "wb"),delimiter="\t")
c.writerow(["Tipo del piso\t","m2\t","Dormitorios\t","Baños\t","€/m2\t","Precio\t","Enlace Web\t"])

pdt4 = wd.find_element_by_id("panelLateralTopInmuebles")
pdt4.click()

wd.implicitly_wait(2) # seconds
pdt5 = wd.find_element_by_id("submitAlert")
pdt5.click()

pdt = wd.find_element_by_id("inputTipoDeBusqueda")
pdt.click()

pdt2 = wd.find_element_by_id("TipoDeBusqueda4")
pdt2.click()

wd.implicitly_wait(1) # seconds

pdt3 = wd.find_element_by_id("TextReferencia")
pdt3.send_keys("7013214DF2871C0010WO")
pdt3.send_keys(Keys.ENTER)

wd.implicitly_wait(6) # seconds

pisos = wd.find_elements_by_class_name("tableListadoInmueblesHover")

pisos[0].click()

enlaces = []
lista_pisos = []
for piso in pisos:
    piso.click()
    info = wd.find_element_by_id("containerInfoWindowInmueble")
    enlace = info.find_element_by_tag_name("a").get_attribute("href")
    temp = (piso.text).split(' ')
    c.writerow([(temp[0] + "\t").encode("utf-8"),(temp[1] + "\t").encode("utf-8"),(temp[2] + "\t").encode("utf-8"),(temp[3] + "\t").
                           encode("utf-8"),(temp[4] + "\t").encode("utf-8"),temp[5].encode("utf-8"),(enlace + "\t").encode("utf-8")])

print "FINAL"

