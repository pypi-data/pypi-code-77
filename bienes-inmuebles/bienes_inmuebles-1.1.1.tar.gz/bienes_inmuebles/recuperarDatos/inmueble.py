from typing import Any


class Inmueble(object):
    def __init__(self, idInmueble, urlInmueble, fuenteInfo, tipoInmueble, tipoOperacion, precio, numHab, tamano, planta, distrito, ciudad, fecha, descripcion,
                 eficienciaEnergetica, ascensor, terraza, trastero, garaje, balcon, aireAcondicionado, piscina, vendedor, banios ):
        self.idInmueble = idInmueble
        self.urlInmueble = urlInmueble
        self.fuenteInfo = fuenteInfo
        self.tipoOperacion = tipoOperacion
        self.tipoInmueble = tipoInmueble
        self.precio = precio
        self.numHab = numHab
        self.tamano = tamano
        self.planta = planta
        self.distrito = distrito
        self.ciudad = ciudad
        self.fecha = fecha
        self.descripcion = descripcion
        self.eficienciaEnergetica = eficienciaEnergetica
        self.ascensor = ascensor
        self.terraza = terraza
        self.trastero = trastero
        self.garaje = garaje
        self.balcon = balcon
        self.aireAcondicionado = aireAcondicionado
        self.piscina = piscina
        self.vendedor = vendedor
        self.banios = banios

    # self.precio = precio
    # self.set_precio(precio)
    def getIdInmueble(self):
        return self.idInmueble

    def setIdInmueble(self, nuevoId):
        self.idInmueble = nuevoId

    def getUrlInmueble(self):
        return self.urlInmueble

    def setUrlInmueble(self, nuevoUrlInmueble):
        self.urlInmueble = nuevoUrlInmueble

    def getFuenteInfo(self):
        return self.fuenteInfo

    def setFuenteInfo(self, nuevoFuenteInfo):
        self.fuenteInfo = nuevoFuenteInfo

    def getTipoOperacion(self):
        return self.tipoOperacion

    def setTipoOperacion(self, nuevoTipoOperacion):
        self.tipoOperacion = nuevoTipoOperacion

    def getTipoInmueble(self):
        return self.tipoInmueble

    def setTipoInmueble(self, nuevoTipoInmueble):
        self.tipoInmueble = nuevoTipoInmueble

    def getPrecio(self):
        return self.precio

    def setPrecio(self, nuevoPrecio):
        self.precio = nuevoPrecio

    def getNumHab(self):
        return self.numHab

    def setNumHab(self, nuevoNumHab):
        self.numHab = nuevoNumHab

    def getTamano(self):
        return self.tamano

    def setTamano(self, nuevoTamano):
        self.tamano = nuevoTamano

    def getPlanta(self):
        return self.planta

    def setPlanta(self, nuevoPlanta):
        self.planta = nuevoPlanta

    def getDistrito(self):
        return self.distrito

    def setDistrito(self, nuevoDistrito):
        self.distrito = nuevoDistrito

    def getCiudad(self):
        return self.ciudad

    def setCiudad(self, nuevoCiudad):
        self.ciudad = nuevoCiudad

    def getFecha(self):
        return self.fecha

    def setFecha(self, nuevoFecha):
        self.fecha = nuevoFecha

    def getDescripcion(self):
        return self.descripcion

    def setDescripcion(self, nuevoDescripcion):
        self.descripcion = nuevoDescripcion

    def getEficienciaEnergetica(self):
        return self.eficienciaEnergetica

    def setEficienciaEnergetica(self, eficienciaEnergetica):
        self.eficienciaEnergetica = eficienciaEnergetica

    def getAscensor(self):
        return self.ascensor

    def setAscensor(self, nuevoAscensor):
        self.ascensor = nuevoAscensor

    def getTerraza(self):
        return self.terraza

    def setTerraza(self, terraza):
        self.terraza = terraza

    def getTrastero(self):
        return self.trastero

    def setTrastero(self, trastero):
        self.trastero = trastero

    def getGaraje(self):
        return self.garaje

    def setGaraje(self, garaje):
        self.garaje = garaje

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

    def getVendedor(self):
        return self.vendedor

    def setVendedor(self, vendedor):
        self.vendedor = vendedor

    def getBanios(self):
        return self.banios

    def setBanios(self, banios):
        self.banios = banios