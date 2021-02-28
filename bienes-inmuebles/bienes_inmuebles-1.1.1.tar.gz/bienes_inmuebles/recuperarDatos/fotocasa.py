from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import datetime

from bienes_inmuebles.recuperarDatos.inmueble import Inmueble
from bienes_inmuebles.base_datos.metodosDb import MetodosDb
from bienes_inmuebles.utilidades.urlPath import UrlPath
import requests
import csv

import os

class Fotocasa():
    def __init__(self, urlConsulta):
        self.urlConsulta = urlConsulta

    def creaTxt(self, listaEscribirCsv):
        # crea el fichero datos_fotocasa.txt en el modulo data
        fp = open(str(UrlPath.getPath(__file__, 2)) + "\data\datos_fotocasa.txt", 'a')
        for linea in listaEscribirCsv:
            fp.writelines(str(linea.getIdInmueble()) + ';' +
                          str(linea.getUrlInmueble()) + ';' +
                          str(linea.getFuenteInfo()) + ';' +
                          str(linea.getTipoInmueble()) + ';' +
                          str(linea.getTipoOperacion()) + ';' +
                          str(linea.getPrecio()) + ';' +
                          str(linea.getNumHab()) + ';' +
                          str(linea.getTamano()) + ';' +
                          str(linea.getPlanta()) + ';' +
                          str(linea.getDistrito()) + ';' +
                          str(linea.getCiudad()) + ';' +
                          str(linea.getFecha()) + ';' +
                          str(linea.getEficienciaEnergetica()) + ';' +
                          str(linea.getAscensor()) + ';' +
                          str(linea.getTerraza()) + ';' +
                          str(linea.getTrastero()) + ';' +
                          str(linea.getGaraje()) + ';' +
                          str(linea.getBalcon()) + ';' +
                          str(linea.getAireAcondicionado()) + ';' +
                          str(linea.getPiscina()) + ';' +
                          str(linea.getVendedor()) + ';' +
                          str(linea.getBanios()) +
                          '\n')
        fp.close()


    def crearCsv(self, listaEscribirCsv):
        csvsalida = open(str(UrlPath.getPath(__file__, 2)) + '\data\datos_fotocasa.csv', 'w', newline='')
        salida = csv.writer(csvsalida)
        salida.writerow(['tipoInmueble','tipoOperacion','precio','habitaciones','tamano','planta','distrito','ciudad','eficienciaEnergetica','ascensor','terraza','trastero','garaje','balcon','aireAcondicinado','piscina','banos'])
        salida.writerows(listaEscribirCsv)
        del salida
        csvsalida.close()

    def getDistrito(self, url):
        return (url.split("/")[7])

    def getCiudad(self, url):
        return (url.split("/")[6])

    def getTipoOperacion(self, url):
        if (url.find("comprar")!=-1):
            operationType = 1
        elif (url.find("alquiler")!=-1):
            operationType = 2
        else:
            operationType = 0

        return (operationType)

    def getTipoInmueble(self, url):
        if (url.find("vivienda")!=-1):
            tipoInmueble = 1
        elif (url.find("locales")!=-1):
            tipoInmueble = 2
        else:
            tipoInmueble = 0

        return (tipoInmueble)



    def getPoblacion(self, url):
        x = url.split("/")
        return (x[-2])


    def descargarInfo(self, url):
        # browser = webdriver.Firefox()
        browser = webdriver.Chrome()
        browser.get(url)
        time.sleep(5)

        for i in range(25):
            ActionChains(browser).send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(0.5)

        html_txt = browser.page_source
        soup = BeautifulSoup(html_txt)
        listaInmueblesCsv = []
        listaInmueblesDb = []
        productos = soup.find_all('div', class_="re-Card-secondary")

        for producto in productos:

            # Obtenermos la referencia del inmueble
            urlInmueble = producto.findChildren('a', attrs={'class': 're-Card-link'})[0].get('href')
            idInmueble = urlInmueble.split("/")

            if (len(idInmueble) > 6 and idInmueble[-1] == 'd'):
                if (idInmueble[6].isnumeric()):
                    idInmueble = int(idInmueble[6])

                    headersFakeBrowser = [
                        {
                            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                            "Accept-Encoding": "gzip, deflate, br",
                            "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
                            "Host": "www.fotocasa.es",
                            "Upgrade-Insecure-Requests": "1",
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0",
                        },
                    ]

                    urlInmueble = "https://www.fotocasa.es" + urlInmueble

                    # Realizamos peticion HTTPS para obtener la informacion del web
                    req = requests.get(urlInmueble, headers=headersFakeBrowser[0])

                    # Comprobamos que la petición nos devuelve un Status Code = 200
                    status_code = req.status_code
                    if status_code == 200:
                        soup = BeautifulSoup(req.text, "html.parser")

                        # Obtenermos el precio del inmueble
                        precio = producto.findChildren('span', attrs={'class': 're-Card-price'})[0].get_text()
                        precio = precio.replace(".", "")
                        precio = precio.replace("/mes", "")
                        precio = precio.replace("€", "")
                        precio = precio.rstrip()

                        if (precio.find("consultar") != -1):
                            precio = 0

                        # Obtenemos las caracteristicas del inmueble
                        caracteristicas = soup.findChildren('li', attrs={'class':'re-DetailHeader-featuresItem'})

                        numHab = 0
                        tamano = 0
                        banios = 0

                        planta = 0

                        for caracteristica in caracteristicas:
                            texto = caracteristica.get_text()
                            #                        print(texto)
                            if (texto.find("hab") > -1):
                                # Obtenermos el numero de habitaciones
                                if (texto.find("habs") > -1):
                                    numHab = texto.replace(" habs.", "")
                                elif (texto.find("hab") > -1):
                                    numHab = texto.replace(" hab.", "")

                            elif (texto.find("m²") > -1):
                                # Obtenemos el tamaño del inmueble
                                if (texto.find("terreno") > -1):
                                    tamano = texto.replace(" m² terreno", "")
                                    tamano = tamano.replace(".", "")
                                else:
                                    tamano = texto.replace(" m²", "")
                                    tamano = tamano.replace(".", "")

                            elif (texto.find("baño") > -1):
                                if (texto.find("baños") > -1):
                                    banios = texto.replace(" baños","")
                                elif (texto.find("baño") > -1):
                                    banios = texto.replace(" baño", "")

                            #elif (texto.find("con ascensor") > -1):
                               # ascensor = True

                            elif (texto.find("Bajo") > -1):
                                planta = 0

                            elif (texto.find("Planta") > -1):
                                planta = texto.replace("ª Planta", "")

                        caracteristicas = soup.findChildren('div', attrs={'class': 're-DetailFeaturesList-featureContent'})

                        ascensor = False
                        eficienciaEnergetica = ""
                        garaje = "No-detallado"
                        for caracteristica in caracteristicas:
                            texto = caracteristica.get_text()
                            if (texto.find("Ascensor") > -1):
                                if (texto.find("Sí") > -1):
                                    ascensor = True
                                else:
                                    ascensor = False

                            elif (texto.find("Consumo energía") > -1):
                                if (texto.find("A") > -1):
                                    eficienciaEnergetica = "A"
                                elif (texto.find("B") > -1):
                                    eficienciaEnergetica = "B"
                                elif (texto.find("C") > -1):
                                    eficienciaEnergetica = "C"
                                elif (texto.find("D") > -1):
                                    eficienciaEnergetica = "D"
                                elif (texto.find("E") > -1):
                                    eficienciaEnergetica = "E"
                                elif (texto.find("F") > -1):
                                    eficienciaEnergetica = "F"
                                elif (texto.find("G") > -1):
                                    eficienciaEnergetica = "G"
                                else:
                                    eficienciaEnergetica = ""

                            elif (texto.find("Parking") > -1):
                                garaje = texto.replace("Parking", "")

                        caracteristicas = soup.findChildren('li', attrs={'class': 're-DetailExtras-listItem'})
                        terraza = False
                        trastero = False
                        balcon = False
                        aireAcondicionado = False
                        piscina = False
                        for caracteristica in caracteristicas:
                            texto = caracteristica.get_text()
                            if (texto.find("Terraza") > -1):
                                terraza = True
                            elif (texto.find("Trastero") > -1):
                                trastero = True
                            elif (texto.find("Balcón") > -1):
                                balcon = True
                            elif (texto.find("Aire acondicionado") > -1):
                                aireAcondicionado = True
                            elif (texto.find("Piscina") > -1):
                                piscina = True

                        vendedor = soup.findChildren('span', attrs={'class': 're-ContactDetail-inmoContainer-clientName'})
                        if (len(vendedor) > 0):
                            vendedor = vendedor[0].get_text()

                        # Obtencion de la descripcion
                        descripcion = soup.findChildren('p', attrs={'class': 'fc-DetailDescription'})
                        if (len(descripcion) > 0):
                            descripcion = descripcion[0].get_text()
                        else:
                            descripcion = ""

                        fuenteInfo = "fotocasa"
                        tipoInmueble = self.getTipoInmueble(urlInmueble)
                        tipoOperacion = self.getTipoOperacion(urlInmueble)

                        distrito = self.getDistrito(url)
                        ciudad = self.getCiudad(url)

                        fecha = datetime.datetime.now()
                        fecha = str(fecha.year) + "-" + str(fecha.month) + "-" + str(fecha.day)

                        obInmDb = Inmueble(idInmueble, urlInmueble, fuenteInfo, tipoInmueble, tipoOperacion, precio, numHab, tamano,
                                         planta, distrito, ciudad, fecha, descripcion, eficienciaEnergetica, ascensor, terraza,
                                         trastero, garaje, balcon, aireAcondicionado, piscina, vendedor, banios)
                        listaInmueblesDb.append(obInmDb)
                        obInmCsv = [idInmueble, urlInmueble, fuenteInfo, tipoInmueble, tipoOperacion, precio, numHab, tamano, planta,
                                 distrito, ciudad, fecha, eficienciaEnergetica, ascensor, terraza, trastero, garaje,
                                 balcon, aireAcondicionado, piscina, banios]
                        listaInmueblesCsv.append(obInmCsv)


        browser.quit()

        return (listaInmueblesDb, listaInmueblesCsv)


###### APLICACION PRINCIPAL ########




if __name__ == "__main__":
    ObjMetodosDb = MetodosDb()

    direcciones = [
        "https://www.fotocasa.es/es/comprar/viviendas/madrid-capital/arganzuela/l?combinedLocationIds=724%2C14%2C28%2C173%2C0%2C28079%2C0%2C671%2C0&gridType=3&latitude=40.4096&longitude=-3.68624",
        "https://www.fotocasa.es/es/comprar/viviendas/madrid-capital/barajas/l?latitude=40.40099999447889&longitude=-3.7040766977717645&combinedLocationIds=724,14,28,173,0,28079,0,668,0&gridType=3",
        "https://www.fotocasa.es/es/comprar/viviendas/madrid-capital/carabanchel/l?latitude=40.468037022265854&longitude=-3.582424716280453&combinedLocationIds=724,14,28,173,0,28079,0,171,0&gridType=3",
        "https://www.fotocasa.es/es/comprar/viviendas/madrid-capital/centro/l?latitude=40.37959392136568&longitude=-3.739877001407099&combinedLocationIds=724,14,28,173,0,28079,0,672,0&gridType=3",
        "https://www.fotocasa.es/es/comprar/viviendas/madrid-capital/chamartin/l?latitude=40.416861199611624&longitude=-3.7028325693424122&combinedLocationIds=724,14,28,173,0,28079,0,176,0&gridType=3",
        "https://www.fotocasa.es/es/comprar/viviendas/madrid-capital/chamberi/l?latitude=40.4553103039952&longitude=-3.6790275377675594&combinedLocationIds=724,14,28,173,0,28079,0,177,0&gridType=3",
        "https://www.fotocasa.es/es/comprar/viviendas/madrid-capital/ciudad-lineal/l?latitude=40.438617543919925&longitude=-3.7023556174435788&combinedLocationIds=724,14,28,173,0,28079,0,685,0&gridType=3",
        "https://www.fotocasa.es/es/comprar/viviendas/madrid-capital/fuencarral/l?latitude=40.4441705854059&longitude=-3.6525802484224394&combinedLocationIds=724,14,28,173,0,28079,0,187,0&gridType=3",
        "https://www.fotocasa.es/es/comprar/viviendas/madrid-capital/hortaleza/l?latitude=40.49446606429687&longitude=-3.7136771420672146&combinedLocationIds=724,14,28,173,0,28079,0,678,0&gridType=3",
        "https://www.fotocasa.es/es/comprar/viviendas/madrid-capital/latina/l?latitude=40.46881501855609&longitude=-3.641945499708502&combinedLocationIds=724,14,28,173,0,28079,0,675,0&gridType=3",
        "https://www.fotocasa.es/es/comprar/viviendas/madrid-capital/moncloa/l?latitude=40.39225632660759&longitude=-3.7579024169335757&combinedLocationIds=724,14,28,173,0,28079,0,669,0&gridType=3",
        "https://www.fotocasa.es/es/comprar/viviendas/madrid-capital/moratalaz/l?latitude=40.449174073700895&longitude=-3.7395741953059853&combinedLocationIds=724,14,28,173,0,28079,0,191,0&gridType=3",
        "https://www.fotocasa.es/es/comprar/viviendas/madrid-capital/puente-de-vallecas/l?latitude=40.407259583898416&longitude=-3.6443908162015353&combinedLocationIds=724,14,28,173,0,28079,0,677,0&gridType=3",
        "https://www.fotocasa.es/es/comprar/viviendas/madrid-capital/retiro/l?latitude=40.39272222236246&longitude=-3.659177255581731&combinedLocationIds=724,14,28,173,0,28079,0,199,0&gridType=3",
        "https://www.fotocasa.es/es/comprar/viviendas/madrid-capital/salamanca/l?latitude=40.411591900855164&longitude=-3.67337318656686&combinedLocationIds=724,14,28,173,0,28079,0,667,0&gridType=3",
        "https://www.fotocasa.es/es/comprar/viviendas/madrid-capital/san-blas/l?latitude=40.428670212130825&longitude=-3.676313801748082&combinedLocationIds=724,14,28,173,0,28079,0,676,0&gridType=3",
        "https://www.fotocasa.es/es/comprar/viviendas/madrid-capital/tetuan/l?latitude=40.43455248864532&longitude=-3.6117328944176728&combinedLocationIds=724,14,28,173,0,28079,0,681,0&gridType=3",
        "https://www.fotocasa.es/es/comprar/viviendas/madrid-capital/usera/l?latitude=40.459750181899&longitude=-3.698760133898529&combinedLocationIds=724,14,28,173,0,28079,0,205,0&gridType=3",
        "https://www.fotocasa.es/es/comprar/viviendas/madrid-capital/vicalvaro/l?latitude=40.379623008087385&longitude=-3.704375194087928&combinedLocationIds=724,14,28,173,0,28079,0,209,0&gridType=3",
        "https://www.fotocasa.es/es/comprar/viviendas/madrid-capital/villa-de-vallecas/l?latitude=40.401199408868656&longitude=-3.606278537506303&combinedLocationIds=724,14,28,173,0,28079,0,680,0&gridType=3",
        "https://www.fotocasa.es/es/comprar/viviendas/madrid-capital/villaverde/l?latitude=40.36808128794791&longitude=-3.6216737278917877&combinedLocationIds=724,14,28,173,0,28079,0,670,0&gridType=3",
        "https://www.fotocasa.es/es/comprar/viviendas/madrid-capital/vicalvaro/l?latitude=40.379623008087385&longitude=-3.704375194087928&combinedLocationIds=724,14,28,173,0,28079,0,209,0&gridType=3",
        "https://www.fotocasa.es/es/alquiler/viviendas/madrid-capital/arganzuela/l?combinedLocationIds=724%2C14%2C28%2C173%2C0%2C28079%2C0%2C671%2C0&gridType=3&latitude=40.4096&longitude=-3.68624",
        "https://www.fotocasa.es/es/alquiler/viviendas/madrid-capital/barajas/l?latitude=40.40099999447889&longitude=-3.7040766977717645&combinedLocationIds=724,14,28,173,0,28079,0,668,0&gridType=3",
        "https://www.fotocasa.es/es/alquiler/viviendas/madrid-capital/carabanchel/l?latitude=40.468037022265854&longitude=-3.582424716280453&combinedLocationIds=724,14,28,173,0,28079,0,171,0&gridType=3",
        "https://www.fotocasa.es/es/alquiler/viviendas/madrid-capital/centro/l?latitude=40.37959392136568&longitude=-3.739877001407099&combinedLocationIds=724,14,28,173,0,28079,0,672,0&gridType=3",
        "https://www.fotocasa.es/es/alquiler/viviendas/madrid-capital/chamartin/l?latitude=40.416861199611624&longitude=-3.7028325693424122&combinedLocationIds=724,14,28,173,0,28079,0,176,0&gridType=3",
        "https://www.fotocasa.es/es/alquiler/viviendas/madrid-capital/chamberi/l?latitude=40.4553103039952&longitude=-3.6790275377675594&combinedLocationIds=724,14,28,173,0,28079,0,177,0&gridType=3",
        "https://www.fotocasa.es/es/alquiler/viviendas/madrid-capital/ciudad-lineal/l?latitude=40.438617543919925&longitude=-3.7023556174435788&combinedLocationIds=724,14,28,173,0,28079,0,685,0&gridType=3",
        "https://www.fotocasa.es/es/alquiler/viviendas/madrid-capital/fuencarral/l?latitude=40.4441705854059&longitude=-3.6525802484224394&combinedLocationIds=724,14,28,173,0,28079,0,187,0&gridType=3",
        "https://www.fotocasa.es/es/alquiler/viviendas/madrid-capital/hortaleza/l?latitude=40.49446606429687&longitude=-3.7136771420672146&combinedLocationIds=724,14,28,173,0,28079,0,678,0&gridType=3",
        "https://www.fotocasa.es/es/alquiler/viviendas/madrid-capital/latina/l?latitude=40.46881501855609&longitude=-3.641945499708502&combinedLocationIds=724,14,28,173,0,28079,0,675,0&gridType=3",
        "https://www.fotocasa.es/es/alquiler/viviendas/madrid-capital/moncloa/l?latitude=40.39225632660759&longitude=-3.7579024169335757&combinedLocationIds=724,14,28,173,0,28079,0,669,0&gridType=3",
        "https://www.fotocasa.es/es/alquiler/viviendas/madrid-capital/moratalaz/l?latitude=40.449174073700895&longitude=-3.7395741953059853&combinedLocationIds=724,14,28,173,0,28079,0,191,0&gridType=3",
        "https://www.fotocasa.es/es/alquiler/viviendas/madrid-capital/puente-de-vallecas/l?latitude=40.407259583898416&longitude=-3.6443908162015353&combinedLocationIds=724,14,28,173,0,28079,0,677,0&gridType=3",
        "https://www.fotocasa.es/es/alquiler/viviendas/madrid-capital/retiro/l?latitude=40.39272222236246&longitude=-3.659177255581731&combinedLocationIds=724,14,28,173,0,28079,0,199,0&gridType=3",
        "https://www.fotocasa.es/es/alquiler/viviendas/madrid-capital/salamanca/l?latitude=40.411591900855164&longitude=-3.67337318656686&combinedLocationIds=724,14,28,173,0,28079,0,667,0&gridType=3",
        "https://www.fotocasa.es/es/alquiler/viviendas/madrid-capital/san-blas/l?latitude=40.428670212130825&longitude=-3.676313801748082&combinedLocationIds=724,14,28,173,0,28079,0,676,0&gridType=3",
        "https://www.fotocasa.es/es/alquiler/viviendas/madrid-capital/tetuan/l?latitude=40.43455248864532&longitude=-3.6117328944176728&combinedLocationIds=724,14,28,173,0,28079,0,681,0&gridType=3",
        "https://www.fotocasa.es/es/alquiler/viviendas/madrid-capital/usera/l?latitude=40.459750181899&longitude=-3.698760133898529&combinedLocationIds=724,14,28,173,0,28079,0,205,0&gridType=3",
        "https://www.fotocasa.es/es/alquiler/viviendas/madrid-capital/vicalvaro/l?latitude=40.379623008087385&longitude=-3.704375194087928&combinedLocationIds=724,14,28,173,0,28079,0,209,0&gridType=3",
        "https://www.fotocasa.es/es/alquiler/viviendas/madrid-capital/villaverde/l?latitude=40.3472523466546&longitude=-3.6934487165321173&combinedLocationIds=724,14,28,173,0,28079,0,670,0&gridType=3",
        "https://www.fotocasa.es/es/alquiler/viviendas/madrid-capital/vicalvaro/l?latitude=40.379623008087385&longitude=-3.704375194087928&combinedLocationIds=724,14,28,173,0,28079,0,209,0&gridType=3",
        "https://www.fotocasa.es/es/alquiler/viviendas/madrid-capital/villa-de-vallecas/l?latitude=40.401199408868656&longitude=-3.606278537506303&combinedLocationIds=724,14,28,173,0,28079,0,680,0&gridType=3"
    ]

    # borra el fichero datos_fotocasa.txt del directorio data
    if os.path.exists(str(UrlPath.getPath(__file__, 2)) + "\data\datos_fotocasa_final.csv"):
        os.remove(str(UrlPath.getPath(__file__, 2)) + "\data\datos_fotocasa_final.csv")

    listaEscribirCsv = []
    for url in direcciones:
        for pagina in range(1, 100):
            pestana = "/l/" + str(pagina) + "/?"
            urlConsulta = url.replace("/l?", pestana)

            print(urlConsulta)
            fotocasa = Fotocasa(urlConsulta)
            objetosDb, objetosCsv = fotocasa.descargarInfo(urlConsulta)


            for inmueble in objetosDb:
                ObjMetodosDb.addDbFotocasa(inmueble)


            for inmueble in objetosCsv:
                listaEscribirCsv.append(inmueble)


            if (len(objetosDb) < 30):
                break

            time.sleep(10)

    fotocasa.crearCsv(listaEscribirCsv)