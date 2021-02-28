from colorama import Back, Style
from bienes_inmuebles.formulario.objetoPrediccion import ObjetoPrediccion


class MetodosFormulario():

    def __init__(self):
        self.listaDistritos = ["arganzuela", "barajas", "carabanchel", "centro", "chamartin", "chamberi",
                               "ciudad_lineal",
                               "fuencarral", "hortaleza", "latina", "moncloa", "moratalaz", "puente_de_vallecas",
                               "retiro",
                               "salamanca", "san_blas", "tetuan", "usera", "vicalvaro", "villa_de_vallecas",
                               "villaverde",
                               "vicalvaro"]
        self.listaEficiencias = ["eficienciaEnergetica_A", "eficienciaEnergetica_B", "eficienciaEnergetica_C"]
        self.listaOperaciones = ["Comprar", "Alquiler"]
        self.listaOpcionesGarage = ["garaje_Comunitario", "garaje_Privado"]
        self.maxHabitaciones = 30
        self.maxPlantas = 16
        self.maxMetros = 999999
        self.maxBaños = 20

    def getSIoNO(self, objetoPreguntado):
        dato = input("¿La vivienda tiene " + objetoPreguntado + "? (s)si - (n)no \n> ").lower()
        while dato != 's' and dato != 'n':
            print(Style.RESET_ALL)
            print(Back.BLUE + "El dato introducido no es valido. Intentelo otra vez")
            print(Style.RESET_ALL)
            dato = input("La vivienda tiene " + objetoPreguntado + "? (s)si - (n)no\n> ").lower()

        return dato

    def getNumero(self, consulta, numeroMaximo):
        dato = input(consulta + "\n> ")
        if dato.isnumeric():
            dato = int(dato)
        else:
            dato = -1

        while dato < 0 or dato > numeroMaximo:
            print(Style.RESET_ALL)
            print(Back.YELLOW + "El dato introducido no es valido. Intentelo otra vez")
            print(Style.RESET_ALL)

            dato = input(consulta + "\n> ").lower()
            if dato.isnumeric():
                dato = int(dato)
            else:
                dato = -1
        return dato

    def getOpcion(self, listaElementos, consulta):
        x = 1
        for elemento in listaElementos:
            print("(" + str(x) + ")" + elemento)
            x += 1

        opcion = input(consulta + "\n> ")
        if opcion.isnumeric():
            opcion = int(opcion)
        else:
            opcion = -1

        while opcion < 0 or opcion > len(listaElementos):
            print(Style.RESET_ALL)
            print(Back.YELLOW + "El dato introducido no es valido. Intentelo otra vez")
            print(Style.RESET_ALL)

            opcion = input(consulta + "\n> ")

            if opcion.isnumeric():
                opcion = int(opcion)
            else:
                opcion = -1

        return listaElementos[opcion - 1]

    def formulario(self):

        objetoPred = ObjetoPrediccion("Madrid")

        tipoOperacion = self.getOpcion(self.listaOperaciones, "¿Que TIPO de OPERACION tiene pensado realizar?")
        if tipoOperacion == 'Comprar':
            objetoPred.setTipoOperacion(1)
        elif tipoOperacion == 'Alquiler':
            objetoPred.setTipoOperacion(2)

        distrito = self.getOpcion(self.listaDistritos, "¿En qué DISTRITO se encuentra la vivienda?")
        setattr(objetoPred, "distrito_" + distrito, 1)

        habitaciones = self.getNumero("¿Cuantos HABITACIONES tiene la vivienda?,", self.maxHabitaciones)
        objetoPred.setHabitaciones(habitaciones)

        planta = self.getNumero("¿En qué PLANTA esta la vivienda?", self.maxPlantas)
        objetoPred.setPlanta(planta)

        tamanio = self.getNumero("¿Cuantos METROS CUADRADOS tiene la vivienda?", self.maxMetros)
        objetoPred.setTamano(tamanio)

        banios = self.getNumero("¿Cuantos BAÑOS tiene la vivienda?", self.maxBaños)
        objetoPred.setBanos(banios)

        terraza = self.getSIoNO("TERRAZA")
        if terraza.lower() == 's':
            objetoPred.setTerraza(1)
        elif terraza.lower() == 'n':
            objetoPred.setTerraza(0)

        trastero = self.getSIoNO("TRASTERO")
        if trastero.lower() == 's':
            objetoPred.setTrastero(1)
        elif trastero.lower() == 'n':
            objetoPred.setTrastero(0)

        garaje = self.getSIoNO("GARAJE")
        if garaje == 's':
            garaje = self.getOpcion(self.listaOpcionesGarage, "¿Qué TIPO de GARAJE tiene?")

        if garaje.lower() == "n":
            objetoPred.setGaraje_No_detallado(1)
        elif garaje == 'garaje_Comunitario':
            objetoPred.setGaraje_Comunitario(1)
        elif garaje == 'garaje_Privado':
            objetoPred.setGaraje_Privado(1)

        balcon = self.getSIoNO("BALCON")
        if balcon.lower() == 's':
            objetoPred.setBalcon(1)
        elif balcon.lower() == 'n':
            objetoPred.setBalcon(0)

        aireAcondicionado = self.getSIoNO("AIRE ACONDICIONADO")
        if aireAcondicionado.lower() == 's':
            objetoPred.setAireAcondicionado(1)
        elif aireAcondicionado.lower() == 'n':
            objetoPred.setAireAcondicionado(0)

        piscina = self.getSIoNO("PISCINA")
        if piscina.lower() == 's':
            objetoPred.setPiscina(1)
        elif piscina.lower() == 'n':
            objetoPred.setPiscina(0)

        ascensor = self.getSIoNO("ASCENSOR")
        if ascensor.lower() == 's':
            objetoPred.setAscensor(1)
        elif ascensor.lower() == 'n':
            objetoPred.setAscensor(0)

        eficiencia = self.getOpcion(self.listaEficiencias, "¿Qué EFICIENCIA energetica tiene la vivienda")
        if eficiencia == 'eficienciaEnergetica_A':
            objetoPred.setEficienciaEnergetica_A(1)
        elif eficiencia == 'eficienciaEnergetica_B':
            objetoPred.setEficienciaEnergetica_B(1)
        elif eficiencia == 'eficienciaEnergetica_C':
            objetoPred.setEficienciaEnergetica_C(1)

        objetoPred.setCiudad(1)
        objetoPred.setTipoInmueble(1)

        return objetoPred


if __name__ == "__main__":
    form = MetodosFormulario()

    objetoPred = form.formulario()

    print(type(objetoPred))

    """print(objetoPred.getTipoOperacion())
    print(objetoPred.getHabitaciones())
    print(objetoPred.getTamano())
    print(objetoPred.getPlanta())
    print(objetoPred.getAscensor())
    print(objetoPred.getTerraza())
    print(objetoPred.getTrastero())
    print(objetoPred.getBalcon())
    print(objetoPred.getAireAcondicionado())
    print(objetoPred.getPiscina())
    print(objetoPred.getGaraje_Comunitario())
    print(objetoPred.getGaraje_No_detallado())
    print(objetoPred.getGaraje_Privado())
    print(objetoPred.getEficienciaEnergetica_A())
    print(objetoPred.getEficienciaEnergetica_B())
    print(objetoPred.getEficienciaEnergetica_C())
    print(objetoPred.getDistrito_arganzuela())
    print(objetoPred.getDistrito_barajas())
    print(objetoPred.getDistrito_carabanchel())
    print(objetoPred.getDistrito_centro())
    print(objetoPred.getDistrito_chamartin())
    print(objetoPred.getDistrito_chamberi())
    print(objetoPred.getDistrito_ciudad_lineal())
    print(objetoPred.getDistrito_fuencarral())
    print(objetoPred.getDistrito_moncloa())
    print(objetoPred.getDistrito_hortaleza())
    print(objetoPred.getDistrito_latina())
    print(objetoPred.getDistrito_moratalaz())
    print(objetoPred.getDistrito_retiro())
    print(objetoPred.getDistrito_puente_de_vallecas())
    print(objetoPred.getDistrito_salamanca())
    print(objetoPred.getDistrito_san_blas())
    print(objetoPred.getDistrito_vicalvaro())
    print(objetoPred.getDistrito_villaverde())
    print(objetoPred.getDistrito_usera())
    print(objetoPred.getDistrito_tetuan())"""
