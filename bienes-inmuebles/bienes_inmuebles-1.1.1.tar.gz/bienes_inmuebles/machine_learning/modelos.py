from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import Lasso
from sklearn.linear_model import ElasticNet
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVR
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeRegressor
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import numpy as np


class Modelo():

    def modelos_clasificacion(self):
        modelos_parametros = {KNeighborsClassifier(): {
            'n_neighbors': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
                            26,
                            27, 28, 29, 30]},
            SVC(): {'kernel': ['rbf'], 'gamma': [1e-3, 1e-4], 'C': [1, 10, 100, 1000]},
            LogisticRegression(): {'C': [0.001, 0.01, 0.1, 1, 10, 100, 1000]},
            LinearDiscriminantAnalysis(): None,
            DecisionTreeClassifier(): None,
            GaussianNB(): None,
            AdaBoostClassifier(): None,
            GradientBoostingClassifier(): None,
            BaggingClassifier(): None,
            RandomForestClassifier(): None,
            ExtraTreesClassifier(): None}
        return modelos_parametros

    def modelos_regresion(self):
        modelos_parametros = {
            LinearRegression(): None,
            Lasso(): {'alpha':[0.02, 0.024, 0.025, 0.026, 0.03]},
            ElasticNet(): {"alpha": [0.0001, 0.001, 0.01, 0.1, 1, 10, 100]},
            KNeighborsRegressor(): {'n_neighbors': np.arange(1, 12, 2),
              'weights': ['uniform', 'distance']},
            DecisionTreeRegressor(): None,
            SVR(): None,
            AdaBoostRegressor(): None,
            GradientBoostingRegressor(): None,
            RandomForestRegressor(): None,
            ExtraTreesRegressor(): None}
        return modelos_parametros
