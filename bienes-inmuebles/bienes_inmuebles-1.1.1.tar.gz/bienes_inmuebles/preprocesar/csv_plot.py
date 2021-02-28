import os
import pandas as pd
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
from pathlib import Path

"""CONSTANTES (en mayuscula)"""
path = Path(__file__)  # PATH A LA FILE EN CUALQUIER ORDENADOR
path2 = Path(path.parent)  # Un directorio hacia atras
path3 = Path(path2.parent)
PATH4 = str(Path(path3.parent))


class CSVPlot():
    def __init__(self, df):
        self.df = df

    """Muestra el grafico del dataset por pantalla output=False o 
    Guarda una imagen graficada por columna en /data output=True"""
    def _show(self, output=False):
        if not output:
            plt.show()
        else:
            columns = self.df.columns.values
            for column in columns:
                try:
                    my_file = f"data/{column}.png"
                    plt.savefig(os.path.join(PATH4, my_file))
                except ValueError:
                    pass

    """Grafico Barras"""
    def plot_histograma(self, output=False):
        self.df.hist()
        self._show(output)

    """Grafico Densidad"""
    def plot_densidad(self, por_columnas=False):
        self.df.plot(subplots=True, layout=(10, 4), sharex=False)  # kind="density" ¿No funciona?
        self._show(output)

    """Grafico Box & Whisker"""
    def plot_bigotes(self, por_columnas=False):
        if por_columnas:
            columns = self.df.columns.values
            for column in columns:
                fig1, ax1 = plt.subplots()
                ax1.set_title(column)
                ax1.boxplot(self.df[column])
                my_file = f"data/{column}.png"
                plt.savefig(os.path.join(PATH4, my_file))
        else:
            self.df.plot(kind='box', subplots=True, layout=(10, 5), sharex=False, sharey=False)
            self._show(por_columnas)

    """Matriz Correlacion"""
    def plot_correlacion(self, output=False):
        correlaciones = self.df.corr()
        fig = plt.figure()
        ax = fig.add_subplot(111)
        cax = ax.matshow(correlaciones, vmin=-1, vmax=1)
        fig.colorbar(cax)
        self._show(output)

    """Matriz Dispersion"""
    def plot_dispersion(self, output=False):
        scatter_matrix(self.df, alpha=0.2)
        self._show(output)

    """Elimina imagenes generadas en carpeta /data"""
    def borrar_output(self):
        columns = self.df.columns.values
        for column in columns:
            try:
                my_file = f"data/{column}.png"
                os.remove(os.path.join(PATH4, my_file))
            except ValueError:
                pass
        """    
        if os.path.exists("archivo_ejemplo.txt"):
            os.remove("archivo_ejemplo.txt")
        else:
            print("El archivo no existe")"""


if __name__ == "__main__":
    df = pd.read_csv("../../data/csv_barcelona.csv")
    # df = pd.DataFrame(np.random.randn(1000, 4), columns=['A', 'B', 'C', 'D'])
    plot = CSVPlot(df)
    plot.plot_bigotes()