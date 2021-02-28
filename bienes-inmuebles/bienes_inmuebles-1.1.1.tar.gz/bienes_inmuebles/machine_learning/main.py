from joblib import load
import os
import numpy as np
import csv

from bienes_inmuebles.preprocesar.csv_preprocesamiento import PATH4
from bienes_inmuebles.formulario.metodosFormulario import MetodosFormulario
from bienes_inmuebles.utilidades.urlPath import UrlPath


def main():
    """Llamada a file para la introduccion de datos dl usuario por teclado"""
    form = MetodosFormulario()
    objetoPred = form.formulario()

    """Seleccion del modelo en funcion de los datos introducidos por teclado: 
    1) Compra
    2) Alquiler"""
    if objetoPred.getTipoOperacion() == 1:
        modelo = load(os.path.join(PATH4, "data/model_compra.joblib"))
        fichero_path = os.path.join(PATH4, "data/scaler_compra.pkl")
        scaler = load(open(fichero_path, 'rb'))

    elif objetoPred.getTipoOperacion() == 2:
        modelo = load(os.path.join(PATH4, "data/model_alquiler.joblib"))
        fichero_path = os.path.join(PATH4, "data/scaler_alquiler.pkl")
        scaler = load(open(fichero_path, 'rb'))

    """Prediccion"""
    predecir = np.array([1,
                         objetoPred.getTipoOperacion(),
                         objetoPred.getHabitaciones(),
                         objetoPred.getTamano(),
                         objetoPred.getPlanta(),
                         objetoPred.getAscensor(),
                         objetoPred.getTerraza(),
                         objetoPred.getTrastero(),
                         objetoPred.getBalcon(),
                         objetoPred.getAireAcondicionado(),
                         objetoPred.getPiscina(),
                         objetoPred.getBanos(),
                         objetoPred.getGaraje_Comunitario(),
                         objetoPred.getGaraje_No_detallado(),
                         objetoPred.getGaraje_Privado(),
                         objetoPred.getDistrito_arganzuela(),
                         objetoPred.getDistrito_barajas(),
                         objetoPred.getDistrito_carabanchel(),
                         objetoPred.getDistrito_centro(),
                         objetoPred.getDistrito_chamartin(),
                         objetoPred.getDistrito_chamberi(),
                         objetoPred.getDistrito_ciudad_lineal(),
                         objetoPred.getDistrito_fuencarral(),
                         objetoPred.getDistrito_hortaleza(),
                         objetoPred.getDistrito_latina(),
                         objetoPred.getDistrito_moncloa(),
                         objetoPred.getDistrito_moratalaz(),
                         objetoPred.getDistrito_puente_de_vallecas(),
                         objetoPred.getDistrito_retiro(),
                         objetoPred.getDistrito_salamanca(),
                         objetoPred.getDistrito_san_blas(),
                         objetoPred.getDistrito_tetuan(),
                         objetoPred.getDistrito_usera(),
                         objetoPred.getDistrito_vicalvaro(),
                         objetoPred.getDistrito_villa_de_vallecas(),
                         objetoPred.getDistrito_villaverde(),
                         objetoPred.getCiudad(),
                         objetoPred.getEficienciaEnergetica_A(),
                         objetoPred.getEficienciaEnergetica_B(),
                         objetoPred.getEficienciaEnergetica_C()])

    escalado = scaler.transform(predecir.reshape(1, -1))
    resultado_final = modelo.predict(escalado)[0]  # Get out of the array
    resultado_final = float(resultado_final)
    print("El resultado de su prediccion es:", round(resultado_final, 2),"€")

    """Exportar CSV con los datos de la prediccion"""
    csvPrediccion = open(str(UrlPath.getPath(__file__, 2)) + '\data\datos_usuario_prediccion.csv', 'w', newline='')
    salida = csv.writer(csvPrediccion)
    salida.writerow(
        ['tipoInmueble', 'tipoOperacion', 'Habitaciones', 'Tamano', 'Planta', 'Ascensor', 'Terraza', 'Trastero',
         'Balcon', 'AireAcondicionado', 'Piscina', 'Banos', 'Garaje_Comunitario', 'Garaje_No_detallado',
         'Garaje_Privado',
         'Distrito_arganzuela', 'Distrito_barajas', 'Distrito_carabanche', 'Distrito_centro', 'Distrito_chamartin',
         'Distrito_chamberi', 'Distrito_ciudad_lineal', 'Distrito_fuencarral', 'Distrito_hortaleza', 'Distrito_latina',
         'Distrito_moncloa', 'Distrito_moratalaz', 'Distrito_puente_de_vallecas', 'Distrito_retiro',
         'Distrito_salamanca',
         'Distrito_san_blas', 'Distrito_tetuan', 'Distrito_usera', 'Distrito_vicalvaro', 'Distrito_villa_de_vallecas',
         'Distrito_villaverde', 'Ciudad', 'EficienciaEnergetica_A', 'EficienciaEnergetica_B', 'EficienciaEnergetica_C',
         'Prediccion'])
    salida.writerow([1,
                     objetoPred.getTipoOperacion(),
                     objetoPred.getHabitaciones(),
                     objetoPred.getTamano(),
                     objetoPred.getPlanta(),
                     objetoPred.getAscensor(),
                     objetoPred.getTerraza(),
                     objetoPred.getTrastero(),
                     objetoPred.getBalcon(),
                     objetoPred.getAireAcondicionado(),
                     objetoPred.getPiscina(),
                     objetoPred.getBanos(),
                     objetoPred.getGaraje_Comunitario(),
                     objetoPred.getGaraje_No_detallado(),
                     objetoPred.getGaraje_Privado(),
                     objetoPred.getDistrito_arganzuela(),
                     objetoPred.getDistrito_barajas(),
                     objetoPred.getDistrito_carabanchel(),
                     objetoPred.getDistrito_centro(),
                     objetoPred.getDistrito_chamartin(),
                     objetoPred.getDistrito_chamberi(),
                     objetoPred.getDistrito_ciudad_lineal(),
                     objetoPred.getDistrito_fuencarral(),
                     objetoPred.getDistrito_hortaleza(),
                     objetoPred.getDistrito_latina(),
                     objetoPred.getDistrito_moncloa(),
                     objetoPred.getDistrito_moratalaz(),
                     objetoPred.getDistrito_puente_de_vallecas(),
                     objetoPred.getDistrito_retiro(),
                     objetoPred.getDistrito_salamanca(),
                     objetoPred.getDistrito_san_blas(),
                     objetoPred.getDistrito_tetuan(),
                     objetoPred.getDistrito_usera(),
                     objetoPred.getDistrito_vicalvaro(),
                     objetoPred.getDistrito_villa_de_vallecas(),
                     objetoPred.getDistrito_villaverde(),
                     objetoPred.getCiudad(),
                     objetoPred.getEficienciaEnergetica_A(),
                     objetoPred.getEficienciaEnergetica_B(),
                     objetoPred.getEficienciaEnergetica_C(),
                     round(resultado_final, 2)])
    del salida
    csvPrediccion.close()


if __name__ == "__main__":
    main()
