import numpy as np
from joblib import load
import os
from bienes_inmuebles.preprocesar.csv_preprocesamiento import PATH4

# PREDICCION DE EDIFICIO INVENTADO COMPRA
modelo = load(os.path.join(PATH4, "data/model_compra.joblib"))
fichero_path = os.path.join(PATH4, "data/scaler_compra.pkl")
scaler = load(open(fichero_path, 'rb'))
predecir = np.array(
    [1, 1, 1, 87, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,
     1, 0])  # Compra inventado
escalado = scaler.transform(predecir.reshape(1, -1))
resultado_final = modelo.predict(escalado)[0]  # Get out of the array
print("Resultado inventado compra: ",round(resultado_final, 2))

# PREDICCION DE EDIFICIO INVENTADO ALQUILER
modelo = load(os.path.join(PATH4, "data/model_alquiler.joblib"))
fichero_path = os.path.join(PATH4, "data/scaler_alquiler.pkl")
scaler = load(open(fichero_path, 'rb'))
predecir = np.array(
    [1, 2, 1, 32, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,
     0, 1])  # Alquiler inventado
escalado = scaler.transform(predecir.reshape(1, -1))
resultado_final = modelo.predict(escalado)[0]  # Get out of the array
print("Resultado inventado alquiler: ",round(resultado_final, 2))

# PRDICCION DE EDIFICIO COMPRA DEL TRAIN
modelo = load(os.path.join(PATH4, "data/model_compra.joblib"))
fichero_path = os.path.join(PATH4, "data/scaler_compra.pkl")
scaler = load(open(fichero_path, 'rb'))
predecir_comprobacion = np.array([0, 0, -1.27043022, -0.03037415, -0.80451695, 0.73192505,
                                  -0.74086779, -0.61304591, -0.3902251, -0.97053361, - 0.41926275, - 0.78156767,
                                  - 0.26599058, 0.59710535, -0.49491904, 7.29246186, -0.31603512, -0.14791395,
                                  -0.15177699, -0.15430335, -0.75828754, -0.14791395, -0.14261481, -0.1371279,
                                  -0.14921177, -0.14528654, -0.26118512, -0.14791395, -0.14261481, -0.21622731,
                                  -0.14261481, -0.14921177, -0.36208628, -0.10219523, -0.14126153, -0.13851844,
                                  0, -0.11440719, -0.14660564, 0.18749602]).reshape(1, -1) # set de datos del main para compra
resultado_final = modelo.predict(predecir_comprobacion)[0]  # Get out of the array
print("Resultado real dataset compra: ",round(resultado_final, 2), "Esperado: 219000")

# PREDICCION DE EDIFICIO ALQUILER TRAIN
modelo = load(os.path.join(PATH4, "data/model_alquiler.joblib"))
fichero_path = os.path.join(PATH4, "data/scaler_alquiler.pkl")
scaler = load(open(fichero_path, 'rb'))
predecir_comprobacion = np.array([0, 0, -0.8277271, -0.84307123, -0.80314054, 0.64890474,
                                  -0.55142241, -0.4196755, -0.40816956, -1.30110658, -0.42510962, -0.5578013,
                                  -0.28142647, 0.54053939, -0.42456744, 4.32761607, -0.12697879, -0.19395153,
                                  -0.56721272, -0.30600167, -0.37503142, -0.0822633, -0.206456, -0.22761385,
                                  -0.17809818, -0.23813239, -0.09371062, -0.15088305, -0.24198333, -0.09838482,
                                  -0.20147376, -0.30986205, -0.12787187, -0.08020159, -0.11076976, -0.08089451,
                                  0, -0.21973763, - 0.18297918, 0.2917823]).reshape(1, -1) # set de datos del main para alquiler
resultado_final = modelo.predict(predecir_comprobacion)[0]  # Get out of the array
print("Resultado real dataset alquiler: ",round(resultado_final, 2),"Esperado: 600")
