# -*- coding: cp1252 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import string, csv, time,urllib, urllib2

def procesoTabla1(soup):
    temp = soup.find("table", { "id" : "ctl00_body_tblInmueble" })
    temp = temp.findAll("tr")
    del temp[0]
    
    tabla1={}


    tabla1[u'Año construcción local principal']=" "
    tabla1['Uso']=" "
    tabla1[u'Coeficiente de participación']=" "
    tabla1['Superficie (*)']=" "
    tabla1['Clase']=" "
    tabla1[u'Localización']=" " 
    tabla1['Referencia catastral']=" "
    
    i=0
    for item in temp:
        temp2 = item.findAll("td")
        if i == 1:
            tabla1[temp2[0].find("span").contents[0]] = temp2[1].find("span").contents[0]
        else:
            tabla1[temp2[0].find("span").contents[0]] = temp2[1].find("span").contents[0]
        i+=1

    #temp = tabla1['Localización']
    #tabla1['Localización']=tratarString(temp)
    #tabla1['Superficie (*)'] = tabla1['Superficie (*)'].replace("m", "")
    return tabla1

def procesoTabla2(soup):
    temp = soup.find("table", { "id" : "ctl00_body_tblFinca" })
    temp = temp.findAll("tr")
    del temp[0]

    tabla2={}
    tabla2['Localización']=" "
    tabla2['Superficie construida']=" "
    tabla2['Superficie suelo']=" "
    tabla2['Tipo Finca']=" "
    for item in temp:
        temp2 = item.findAll("td")
        tabla2[temp2[0]] = temp2[1].find("span").contents[0]
        
    #tabla2[0] = tratarString(tabla2[0])
    #tabla2[1] = tabla2[1].replace("m", "")
    #tabla2[2] = tabla2[2].replace("m", "")
    #tabla2[1] = tabla2[1].replace(".", "")
    #tabla2[2] = tabla2[2].replace(".", "")
    return tabla2

def procesoTabla3(soup):
    try:
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
        if len(tabla3 != 7):
            tabla3=[" "," "," "," "," "," "," "]
    except:
        tabla3=[" "," "," "," "," "," "," "]
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
    x = temp[0] +" "
    y = temp[1]+" "
    return driver,x,y

###################################################################

#ref = "0016408VK7801N0009QR"
#crm = "CEN-01-000624"
driver = webdriver.Firefox()
f = open("catastre.csv", "wb")
c = csv.writer(f,delimiter="\t")
c.writerow(["ID-CRM","Ref. Catastral","Latitud","Longitud","Localizacion","Clase","Superficie","Coef. Participacion",
            "Uso","Fecha Construccion","Localizacion2","Superficie Construida","Superficie Suelo",
            "Tipo Finca","Uso2","Escalera","Planta","Puerta","Superficie Catastral(m2)",
            "Tipo Reforma","Fecha Feforma"])

with open("ref2.txt", "r") as lines:
    for line in lines:
        temp = line.split("|")
        crm = temp[0]
        ref= temp[1]
        flag=True
        #try:
        driver = conexionPagina(driver,ref)
        html = driver.page_source
        soup = BeautifulSoup(html)
        tabla1 = procesoTabla1(soup)
        #tabla2 = procesoTabla2(soup)
        #tabla3 = procesoTabla3(soup)
        #driver,x,y = getCoord(ref)
        #except:
        #    flag=False
        if flag == True:
            print "Referencia -->" + ref[:20]
            print " "

            print tabla1
            #print tabla2
           
        else:
            print "Referencia erronea --> " + ref
            c.writerow([crm.encode("ISO-8859-1"),ref[:20]," ERROR: Mirar Manualmente ",
                        " " ," " ," " ," " ," " ," " ," " ," " ," " ," " ," " ," "," "," "," "," "," "," "])
            try:
                alert = driver.switch_to_alert()
                alert.accept()
            except:
                driver.window_handles
                for h in driver.window_handles[1:]:
                    driver.switch_to_window(h)
                    driver.close()
                driver.switch_to_window(driver.window_handles[0])
        time.sleep(2)
             
print "------------------------FINAL------------------------"

f.close()
driver.close()
