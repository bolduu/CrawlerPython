# -*- coding: cp1252 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import string, csv, time

#print "Introduce la Referencia Catastral a buscar:"
#referencia = input()
referencia = "0990511VL5009S0030AL"

wd = webdriver.Firefox()

wd.get("https://www1.sedecatastro.gob.es/OVCFrames.aspx?TIPO=Consulta")

driver.maximize_window()
driver.implicitly_wait(20)

wd.find_element_by_id("txtRC.textogris").send_keys(referencia)

#wd.find_element_by_id("btnAlfanumerico").click()


print "------------------------FINAL------------------------"
