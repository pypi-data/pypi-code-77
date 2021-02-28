import time
import os

from bienes_inmuebles.base_datos.metodosDb import MetodosDb
from bienes_inmuebles.utilidades.urlPath import UrlPath
from bienes_inmuebles.recuperarDatos.fotocasa import Fotocasa

def main():
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

            if len(objetosDb) < 30:
                break

            time.sleep(10)

    fotocasa.crearCsv(listaEscribirCsv)


if __name__ == "__main__":
    main()
