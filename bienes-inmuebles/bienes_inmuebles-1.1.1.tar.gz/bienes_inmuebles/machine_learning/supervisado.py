import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

from bienes_inmuebles.machine_learning.modelos import Modelo


class Supervisado():

    def __init__(self, clf, X, Y):
        self.clf = clf
        self.X = X
        self.Y = Y
        self.clf_optimizado = None
        self.best_score = None

    # DE DONDE VIENEN LOS DATOS? CSV --> PREPROCES --> TrainTestSplitter

    # Argumentos Obligatorios: son parametros posicionales
    # Argumentos Opcionales: son parametros no posicionales (aquellos que tienen un valor por defecto mediante un igual)
    def optimizacion(self, clave, parametros, cv=10, scoring='r2'):

        if self.X.tolist() and self.Y.tolist() and parametros:
            grid = GridSearchCV(self.clf, parametros, scoring=scoring, cv=cv)
            grid.fit(self.X, self.Y)
            self.clf_optimizado = grid.best_estimator_
            self.best_score = grid.best_score_
            return self.clf_optimizado, self.best_score
        else:
            cross_val = cross_val_score(clave, self.X, self.Y, cv=cv, scoring=scoring)
            modelo_entrenado = clave.fit(self.X, self.Y)
            return modelo_entrenado, cross_val.mean()

    def predict(self, X_test):  # Error en predict cuando no recibe modelo optimizado
        if self.clf_optimizado:
            pred = self.clf_optimizado.predict(X_test)
            return pred
        else:
            pred = self.clf.predict(X_test)
            return pred


def prepare_dataset(X_columns, Y_columns):
    X_train, X_test, y_train, y_test = train_test_split(X_columns, Y_columns, test_size=0.3, random_state=42)
    return X_train, X_test, y_train, y_test


def regresion(X_train, X_test, y_train, y_test):
    obj_eva = Modelo()
    for classificador, parametros in obj_eva.modelos_regresion().items():
        modelo = Supervisado(classificador, X_train, y_train)
        model, score = modelo.optimizacion(classificador, parametros)  # train -> train/validation -> score
        y_pred = modelo.predict(X_test)  # test -> pred(test) == y_test???
        if parametros == None:
            print(
                f"-> Modelo NO Optimizado: {classificador}\n Validation Score: {score}\n "
                f"Test score: {r2_score(y_test, y_pred)} \n ")
        else:
            print(
                f"-> Modelo Optimizado: {classificador}\n Validation Score: {score}\n "
                f"Test score: {r2_score(y_test, y_pred)}\n ")


def clasificacion(X_train, X_test, y_train, y_test):
    obj_eva = Modelo()
    for classificador, parametros in obj_eva.modelos_clasificacion().items():
        modelo = Supervisado(classificador, X_train, y_train)
        model, score = modelo.optimizacion(classificador, parametros,
                                           scoring="accuracy")  # train -> train/validation -> score
        y_pred = modelo.predict(X_test)  # test -> pred(test) == y_test???
        if parametros == None:
            print(
                f"-> Modelo NO Optimizado: {classificador}\n Validation Score: {score}\n "
                f"Test score: {accuracy_score(y_test, y_pred)} \n "
                f"Matriz de confusion:\n{confusion_matrix(y_test, y_pred)}")  # ‘r2’ mejor metrica regresion

        else:
            print(
                f"-> Modelo Optimizado: {classificador}\n Validation Score: {score}\
                n "
                f"Test score: {accuracy_score(y_test, y_pred)}\n "
                f"Matriz de confusion:\n{confusion_matrix(y_test, y_pred)}")


def predict(is_regresion=False, is_clasificacion=False):
    X_train, X_test, y_train, y_test = prepare_dataset("18. visitasUsuarios.csv")
    if is_regresion:
        regresion(X_train, X_test, y_train, y_test)
    elif is_clasificacion:
        clasificacion(X_train, X_test, y_train, y_test)


if __name__ == "__main__":
    dataset = pd.read_csv("datos_fotocasa_final.csv")
    X_columns = dataset[['CRIM', 'ZN']].values
    Y_columns = dataset['MEDV'].values
    X_train, X_test, y_train, y_test = prepare_dataset(X_columns, Y_columns)
    regresion(X_train, X_test, y_train, y_test)

    """
    main(clasificacion=true, regresion=true)
    """
    # nombres = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT', 'MEDV']
    # acabar funcion añadir modelos
    # corregir error predict = cuando no recibe modelo optimizado
    # escoger 3 mejores modelos

"""
    #Voting 3 mejores
    voting = Voting(clf[0], clf[1], clf[2])
    Modelo(voting)"""

"""
1) Split datos
    a) Separar columnas (solo los valores): una columna con los datos para predecir, el resto de columnas como base de prediccion
    b) Utilizar funcion train_test_split para recibir de cada columna dos conjuntos de datos, uno para entrenar y otro para testear (en total 4)
2) Modelo fittear
    a) En caso de ser un modelo optimizado, utilizar gridesearch para recibir resultado y despues entrenar
    b) En caso de ser un modelo no optimo, utilizar cross_val_score para recibir resultado y despues entrenar
3) Modelo predecir (transform): con los modelos entrenados, predecir
4) Revisar puntuacion sobre prediccion:
    a) Verificar que no existe mucha diferencia entre el resultado obtenido con el modelo sin entrenar y el modelo entrenado en la prediccion
"""
