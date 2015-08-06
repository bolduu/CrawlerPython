import urllib, urllib2, string, csv
from bs4 import BeautifulSoup

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

    return direcciones

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
        soup2 = BeautifulSoup(page2)
    except urllib2.HTTPError:
        print "La busqueda no se ha podido realizar"
        exit()
    return soup2

#Se trata la direccion del piso
def tratarDireccion(soup2):
    datos_direccion = soup2.find("div", { "id" : "addressPromo" })
    calle_piso = datos_direccion.find("h2").contents[0]

    calle_numero = calle_piso.split(",")
    calle =""
    if (len(calle_numero) == 2):
        numero = calle_numero[1]
        calle_piso = calle_numero[0].split(" ")
        tipo_via = calle_piso[0]
        for trozo in calle_piso[1:]:
            calle += trozo + " "
    elif(len(calle_numero) == 0):
        tipo_via = "XXXX"
        calle = "Direccion sin especificar"
        numero = "S/N"
    else:
        calle_piso = calle_numero[0].split(" ")
        tipo_via = calle_piso[0]
        for trozo in calle_piso[1:]:
            calle += trozo + " "
        numero = "S/N"

    datos_barrio = datos_direccion.findAll("li")
    barrio = datos_barrio[0].contents[0]
    ciudad = datos_barrio[len(datos_barrio)-1].contents[0]
    
    return tipo_via,calle,numero,barrio,ciudad

#Se obtiene la referencia del piso
def referenciaPiso(soup2):
    temp = soup2.find("div", { "id" : "aside-share-links" })
    anuncio = temp.find("h3").contents[0].split(" ")
    referencia_piso = anuncio[len(anuncio)-1]
    return referencia_piso
    
def precio_piso(soup2):
    temp = soup2.find("section", { "id" : "details" })

    print temp

####################################  INICIO PROGRAMA  ######################################

#Se cogen todas las direcciones
lista_direcciones = direcciones_codigoPostal()

#for direccion in lista_direcciones:

#Se conecta a la pagina web general de pisos
soup = conexion_listaPisos(lista_direcciones[1])

llista_items = soup.findAll("div", { "class" : "item-info-container" })

for item in llista_items:

    link = item.find("a", { "class" : "item-link" })
    titulo = (link.get('title')).encode("utf-8") + "\t"
    #print titulo
    enlace = "http://www.idealista.com" + link.get('href') + "\t"
    #print enlace

    soup2 = conexionPiso(enlace)

    telefono = soup2.find("p", { "class" : "txt-big txt-bold _browserPhone" }).contents[0]
    #print telefono

    vendedor = soup2.find("div", { "class" : "advertiser-data txt-soft" })
    datos_vendedor = vendedor.findAll("p")
    vendedor = datos_vendedor[0].contents[0]
    referencia_vendedor = datos_vendedor[1].contents[0]
    #print vendedor
    #print referencia_vendedor
    
    tipo_via,partes_direccion,numero,barrio,ciudad = tratarDireccion(soup2)

    referencia_piso = referenciaPiso(soup2)
    #print referencia_piso

    precio_piso(soup2)
    
    
print "------------------------FINAL------------------------"
