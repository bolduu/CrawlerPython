import urllib, urllib2, string, csv, time
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
    if "-" in poblacion:
        temp = poblacion.split("-")
        temp2 = temp[1].split(",")
    else:
        temp2 = poblacion.split(",")

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
    flag = True
    soup=""
    item.encode("utf-8")
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
    except :
        print "No hay pisos en esta direccion"
        flag = False
    
    return soup,flag

#Realiza la conexion con la pagina individual del piso
def conexionPiso(enlace):
    flag2 = True
    try:
        header2 = {'User-Agent': 'Mozilla/5.0'}
        req2 = urllib2.Request(enlace,headers=header2)
        page2 = urllib2.urlopen(req2)
        soup2 = BeautifulSoup(page2.read())
    except:
        print "La busqueda no se ha podido realizar"
        flag2 = False
        soup2 = ""
        
    return soup2,flag2

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
    try:
        datos_barrio = datos_direccion.findAll("li")
        barrio = datos_barrio[0].contents[0]
        ciudad = datos_barrio[len(datos_barrio)-1].contents[0]
    except:
        barrio=""
        ciudad=""
        
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
        if len(planta) == 2:
            planta = planta [0]
        elif len(planta) == 3:
            planta = planta [0:1]
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

    temp = precio_mes.replace(".", "")
    temp2 = m2.replace(".", "")
    precio = float(temp)
    M2 = float(temp2)
    return str(round(precio/M2,2))

#Se obtiene el calculo de la coordenadas de la vivienda
def calculCoordenades(soup2):
    prova = "" + str(soup2)
    x_temp = prova.find('latitude:"')
    x = prova[x_temp+10 : x_temp+18]
    y_temp = prova.find('longitude:"')
    y = prova[y_temp+11 : y_temp+18]
    return x,y

#Se obtiene la fecha de la ultima actualizacion del anuncio
def compruebaActualizado(soup2):
    try:    
        actualizado = soup2.find("section", { "id" : "stats"}).find("h2").contents[0]
    except:
        actualizado = ""
        
    return actualizado

#Se obtiene el vendedor y su referencia
def buscaVendedor(soup2):
    try:
        vendedor = soup2.find("div", { "class" : "advertiser-data txt-soft" })
        datos_vendedor = vendedor.findAll("p")
        vendedor = datos_vendedor[0].contents[0]
        referencia_vendedor = datos_vendedor[1].contents[0]
    except:
        vendedor = "No se especifica"
        referencia_vendedor = "No se especifica"

    return vendedor,referencia_vendedor    
        
####################################  INICIO PROGRAMA  ########################################

#Se cogen todas las direcciones
lista_direcciones,cp = direcciones_codigoPostal()
#se crea el fichero.csv

print len(lista_direcciones)

f = open("IDEALISTA_MASSIU.csv", "wb")
c = csv.writer(f,delimiter="\t")
c.writerow(["Tipo\t","Cartera\t","Fecha Carga\t","Referencia Piso\t",
            "Telefono\t","Tipo\t","Nuevo/Usado\t","Provincia\t","Codigo Postal\t",
            "Direccion\t","Via\t","Calle\t","Numero\t","Barrio\t",
            "Precio euros/mes\t","Planta\t","Habitaciones\t","m2\t",
            "Euro/m2\t","Enlace\t","Latitud\t","Longitud\t","Vendedor\t",
            "Referencia Vendedor\t","Fecha Actualizacion\t"])

for direccion in lista_direcciones:

    #Se conecta a la pagina web general de pisos
    soup,flag = conexion_listaPisos(direccion)
    if flag == True:
        llista_items = soup.findAll("div", { "class" : "item-info-container" })

        for item in llista_items:

            link = item.find("a", { "class" : "item-link" })
            titulo = (link.get('title')).encode("utf-8") + "\t"
            enlace = "http://www.idealista.com" + link.get('href') + "\t"
            tipo_piso = tipoPiso(titulo)
            soup2,flag2 = conexionPiso(enlace)
            if flag2 == True:
                try:
                    telefono = soup2.find("p", { "class" : "txt-big txt-bold _browserPhone" }).contents[0]
                except:
                    telefono = "Sin especificar"

                vendedor,referencia_vendedor = buscaVendedor(soup2)
                tipo_via,partes_direccion,numero,barrio,ciudad,calle_piso = tratarDireccion(soup2)
                referencia_piso = referenciaPiso(soup2)
                precio_mes,m2,hab,planta = precio_piso(soup2)
                fecha_carga = time.strftime("%d/%m/%Y")
                nuevo_usado = compruebaPiso(soup2)
                actualizado = compruebaActualizado(soup2)
                descripcion = getDescripcion(item)
                precioM2 = calculoPrecioM2(precio_mes,m2)
                x,y = calculCoordenades(soup2)

                precioM2 = precioM2.replace(".", ",")
                m2 = m2.replace(".", "")
                precio_mes = precio_mes.replace(".", "")

                ####################### PRINTS ##################################
                print "-->" + direccion
                #print "Alquiler"
                #print "Idealista"
                #print "fecha carga: " + fecha_carga
                print "Referencia Piso: " + referencia_piso
                #print "Telefono: " + telefono
                #print "Precio Mes: " + precio_mes
                #print "Vendedor: " + vendedor
                #print "Referencia vendedor" + referencia_vendedor
                #print "tipo de vivienda: " + tipo_piso
                #print "Nuevo/Usado: " + nuevo_usado
                #print "Ciudad: " + ciudad
                #print "Codigo Postal: " + cp
                #print "Direccion completa: " + calle_piso
                #print "Tivo Via: " + tipo_via
                #print "Calle: " + partes_direccion
                #print "Numero: " + numero
                #print "Barrio:" + barrio
                #print "Precio/Mes: " + precio_mes
                #print "m2: " + m2
                #print "Habitaciones: " + hab
                #print "Planta: " + planta
                #print "Precio eur/m2: " + precioM2
                #print "Fecha Actualizacion: " + actualizado
                #print "Descripcion: " + descripcion
                #print "Enlace: " + enlace
                #print "X/Y: " + x + "," + y
                print "------------------------FINAL------------------------"
                try:
                    c.writerow(["Alquiler \t","IDEALISTA \t",fecha_carga + " \t",referencia_piso+" \t",
                                telefono+" \t",tipo_piso+" \t",nuevo_usado+" \t",ciudad.encode("ISO-8859-1")+" \t",
                                cp+" \t",calle_piso.encode("ISO-8859-1")+" \t",tipo_via+" \t",
                                partes_direccion.encode("ISO-8859-1")+" \t",numero+" \t",barrio+" \t",
                                precio_mes+" \t",planta.encode("ISO-8859-1")+" \t",hab+"\t",m2+" \t",
                                precioM2+" \t",enlace+" \t",x+"\t",y+" \t",vendedor.encode("ISO-8859-1")+" \t",
                                referencia_vendedor.encode("ISO-8859-1")+" \t",actualizado.encode("ISO-8859-1")+" \t"])
                except:
                    pass
    else:
        print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
f.close()
