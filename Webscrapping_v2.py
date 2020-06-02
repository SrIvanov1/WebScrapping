import requests
import bs4
from pandas import DataFrame
from selenium import webdriver
import csv


# !/usr/bin/env python
# -- coding: utf-8 --

# Establecemos rutas dinámicas (que variamos según interés)
distrito = ['Arganzuela', 'madrid_capital_barajas', 'madrid_capital_carabanchel', 'madrid_capital_centro',
            'madrid_capital_chamartin', 'chamberi_distrito', 'ciudad_lineal', 'fuencarral_el_pardo', 'hortaleza',
            'latina', 'moncloa_aravaca', 'moratalaz', 'puente_de_vallecas', 'madrid_capital_retiro',
            'madrid_capital_salamanca', 'madrid_capital_san_blas', 'tetuan', 'madrid_capital_usera',
            'madrid_capital_vicalvaro', 'villa_de_vallecas', 'villaverde_distrito']
num_pag = 2  # número de páginas a scrapear
dist_num = 0
sinDatos = 'N/A'
nombre_excel = 'Pisos'

# Establecemos rutas estáticas
Excel = 'C:/Users/leonr/Desktop/' + nombre_excel + '.csv'
url = ('https://www.pisos.com/alquiler/pisos-' + distrito[dist_num] + '/desc/')
chromedriver = 'D:\Coding\Tools\chromedriver'

# Descargamos el código fuente de la página y nos avisa de posibles errores HTTP
res = requests.get(url)
res.raise_for_status()
Soup = bs4.BeautifulSoup(res.content.decode('utf-8'), 'lxml')  # lxml o html.parse según qué estemos buscando

# print(Soup.prettify()[:100000]) -- Si queremos ver el código página (organizado con .prettify)

# Esto nos sirve para ver los resultados que estamos filtrando (a modo de prueba)
# Filtramos resultados
Elementos_h3 = Soup.findAll("h3", {"class": "title"})
Precio = Soup.findAll("div", {"class": "price"})

print("==================================================")
print(url)
print('Anuncios por página: '+str(len(Elementos_h3)))
print("                                                  ")

# Obtenemos el próximo enlace - En este caso no nos sirve, uso una variable distinta - Podría saber para obtener
# nº de páginas totales
nextLink = Soup.findAll("a", {"id": "lnkPagSig"})

# Variables para rellenar en el DataFrame
piso_titulo = []
piso_precio = []
piso_ubicacion = []
piso_distrito = []
piso_href = []
piso_enlace = []
piso_superficie = []
piso_habitaciones = []
piso_wc = []
piso_garaje = []
piso_trastero = []
piso_terraza = []
piso_piscina = []
piso_aireAcondicionado = []
piso_jardin = []
piso_orientacionSur = []
piso_calefaccion = []
piso_blindado = []
piso_ascensor = []
piso_cocina = []
piso_seguridad = []
piso_lavadero = []
piso_chimenea = []
piso_portero = []
piso_amueblado = []
piso_armariosEmpotrados = []

# Creamos el DataFrame (introduciendo nuestros criterios)
data = {'Titulo': piso_titulo, 'Precio': piso_precio, 'Ubicacion': piso_ubicacion, 'Distrito': piso_distrito,
        'Origen': piso_href, 'Enlace': piso_enlace, 'Superficie': piso_superficie, 'Habitaciones': piso_habitaciones,
        'Baños': piso_wc, 'Garaje': piso_garaje, 'Trastero': piso_trastero, 'Terraza': piso_terraza,
        'Piscina': piso_piscina, 'Aire acondicionado': piso_aireAcondicionado, 'Jardín': piso_jardin,
        'Orientación: Sur': piso_orientacionSur, 'Calefacción': piso_calefaccion, 'Puerta blindada': piso_blindado,
        'Ascensor': piso_ascensor, 'Cocina': piso_cocina, 'Sistema de seguridad': piso_seguridad,
        'Lavadero': piso_lavadero, 'Chimenea': piso_chimenea, 'Portero': piso_portero, 'Amueblado': piso_amueblado,
        'Armarios empotrados': piso_armariosEmpotrados
        }

# Definimos CSV (introducimos nombres de columnas, mismo orden que DataFrame)
with open(nombre_excel, mode='w') as csv_file:
    fieldnames = list(data.keys())
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()


# Función (loop) que extrae todos los datos de la web
def pisosscrapping(url_main, page_number):
    # Sacamos datos de la página principal - BeautifulSoup
    next_page = url_main + str(page_number)
    response = requests.get(next_page)
    soup_nextpage = bs4.BeautifulSoup(response.content.decode('utf-8'), "html.parser")
    titulo = soup_nextpage.findAll("a", {"class": "anuncioLink"})
    precio = soup_nextpage.findAll("div", {"class": "price"})
    ubicacion = soup_nextpage.findAll("div", {"class": "location"})
    enlace = soup_nextpage.findAll("section", {"itemtype": "http://schema.org/ImageObject"})
    piso_enlace_temp = []

    for link in enlace:
        piso_enlace.append(link.find("meta", {"itemprop": "url"})['content'])
        piso_enlace_temp.append(link.find("meta", {"itemprop": "url"})['content'])
    for x in range(len(enlace)):
        piso_precio.append(precio[x].text.strip())
        piso_titulo.append(titulo[x].text.strip().replace(',', ''))
        piso_ubicacion.append(ubicacion[x].text.strip())
        piso_distrito.append(distrito[dist_num])
        piso_href.append(next_page)

        enlace_piso = 'https://www.pisos.com' + str(piso_enlace_temp[x])

        chrome = webdriver.Chrome(chromedriver)
        chrome.get(enlace_piso)

        response_insidepage = requests.get(enlace_piso)
        soup_insidepage = bs4.BeautifulSoup(response_insidepage.content.decode('utf-8'), "html.parser")
        adicionales = soup_insidepage.findAll("div", {"class": "basicdata-item"})

        datos_piso = ['superficie', 'habitaciones', 'banyos']
        for i in range(len(adicionales)):
            if (str(adicionales[i])[50:60]) == datos_piso[0]:
                piso_superficie.append(str(adicionales[i].text.strip()))
            if (str(adicionales[i])[50:62]) == datos_piso[1]:
                piso_habitaciones.append(str(adicionales[i].text.strip()).replace("habs", "").replace("hab", ""))
            if (str(adicionales[i])[50:56]) == datos_piso[2]:
                piso_wc.append(str(adicionales[i].text.strip())[0:1])

        variables = [piso_superficie, piso_habitaciones, piso_wc, piso_precio, piso_titulo, piso_ubicacion,
                     piso_distrito, piso_href]

        for i in range(len(variables)):
            if len(variables[i]) < len(enlace):
                variables[i].append(sinDatos)

        print("Cargando página " + str(page_number) + ": " + str(int(x*100/(len(enlace)))) + "%")
        print("Número de páginas cargadas: " + str(page_number))

        soup_insidepage_boolean = bs4.BeautifulSoup(response_insidepage.content.decode('utf-8'), "html.parser")
        complementarios = soup_insidepage_boolean.findAll("li", {"class": "charblock-element element-with-bullet"})
        datos_comp = ['Garaje', 'Trastero', 'Terraza', 'Piscina', 'Aire acondicionado', 'Jardín', 'Sur', 'Suroeste',
                      'Sureste', 'Calefacción', 'Puerta blindada', 'Ascensor', 'Cocina', 'Sistema de seguridad',
                      'Lavadero', 'Chimenea', 'Portero', 'Amueblado', 'Armarios empotrados']

        for i in range(len(complementarios)):
            if (str(complementarios[i])[57:63]) == datos_comp[0]:
                piso_garaje.append("1")
            if (str(complementarios[i])[57:65]) == datos_comp[1]:
                piso_trastero.append("1")
            if (str(complementarios[i])[57:64]) == datos_comp[2]:
                piso_terraza.append("1")
            if (str(complementarios[i])[57:64]) == datos_comp[3]:
                piso_piscina.append("1")
            if (str(complementarios[i])[57:75]) == datos_comp[4]:
                piso_aireAcondicionado.append("1")
            if (str(complementarios[i])[57:63]) == datos_comp[5]:
                piso_jardin.append("1")
            if (str(complementarios[i])[84:87]) == datos_comp[6]:
                piso_orientacionSur.append("1")
            if (str(complementarios[i])[84:92]) == datos_comp[7]:
                piso_orientacionSur.append("1")
            if (str(complementarios[i])[84:91]) == datos_comp[8]:
                piso_orientacionSur.append("1")
            if (str(complementarios[i])[57:68]) == datos_comp[9]:
                piso_calefaccion.append("1")
            if (str(complementarios[i])[57:72]) == datos_comp[10]:
                piso_blindado.append("1")
            if (str(complementarios[i])[57:65]) == datos_comp[11]:
                piso_ascensor.append("1")
            if (str(complementarios[i])[57:63]) == datos_comp[12]:
                piso_cocina.append("1")
            if (str(complementarios[i])[57:77]) == datos_comp[13]:
                piso_seguridad.append("1")
            if (str(complementarios[i])[57:65]) == datos_comp[14]:
                piso_lavadero.append("1")
            if (str(complementarios[i])[57:65]) == datos_comp[15]:
                piso_chimenea.append("1")
            if (str(complementarios[i])[57:64]) == datos_comp[16]:
                piso_portero.append("1")
            if (str(complementarios[i])[57:66]) == datos_comp[17]:
                piso_amueblado.append("1")
            if (str(complementarios[i])[57:76]) == datos_comp[18]:
                piso_armariosEmpotrados.append("1")

            # Añadir aquí copiando y duplicando el estilo de los if's de arriba todos los complementarios que quiera
            # para la distancia 57:(57+longitud palabra) -> p. ej. alejandro (9 caracteres) -> [57:66]

        variables_compl = [piso_garaje, piso_trastero, piso_terraza, piso_piscina, piso_aireAcondicionado, piso_jardin,
                           piso_orientacionSur, piso_calefaccion, piso_blindado, piso_ascensor, piso_cocina,
                           piso_seguridad, piso_lavadero, piso_chimenea, piso_portero, piso_amueblado,
                           piso_armariosEmpotrados]

        for i in range(len(variables_compl)):
            if len(variables_compl[i]) < len(enlace):
                variables_compl[i].append("0")

        chrome.close()
    # Contador de nº de páginas (acaba cuando < nº de pág indicado)
    if page_number < num_pag:
        page_number = page_number + 1
        pisosscrapping(url, page_number)


# Llamamos la función, comienza en 1 y va hasta el número de página
pisosscrapping(url, 1)

# Insertamos datos en el DataFrame y generamos el .csv
df = DataFrame(data, columns=fieldnames)
df.to_csv(Excel, index=False, header=True, encoding='utf-8')

print("--------------------------------------------------")
print("Excel actualizado! Ruta: " + Excel)
