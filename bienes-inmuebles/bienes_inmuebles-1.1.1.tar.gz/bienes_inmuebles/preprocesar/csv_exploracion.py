import pandas as pd
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.ensemble import ExtraTreesClassifier

from bienes_inmuebles.preprocesar.csv_plot import CSVPlot


class CSVExploracion(CSVPlot):

    def __init__(self, df):
        self.df = df

    """Muestra informacion general del dataset"""

    def vistazo(self):
        info = self.df.info()
        cabecera = self.df.head()
        final = self.df.tail()
        columnas = self.df.columns.values
        faltantes = self.df.isnull().sum()
        forma = self.df.shape
        print(
            f'\nCABECERA:\n{cabecera}\n\nFINAL:\n{final}\n\nCOLUMNAS:\n{columnas}\n\nMVs:\n{faltantes}\n\nFORMA:\n{forma}')
        return info, cabecera, final, columnas, faltantes, forma

    """Muestra informacion estadistica del dataset. Indicando columnas por una lista realiza ademas la agrupacion"""

    def estadistica(self ,columnas=[], agrupar=None, method="pearson"):
        if columnas:
            df = self.df[columnas]
        else:
            df = self.df
        try:
            agrupar = df.groupby(agrupar).size()
        except TypeError:
            agrupar = None
        describir = df.describe()
        correlaciones = df.corr(method=method)
        sesgo = df.skew()
        media = df.mean()
        print(f'\nAGRUPAR:\n{agrupar}\n\nDESCRIBIR:\n{describir}\n\nCORRELACIONES:\n{correlaciones}\n\nSESGO:\n{sesgo}\n\nMEDIA:\n{media}')
        return agrupar, describir, correlaciones, sesgo, media

    """Indica columnas importantes del Dataset para ML"""

    def caracteristicas(self, n_caracteristicas=3):
        print(self.df.columns.values)
        X = self.df[:, 0:8]
        Y = self.df[:, 8]

        # 2.Extracción de características con RFE
        # modelo = LogisticRegression(solver='lbfgs')
        modelo = SGDClassifier()
        rfe = RFE(modelo, n_caracteristicas)
        fit = rfe.fit(X, Y)
        print(f"Numero de Caracteristicas Seleccionadas por RFE: {fit.n_features_}\n")
        print(f"Columnas del Dataset: {self.df.columns.values}")
        print(f"Caracteristicas Seleccionadas:\n{fit.support_}\nRanking de Caracteristicas:\n{fit.ranking_}")

        # 4.Extracción de importancia de las características
        modelo = ExtraTreesClassifier()
        fit = modelo.fit(X, Y)
        print(f"Importancia de caracteristicas: {fit.feature_importances_}")


if __name__ == "__main__":
    df = pd.read_csv("../../data/csv_barcelona.csv")
    exploracion = CSVExploracion(df)
    exploracion.caracteristicas()
