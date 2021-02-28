"""IMPORTS"""
# Import Librerias Externas
import os
from pathlib import Path
import pandas as pd

# Import libreria interna
from bienes_inmuebles.preprocesar.csv_exploracion import CSVExploracion
from bienes_inmuebles.preprocesar.csv_preprocesamiento import CSVPreprocesamiento

# from .. import csv_exploracion -> significa hacia atras o bajar un nivel (para buscar en carpetas por debajo)

"""CONSTANTES (en mayuscula)"""
# Recupera la ruta del fichero actual yendo un directorio hacia atras
path = Path(__file__)  # C:\bienes_inmuebles\bienes_inmuebles\dataset\csv_utilities.py
path2 = Path(path.parent)  # C:\bienes_inmuebles\bienes_inmuebles\dataset
path3 = Path(path2.parent)  # C:\bienes_inmuebles\bienes_inmuebles
PATH4 = str(Path(path3.parent))  # C:\bienes_inmuebles

"""CLASE y FUNCIONES"""
# class Moto o Coche (Vehiculo)
# class caracteristicas especificas (caracteristicas generales)
# class HIJO (PADRE)
# -------------------Dependencias------------------------
# CSV_PLOT -> CSV_Explolaracion --> CSV
# CSV_Preprocesamiento --> CSV
#
# CSV_ML --> CSV
# CSV --> main

# -------------------2 formas de Herenciar---------------
# from bienes_inmuebles.dataset.csv_exploracion import CSVExploracion
# class CSV (csv_exploracion.CSVExploracion, csv_prepocesamiento.CSVPreprocesamiento)

"""
ULITMA CLASE DE ARQUITECTURA

ARQUITECTURA HERENCIA 1

CSV(CSVPlots, CSVPreprocesamiento)

Pickle (CSVPlots)

 hereda de CSVPreprocesamientov y CSVExploracion
 
CSVPreprocesamiento --> Metodos para limpiar csvs

CSVPlots --> Metodos para hacer estadistica

ARQUITECTURA HERENCIA 2

Motos() y Coches() que heredan de Vehiculo()

    Vehiculo: Caract general (motor, marca, comunes coche moto)
    Motos y Coche (cosas especificas)
"""


class CSV(CSVExploracion, CSVPreprocesamiento):
    def __init__(self, csv=None, df=None):
        if csv:
            self.csv = csv
            self.df = pd.read_csv(self.csv, sep=';')
        else:
            self.csv = None
            self.df = df


"""EJECUCION"""
# Path Absoluto: solo funciona en mi PC
# Path Relativo: solo funciona si estan en el mismo Working Directory

# Permite ejecutar el fichero una vez posicionado directamente en él, pero NO cuando se importa
if __name__ == "__main__":
    # Programar como fichero unico -> linkar/empalmar con otros ficheros, clases ofunciones -> Asegurar Modularidad
    csv = CSV(os.path.join(PATH4, "data/csv_barcelona.csv"))
    csv.vistazo(show=True)
    csv.plot()
    csv_2 = csv.dropna()
    print(csv_2)
