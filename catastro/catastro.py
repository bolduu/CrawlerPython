# -*- coding: cp1252 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import string, csv, time,urllib, urllib2

def procesoTabla1(soup):
    temp = soup.find("table", { "id" : "ctl00_body_tblInmueble" })
    temp = temp.findAll("tr")
    del temp[0]
    i=0
    tabla1=[]
    for item in temp:
        temp2 = item.findAll("td")
        try:
            if i == 1:
                tabla1.append(temp2[1].find("span").contents)
            else:
                tabla1.append(temp2[1].find("span").contents[0])
        except:
            tabla1.append(" ")
        i+=1
    
    tabla1[1]=tratarString(tabla1[1])
    tabla1[3] = tabla1[3].replace("m", "")
    return tabla1

def procesoTabla2(soup):
    temp = soup.find("table", { "id" : "ctl00_body_tblFinca" })
    temp = temp.findAll("tr")
    del temp[0]

    i=0
    tabla2=[]
    for item in temp:
        temp2 = item.findAll("td")
        try:
            if i == 0:
                tabla2.append(temp2[2].find("span").contents)
            else:
                tabla2.append(temp2[1].find("span").contents[0])
        except:
            tabla2.append(" ")
        i+=1
    tabla2[0]=tratarString(tabla2[0])
    tabla2[1] = tabla2[1].replace("m", "")
    tabla2[2] = tabla2[2].replace("m", "")
    return tabla2

def procesoTabla3(soup):
    temp = soup.find("table", { "id" : "ctl00_body_tblLocales" })
    temp = temp.findAll("tr")
    del temp[0]
    del temp[0]
    i=0
    tabla3=[]
    for fila in temp:
        temp2 = fila.findAll("td")
        for item in temp2:
            try:
                tabla3.append(item.find("span").contents[0])
            except:
                tabla3.append(" ")
    return tabla3

def tratarString(cadena):
    trozos = ""
    for item in cadena:
        if ">" not in (str(item.encode('utf-8'))):
            trozos = trozos + " " + str(item.encode('utf-8'))
    return trozos

def conexionPagina(driver,referencia):
    driver.get("https://www1.sedecatastro.gob.es/OVCFrames.aspx?TIPO=Consulta")
    driver.switch_to_default_content()
    driver.switch_to_frame("registrado") 
    driver.find_element_by_id("txtRC").send_keys(ref)
    driver.find_element_by_id("btnAlfanumerico").click()
    return driver

def getCoord(referencia):

    url = "https://www1.sedecatastro.gob.es/Cartografia/BuscarParcelaInternet.aspx?refcat=" + referencia
    driver.get(url)
    driver.switch_to_default_content()
    Currentwindow = driver.window_handles
    Likebutton = driver.find_element_by_id("ctl00_body_ImgBGoogleMaps").click()
    newwindow = driver.window_handles
    newwindow = list(set(newwindow) - set(Currentwindow))[0]
    driver.switch_to.window(newwindow)
    coord = driver.find_element_by_id("searchboxinput").get_attribute('value')
    driver.implicitly_wait(5)
    driver.close()
    driver.switch_to.window(Currentwindow)
    temp = coord.split(",")
    x=temp[0]
    y=temp[1]
    return driver,x,y
    
###################################################################

#ref = "0016408VK7801N0009QR"
#crm = "CEN-01-000624"

driver = webdriver.Firefox()
f = open("catastre.csv", "wb")
c = csv.writer(f,delimiter="\t")
c.writerow(["ID-CRM","Ref. Catastral","Localizacion","Clase","Superficie","Coef. Participacion",
            "Uso","Fecha Construccion","Localizacion2","Superficie Construida","Superficie Suelo",
            "Tipo Finca","Uso2","Escalera","Planta","Puerta","Superficie Catastral(m2)",
            "Tipo Reforma","Fecha Feforma"])

with open("ref.txt", "r") as lines:
    for line in lines:
        temp = line.split("|")
        crm = temp[0]
        ref= temp[1]
        try:
            driver = conexionPagina(driver,ref)

            html = driver.page_source
            soup = BeautifulSoup(html)

            tabla1 = procesoTabla1(soup)
            tabla2 = procesoTabla2(soup)
            tabla3 = procesoTabla3(soup)
            driver,x,y = getCoord(ref)

            print "Referencia -->" + ref
            if len(tabla1)==7:
                c.writerow([crm.encode("ISO-8859-1"),tabla1[0].encode("ISO-8859-1"),tabla1[1].encode("ISO-8859-1"),
                            tabla1[2].encode("ISO-8859-1"),tabla1[3].encode("ISO-8859-1"),tabla1[4].encode("ISO-8859-1"),
                            tabla1[5].encode("ISO-8859-1"),tabla1[6].encode("ISO-8859-1"),
                            tabla2[0].encode("ISO-8859-1"),tabla2[1].encode("ISO-8859-1"),tabla2[2].encode("ISO-8859-1"),
                            tabla2[3].encode("ISO-8859-1"),tabla3[0].encode("ISO-8859-1"),tabla3[1].encode("ISO-8859-1"),
                            tabla3[2].encode("ISO-8859-1"),tabla3[3].encode("ISO-8859-1"),tabla3[4].encode("ISO-8859-1"),
                            tabla3[5].encode("ISO-8859-1"),tabla3[6].encode("ISO-8859-1")])
            else:
                c.writerow([crm.encode("ISO-8859-1"),tabla1[0].encode("ISO-8859-1"),tabla1[1].encode("ISO-8859-1"),
                            tabla1[2].encode("ISO-8859-1"),tabla1[3].encode("ISO-8859-1")," ",
                            tabla1[4].encode("ISO-8859-1"),tabla1[5].encode("ISO-8859-1"),
                            tabla2[0].encode("ISO-8859-1"),tabla2[1].encode("ISO-8859-1"),tabla2[2].encode("ISO-8859-1"),
                            tabla2[3].encode("ISO-8859-1"),tabla3[0].encode("ISO-8859-1"),tabla3[1].encode("ISO-8859-1"),
                            tabla3[2].encode("ISO-8859-1"),tabla3[3].encode("ISO-8859-1"),tabla3[4].encode("ISO-8859-1"),
                            tabla3[5].encode("ISO-8859-1"),tabla3[6].encode("ISO-8859-1")])

            if len(tabla3) != 0:
                cont = 7
                while cont != len(tabla3):
                    c.writerow([" "," " ," "," " ," " ," " ," " ," " ," " ," " ," " ," " , 
                                tabla3[cont].encode("ISO-8859-1"),tabla3[cont+1].encode("ISO-8859-1"),
                                tabla3[cont+2].encode("ISO-8859-1"),tabla3[cont+3].encode("ISO-8859-1"),
                                tabla3[cont+4].encode("ISO-8859-1"),tabla3[cont+5].encode("ISO-8859-1"),
                                tabla3[cont+6].encode("ISO-8859-1")])        
                    cont+=7
        except:
            print "referencia erronia-->" + ref

print "------------------------FINAL------------------------"
f.close()
driver.close()
