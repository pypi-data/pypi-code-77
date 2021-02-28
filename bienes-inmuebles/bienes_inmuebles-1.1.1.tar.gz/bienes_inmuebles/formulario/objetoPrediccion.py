class ObjetoPrediccion(object):
    def __init__(self, tipoInmueble=0, tipoOperacion=0, habitaciones=0, tamano=0, planta=0, ascensor=0, terraza=0,
                 trastero=0, balcon=0, aireAcondicionado=0, piscina=0, banos=0, garaje_Comunitario=0,
                 garaje_No_detallado=0, garaje_Privado=0, distrito_arganzuela=0, distrito_barajas=0,
                 distrito_carabanchel=0, distrito_centro=0, distrito_chamartin=0, distrito_chamberi=0,
                 distrito_ciudad_lineal=0, distrito_fuencarral=0, distrito_hortaleza=0, distrito_latina=0,
                 distrito_moncloa=0, distrito_moratalaz=0, distrito_puente_de_vallecas=0, distrito_retiro=0,
                 distrito_salamanca=0, distrito_san_blas=0, distrito_tetuan=0, distrito_usera=0, distrito_vicalvaro=0,
                 distrito_villa_de_vallecas=0, distrito_villaverde=0, ciudad="", eficienciaEnergetica_A=0,
                 eficienciaEnergetica_B=0, eficienciaEnergetica_C=0):
        self.tipoInmueble = tipoInmueble
        self.tipoOperacion = tipoOperacion
        self.habitaciones = habitaciones
        self.tamano = tamano
        self.planta = planta
        self.ascensor = ascensor
        self.terraza = terraza
        self.trastero = trastero
        self.balcon = balcon
        self.aireAcondicionado = aireAcondicionado
        self.piscina = piscina
        self.banos = banos
        self.garaje_Comunitario = garaje_Comunitario
        self.garaje_No_detallado = garaje_No_detallado
        self.garaje_Privado = garaje_Privado
        self.distrito_arganzuela = distrito_arganzuela
        self.distrito_barajas = distrito_barajas
        self.distrito_carabanchel = distrito_carabanchel
        self.distrito_centro = distrito_centro
        self.distrito_chamartin = distrito_chamartin
        self.distrito_chamberi = distrito_chamberi
        self.distrito_ciudad_lineal = distrito_ciudad_lineal
        self.distrito_fuencarral = distrito_fuencarral
        self.distrito_hortaleza = distrito_hortaleza
        self.distrito_latina = distrito_latina
        self.distrito_moncloa = distrito_moncloa
        self.distrito_moratalaz = distrito_moratalaz
        self.distrito_puente_de_vallecas = distrito_puente_de_vallecas
        self.distrito_retiro = distrito_retiro
        self.distrito_salamanca = distrito_salamanca
        self.distrito_san_blas = distrito_san_blas
        self.distrito_tetuan = distrito_tetuan
        self.distrito_usera = distrito_usera
        self.distrito_vicalvaro = distrito_vicalvaro
        self.distrito_villa_de_vallecas = distrito_villa_de_vallecas
        self.distrito_villaverde = distrito_villaverde
        self.ciudad = ciudad
        self.eficienciaEnergetica_A = eficienciaEnergetica_A
        self.eficienciaEnergetica_B = eficienciaEnergetica_B
        self.eficienciaEnergetica_C = eficienciaEnergetica_C

    def getTipoInmueble(self):
        return self.tipoInmueble

    def setTipoInmueble(self, tipoInmueble):
        self.tipoInmueble = tipoInmueble

    def getTipoOperacion(self):
        return self.tipoOperacion

    def setTipoOperacion(self, tipoOperacion):
        self.tipoOperacion = tipoOperacion

    def getHabitaciones(self):
        return self.habitaciones

    def setHabitaciones(self, habitaciones):
        self.habitaciones = habitaciones

    def getTamano(self):
        return self.tamano

    def setTamano(self, tamano):
        self.tamano = tamano

    def getPlanta(self):
        return self.planta

    def setPlanta(self, planta):
        self.planta = planta

    def getAscensor(self):
        return self.ascensor

    def setAscensor(self, ascensor):
        self.ascensor = ascensor

    def getTerraza(self):
        return self.terraza

    def setTerraza(self, terraza):
        self.terraza = terraza

    def getTrastero(self):
        return self.trastero

    def setTrastero(self, trastero):
        self.trastero = trastero

    def getBalcon(self):
        return self.balcon

    def setBalcon(self, balcon):
        self.balcon = balcon

    def getAireAcondicionado(self):
        return self.aireAcondicionado

    def setAireAcondicionado(self, aireAcondicionado):
        self.aireAcondicionado = aireAcondicionado

    def getPiscina(self):
        return self.piscina

    def setPiscina(self, piscina):
        self.piscina = piscina

    def getBanos(self):
        return self.banos

    def setBanos(self, banos):
        self.banos = banos

    def getGaraje_Comunitario(self):
        return self.garaje_Comunitario

    def setGaraje_Comunitario(self, garaje_Comunitario):
        self.garaje_Comunitario = garaje_Comunitario

    def getGaraje_No_detallado(self):
        return self.garaje_No_detallado

    def setGaraje_No_detallado(self, garaje_No_detallado):
        self.garaje_No_detallado = garaje_No_detallado

    def getGaraje_Privado(self):
        return self.garaje_Privado

    def setGaraje_Privado(self, garaje_Privado):
        self.garaje_Privado = garaje_Privado

    def getDistrito_arganzuela(self):
        return self.distrito_arganzuela

    def setDistrito_arganzuela(self, distrito_arganzuela):
        self.distrito_arganzuela = distrito_arganzuela

    def getDistrito_barajas(self):
        return self.distrito_barajas

    def setDistrito_barajas(self, distrito_barajas):
        self.distrito_barajas = distrito_barajas

    def getDistrito_carabanchel(self):
        return self.distrito_carabanchel

    def setDistrito_carabanchel(self, distrito_carabanchel):
        self.distrito_carabanchel = distrito_carabanchel

    def getDistrito_centro(self):
        return self.distrito_centro

    def setDistrito_centro(self, distrito_centro):
        self.distrito_centro = distrito_centro

    def getDistrito_chamartin(self):
        return self.distrito_chamartin

    def setDistrito_chamartin(self, distrito_chamartin):
        self.distrito_chamartin = distrito_chamartin

    def getDistrito_chamberi(self):
        return self.distrito_chamberi

    def setDistrito_chamberi(self, distrito_chamberi):
        self.distrito_chamberi = distrito_chamberi

    def getDistrito_ciudad_lineal(self):
        return self.distrito_ciudad_lineal

    def setDistrito_ciudad_lineal(self, distrito_ciudad_lineal):
        self.distrito_ciudad_lineal = distrito_ciudad_lineal

    def getDistrito_fuencarral(self):
        return self.distrito_fuencarral

    def setDistrito_fuencarral(self, distrito_fuencarral):
        self.distrito_fuencarral = distrito_fuencarral

    def getDistrito_hortaleza(self):
        return self.distrito_hortaleza

    def setDistrito_hortaleza(self, distrito_hortaleza):
        self.distrito_hortaleza = distrito_hortaleza

    def getDistrito_latina(self):
        return self.distrito_latina

    def setDistrito_latina(self, distrito_latina):
        self.distrito_latina = distrito_latina

    def getDistrito_moncloa(self):
        return self.distrito_moncloa

    def setDistrito_moncloa(self, distrito_moncloa):
        self.distrito_moncloa = distrito_moncloa

    def getDistrito_moratalaz(self):
        return self.distrito_moratalaz

    def setdistrito_moratalaz(self, distrito_moratalaz):
        self.distrito_moratalaz = distrito_moratalaz

    def getDistrito_puente_de_vallecas(self):
        return self.distrito_puente_de_vallecas

    def setDistrito_puente_de_vallecas(self, distrito_puente_de_vallecas):
        self.distrito_puente_de_vallecas = distrito_puente_de_vallecas

    def getDistrito_retiro(self):
        return self.distrito_retiro

    def setDistrito_retiro(self, distrito_retiro):
        self.distrito_retiro = distrito_retiro

    def getDistrito_salamanca(self):
        return self.distrito_salamanca

    def setDistrito_salamanca(self, distrito_salamanca):
        self.distrito_salamanca = distrito_salamanca

    def getDistrito_san_blas(self):
        return self.distrito_san_blas

    def setDistrito_san_blas(self, distrito_san_blas):
        self.distrito_san_blas = distrito_san_blas

    def getDistrito_tetuan(self):
        return self.distrito_tetuan

    def setDistrito_tetuan(self, distrito_tetuan):
        self.distrito_tetuan = distrito_tetuan

    def getDistrito_usera(self):
        return self.distrito_usera

    def setDistrito_usera(self, distrito_usera):
        self.distrito_usera = distrito_usera

    def getDistrito_vicalvaro(self):
        return self.distrito_vicalvaro

    def setDistrito_vicalvaro(self, distrito_vicalvaro):
        self.distrito_vicalvaro = distrito_vicalvaro

    def getDistrito_villa_de_vallecas(self):
        return self.distrito_villa_de_vallecas

    def setDistrito_villa_de_vallecas(self, distrito_villa_de_vallecas):
        self.distrito_moncloa = distrito_villa_de_vallecas

    def getDistrito_villaverde(self):
        return self.distrito_villaverde

    def setDistrito_villaverde(self, distrito_villaverde):
        self.distrito_villaverde = distrito_villaverde

    def getCiudad(self):
        return self.ciudad

    def setCiudad(self, ciudad):
        self.ciudad = ciudad

    def getEficienciaEnergetica_A(self):
        return self.eficienciaEnergetica_A

    def setEficienciaEnergetica_A(self, eficienciaEnergetica_A):
        self.eficienciaEnergetica_A = eficienciaEnergetica_A

    def getEficienciaEnergetica_B(self):
        return self.eficienciaEnergetica_B

    def setEficienciaEnergetica_B(self, eficienciaEnergetica_B):
        self.eficienciaEnergetica_B = eficienciaEnergetica_B

    def getEficienciaEnergetica_C(self):
        return self.eficienciaEnergetica_C

    def setEficienciaEnergetica_C(self, eficienciaEnergetica_C):
        self.eficienciaEnergetica_C = eficienciaEnergetica_C
