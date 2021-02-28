"""IMPORTS"""
# Import Librerias Externas
from pathlib import Path
import numpy as np
# import numpy as * is not a best practice, no sabes de que libreria viene la funcion porque importa todas las funciones
import pandas as pd
from scipy import stats
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import Normalizer
from sklearn.preprocessing import Binarizer
import copy
from joblib import dump
import os

# Import libreria interna
from bienes_inmuebles.preprocesar.csv_exploracion import CSVExploracion

# from .. import csv_exploracion -> significa hacia atras o bajar un nivel (para buscar en carpetas por debajo)

"""CONSTANTES (en mayuscula)"""
path = Path(__file__)  # PATH A LA FILE EN CUALQUIER ORDENADOR
path2 = Path(path.parent)  # Un directorio hacia atras
path3 = Path(path2.parent)
PATH4 = str(Path(path3.parent))

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


class CSVPreprocesamiento():
    def __init__(self, csv):
        self.csv = csv

    """Permite sobrescribir objetos (inplace=True) o realizar copias (inplace=False)"""
    def _inplace(self, atributo, valor_atributo, inplace=False):
        if inplace:
            setattr(atributo, valor_atributo)
        else:
            nuevo_objeto = copy.deepcopy(self)  # Copia del objeto en otro registro de memoria
            setattr(nuevo_objeto, atributo, valor_atributo)
            # self.atributo = valor_atributo
            # self.df = resultado_df
            return nuevo_objeto

    "Castear columnas indicadas"
    def casteo_columnas(self, columnas_casteo, inplace=False):
        for clave, valor in columnas_casteo.items():
            self.df[clave] = self.df[clave].astype(valor)
        return self._inplace("df", self.df, inplace) # Permite pasar tanto CSVs (antes de leerlo) o el Dataframe

    "Codifcar datos categoricos a datos numericos"
    def one_hot_encoding(self, columna, inplace=False):
        y = pd.get_dummies(self.df[columna], prefix=columna)
        # Borra la columna no codificada (columna introducida como input)
        self.df.drop(columna, axis='columns', inplace=True)
        # Concatena las nuevas columnas con el Dataframe
        self.df = pd.concat([self.df, y], axis=1)
        return self._inplace("df", self.df, inplace)

    """Elimina filas con duplicados"""
    def duplicados(self, inplace=False):
        df_resultado = self.df.drop_duplicates()
        return self._inplace("df", df_resultado, inplace)

    """Eliminar filas (axis = 0) o columnas (axis = 1). El limite de NaN lo marca number"""
    def dropna(self, number=10000, axis=1, inplace=False):
        length = self.df.shape[axis - 1] # Esta opereacion permite que siempre salga 0, es decir, logitud de filas
        df_resultado = self.df.dropna(thresh=length - number, axis=axis)
        valor = self._inplace("df", df_resultado, inplace)
        return valor

    """Filtrar Dataset por columnas con datos numericos"""
    def ints(self, inplace=False):
        df_resultado = self.df.select_dtypes(include=["int64", "float64", "uint8"])
        return self._inplace("df", df_resultado, inplace)

    """Imputar valores faltantes. La estrategia puede ser:
                                    - "constant" y "most frecuent" para categoricos y numericos
                                    - "mean" y "median" para solo numericos"""
    def mvs(self, columns=None, strategy="constant", inplace=False):
        imp_mean = SimpleImputer(missing_values=np.nan, strategy=strategy)
        aux = imp_mean.fit_transform(self.df)
        try:
            df_resultado = pd.DataFrame(data=aux, columns=self.df.columns)
        except ValueError:
            raise ValueError("Necesitas borrar columnas con NANs y columnas con Strings primero. También puede que "
                             "tengas mas columas que anters "
                             "Ejecutar self.dropna() y self.ints() antes de self.mvs()")
        return self._inplace("df", df_resultado, inplace)

    """Eliminar filas con outliers"""
    def outliers(self, grado=3, inplace=False):  # Eliminar filas con outlier y escoger grado de eliminacion)
        z_scores = stats.zscore(self.df)  # self.df.values ????
        where_are_NaNs = np.isnan(z_scores)
        z_scores[where_are_NaNs] = 0
        abs_z_scores = np.abs(z_scores)
        filtered_entries = (abs_z_scores < grado).all(axis=1)  # solucion para sustituir NaN x 0 en la lista de listas??
        print(filtered_entries)
        df_resultado = self.df[filtered_entries]
        return self._inplace("df", df_resultado, inplace)

    """Reescalar dataset"""
    def reescalar(self, inplace=False):
        scaler = MinMaxScaler(feature_range=(0, 1))
        df_resultado = scaler.fit_transform(self.df)
        return self._inplace("df", df_resultado, inplace)

    """Estandarizar dataset y guardar el scaler en formato pickle"""
    def estandarizar(self,  scaler_file, inplace=False):
        scaler = StandardScaler().fit(self.df)  # aprende la distribucion de los dstos

        #if compra==True:
        fichero_path = scaler_file
        #elif compra==False:
        #fichero_path = os.path.join(PATH4, "data/scaler_alquiler.pkl")

        dump(scaler, open(fichero_path, 'wb'))
        np_escalado = scaler.transform(self.df)  # coge la distribucion y la estandariza
        df_resultado = pd.DataFrame(np_escalado, columns=self.df.columns)
        return self._inplace("df", df_resultado, inplace)

    """Normalizar dataset"""
    def normalizar(self, inplace=False):
        scaler = Normalizer().fit(self.df)
        df_resultado = scaler.transform(self.df)
        return self._inplace("df", df_resultado, inplace)

    """Binarizar dataset"""
    def binarizar(self, inplace=False):
        binarizer = Binarizer(threshold=0.0).fit(self.df)
        df_resultado = binarizer.transform(self.df)
        return self._inplace("df", df_resultado, inplace)


if __name__ == "__main__":
    preprocesamiento = CSVPreprocesamiento("../../data/csv_barcelona.csv")
    prueba = preprocesamiento.dropna()
    print(path)
    print(prueba.df.info())
