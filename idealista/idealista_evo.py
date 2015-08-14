# -*- coding: cp1252 -*-
import urllib, urllib2, string, csv
from bs4 import BeautifulSoup
import time,re

#Se crea una lista con todas las direcciones mediante un CP
def direcciones_codigoPostal():
    print "Introduce el Codigo Postal:"
    opcion = raw_input()
    url = "http://distritopostal.es/" + opcion
    
    try:
        header = {'User-Agent': 'Mozilla/5.0'}
        req = urllib2.Request(url,headers=header)
        page = urllib2.urlopen(req)
        soup = BeautifulSoup(page)
    except urllib2.HTTPError:
        print "La busqueda no se ha podido realizar"
        exit()

    poblacion = soup.find("h2", {"id":"map_title"}).contents[0]
    temp = poblacion.split("-")
    temp2 = temp[1].split(",")
    poblacion = temp2[0]
    tablas = soup.findAll("div", { "class" : "datatab" })
    direcciones = []
    
    for tabla in tablas:
        filas = tabla.findAll("tr", { "class" : "par" })
        for fila in filas:
            direcciones.append("calle " + fila.contents[0].contents[0] + "," + poblacion)
        filas = tabla.findAll("tr", { "class" : "impar" })
        for fila in filas:
            direcciones.append("calle " + fila.contents[0].contents[0] + "," + poblacion)

    return direcciones,opcion

#Se conecta a la pagina web general de pisos 
def conexion_listaPisos(item):
    palabras = item.split(" ")
    direccion = ""
    for palabra in palabras:
        direccion = direccion + "_" + palabra

    url = "http://www.idealista.com/buscar/alquiler-viviendas/" + direccion[1:] + "/"

    try:
        header = {'User-Agent': 'Mozilla/5.0'}
        req = urllib2.Request(url,headers=header)
        page = urllib2.urlopen(req)
        soup = BeautifulSoup(page)
    except urllib2.HTTPError:
        print "La busqueda no se ha podido realizar"
        exit()

    return soup

#Realiza la conexion con la pagina individual del piso
def conexionPiso(enlace):
    try:
        header2 = {'User-Agent': 'Mozilla/5.0'}
        req2 = urllib2.Request(enlace,headers=header2)
        page2 = urllib2.urlopen(req2)
        soup2 = BeautifulSoup(page2.read())
    except:
        print "La busqueda no se ha podido realizar"
        
        
    return soup2

#Se trata la direccion del piso
def tratarDireccion(soup2):
    datos_direccion = soup2.find("div", { "id" : "addressPromo" })
    try:
        calle_piso = datos_direccion.find("h2").contents[0]
        calle_numero = calle_piso.split(",")
    except:
        calle_piso = ""
        calle_numero = ""
    
    calle =""
    if (len(calle_numero) == 2):
        calle_piso2 = datos_direccion.find("h2").contents[0]
        numero = calle_numero[1]
        calle_piso = calle_numero[0].split(" ")
        tipo_via = calle_piso[0]
        for trozo in calle_piso[1:]:
            calle += trozo + " "
    elif(len(calle_numero) == 0):
        calle_piso2 = "Direccion sin especificar"
        tipo_via = "XXXX"
        calle = "Direccion sin especificar"
        numero = "S/N"
    else:
        calle_piso2 = datos_direccion.find("h2").contents[0]
        calle_piso = calle_numero[0].split(" ")
        tipo_via = calle_piso[0]
        for trozo in calle_piso[1:]:
            calle += trozo + " "
        numero = "S/N"
    
    datos_barrio = datos_direccion.findAll("li")
    barrio = datos_barrio[0].contents[0]
    ciudad = datos_barrio[len(datos_barrio)-1].contents[0]
    
    return tipo_via,calle,numero,barrio,ciudad,calle_piso2

#Se obtiene la referencia del piso
def referenciaPiso(soup2):
    temp = soup2.find("div", { "id" : "aside-share-links" })
    anuncio = temp.find("h3").contents[0].split(" ")
    referencia_piso = anuncio[len(anuncio)-1]
    
    return referencia_piso

#Se obtiene el tipo de vivienda
def tipoPiso(titulo):
    if titulo[:6]=="Chalet":
        tipo = "Chalet"
    elif titulo[:5]=="Atico":
        tipo = "Atico"
    elif titulo[:4]=="Casa":
        tipo = "Casa"
    elif titulo[:6]=="Duplex":
        tipo = "Duplex"
    else:
        tipo = "Piso"
        
    return tipo


#Se obtiene si la vivienda es de obra nueva o de segunda mano
def compruebaPiso(soup2):
    if "Obra nueva" in soup2:
        estado = "Obra nueva"
    else:
        estado = "Segunda mano"
        
    return estado

#Se obtiene el precio/mes, los m2, el numero de habitaciones y la planta del piso
def precio_piso(soup2):
    temp = soup2.find("div", { "class" : "info-data" })
    items = temp.findAll("span")
    precio_mes = items[0].contents[0].contents[0]
    m2 = items[2].contents[0].contents[0]
    try :
        hab = items[4].contents[0].contents[0]
    except:
        hab = ""
    try:
        planta = items[6].contents[0].contents[0]
    except:
        planta = ""
    
    return precio_mes,m2,hab,planta

def getDescripcion(item):
    try:
        descripcion = item.find("p", { "class" : "item-description" }).contents[0]
    except:
        descripcion = ""
        
    return descripcion

#Calculo del precio del m2
def calculoPrecioM2(precio_mes,m2):
    if "." in precio_mes:
        precio = float(precio_mes) * 1000
    else:
        precio = float(precio_mes)
    M2 = float(m2)
    
    return str(round(precio/M2,2))

#Se obtiene el calculo de la coordenadas de la vivienda
def calculCoordenades(soup2):
    prova = "" + str(soup2)
    x_temp = prova.find('latitude:"')
    x = prova[x_temp+10 : x_temp+18]
    y_temp = prova.find('longitude:"')
    y = prova[y_temp+11 : y_temp+18]
    return x,y

def compruebaActualizado(soup2):
    try:    
        actualizado = soup2.find("section", { "id" : "stats"}).find("h2").contents[0]
    except:
        actualizado = ""
        
    return actualizado

def buscaVendedor(soup2):
    try:
        vendedor = soup2.find("div", { "class" : "advertiser-data txt-soft" })
        datos_vendedor = vendedor.findAll("p")
        vendedor = datos_vendedor[0].contents[0]
    except:
        vendedor = "No se especifica"

    return vendedor    
        
####################################  INICIO PROGRAMA  ######################################

#Se cogen todas las direcciones
lista_direcciones,cp = direcciones_codigoPostal()

#f = open("IDEALISTA_MASSIU.csv", "w")
#c = csv.writer(f,delimiter="\t")
#c.writerow(["Nombre del piso\t","Enlace\t","Precio\t","Habitaciones\t",
#            "M2\t","Descripcion\t","Telefono\t"])

for direccion in lista_direcciones:

    #Se conecta a la pagina web general de pisos
    soup = conexion_listaPisos(direccion)
    llista_items = soup.findAll("div", { "class" : "item-info-container" })

    for item in llista_items:

        link = item.find("a", { "class" : "item-link" })
        titulo = (link.get('title')).encode("utf-8") + "\t"
        enlace = "http://www.idealista.com" + link.get('href') + "\t"
        tipo_piso = tipoPiso(titulo)
        soup2 = conexionPiso(enlace)
        try:
            telefono = soup2.find("p", { "class" : "txt-big txt-bold _browserPhone" }).contents[0]
        except:
            telefono = "Sin especificar"

        vendedor = buscaVendedor(soup2)
        referencia_vendedor = datos_vendedor[1].contents[0]
        tipo_via,partes_direccion,numero,barrio,ciudad,calle_piso = tratarDireccion(soup2)
        referencia_piso = referenciaPiso(soup2)
        precio_mes,m2,hab,planta = precio_piso(soup2)
        fecha_carga = time.strftime("%d/%m/%Y")
        nuevo_usado = compruebaPiso(soup2)
        actualizado = compruebaActualizado(soup2)
        descripcion = getDescripcion(item)
        precioM2 = calculoPrecioM2(precio_mes,m2)

        x,y = calculCoordenades(soup2)

        
        ####################### PRINTS ##################################
        print "-----------------------------------------------------"
        print "-->" + direccion
        print "Alquiler"
        print "Idealista"
        print "fecha carga: " + fecha_carga
        print "Precio Mes: " + precio_mes
        print "Telefono: " + telefono
        print "Vendedor: " + vendedor
        print "Referencia vendedor" + referencia_vendedor
        print "tipo de vivienda: " + tipo_piso
        print "Nuevo/Usado: " + nuevo_usado
        print "Ciudad: " + ciudad
        print "Codigo Postal: " + cp
        print "Direccion completa: " + calle_piso
        print "Tivo Via: " + tipo_via
        print "Calle: " + partes_direccion
        print "Numero: " + numero
        print "Barrio:" + barrio
        print "Referencia Piso: " + referencia_piso
        print "Precio/Mes: " + precio_mes
        print "m2: " + m2
        print "Habitaciones: " + hab
        print "Planta: " + planta
        print "Precio eur/m2: " + precioM2
        print "Fecha Actualizacion: " + actualizado
        print "Descripcion: " + descripcion
        print "Enlace: " + enlace
        print "X/Y: " + x + "," + y

        
    print "------------------------FINAL------------------------"
