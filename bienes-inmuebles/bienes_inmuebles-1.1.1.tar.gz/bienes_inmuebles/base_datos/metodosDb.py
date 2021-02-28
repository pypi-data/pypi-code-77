import pymysql


class MetodosDb():
    @staticmethod
    def intancias_bbdd(bbdd_server = "localhost", bbdd_user= "root",bbdd_pass="1234", bbdd_name="db_proyecto_miriadax"):
        return bbdd_server , bbdd_user, bbdd_pass, bbdd_name

    def addDbFotocasa(self, inmueble):

        bbdd_server, bbdd_user, bbdd_pass, bbdd_name = MetodosDb.intancias_bbdd()

        # Establecemos conexion con la BBDD
        db = pymysql.connect(bbdd_server, bbdd_user, bbdd_pass, bbdd_name)

        # Prepando el objeto de manipulacion de BBDD
        cursor = db.cursor()
        # Añadimos elemento a la BBDD
        #sql = "INSERT INTO pisos VALUES (" + str(inmueble.getIdInmueble()) + ", " + "'" + inmueble.getFuenteInfo() + "'" + ", " + str(inmueble.getTipoInmueble()) + ", " + str(inmueble.getTipoOperacion()) + ", " + str(inmueble.getPrecio()) + ", " + str(inmueble.getNumHab()) + ", " + str(inmueble.getTamano()) + ", '" + str(inmueble.getPlanta()) + "', '" + inmueble.getDistrito() + "', '" + inmueble.getCiudad() + "', " + inmueble.getFecha() + "', '" + str(inmueble.getBanio()) + "', " + str(inmueble.getAscensor()) + ")"
        sql = "INSERT INTO pisos (idInmueble, urlInmueble, fuenteInfo, tipoInmueble, tipoOperacion, precio, habitaciones, tamano, planta, distrito, ciudad, fecha, descripcion, eficienciaEnergetica, ascensor, terraza, trastero, garaje, balcon, aireAcondicionado, piscina, vendedor, banios ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        print(sql)

        try:
            # Ejecutamos comando SQL
            #cursor.execute(sql)

            if (inmueble.getPlanta()=='Superior a Planta 15'):
                inmueble.setPlanta('16')

            print(str(inmueble.getIdInmueble()) + ", " + str(inmueble.getUrlInmueble()) + ", " + str(inmueble.getFuenteInfo()) + ", " + str(inmueble.getTipoInmueble()) +
                  ", " + str(inmueble.getTipoOperacion()) + ", " + str(inmueble.getPrecio()) + ", " + str(inmueble.getNumHab()) + ", " + str(inmueble.getTamano()) +
                  ", " + str(inmueble.getPlanta()) + ", " + str(inmueble.getDistrito()) + ", " + str(inmueble.getCiudad()) +
                  ", " + str(inmueble.getFecha()) + ", " + str(inmueble.getEficienciaEnergetica()) + ", " + str(inmueble.getAscensor()) +
                  ", " + str(inmueble.getTerraza()) + ", " + str(inmueble.getTrastero()) + ", " + str(inmueble.getGaraje()) + ", " + str(inmueble.getBalcon()) +
                  ", " + str(inmueble.getAireAcondicionado()) + ", " + str(inmueble.getPiscina()) + ", " + str(inmueble.getVendedor()) + ", " + str(inmueble.getBanios()))
            print(str(inmueble.getDescripcion()))
            cursor.execute(sql, (inmueble.getIdInmueble(),
                                 inmueble.getUrlInmueble(),
                                 inmueble.getFuenteInfo(),
                                 inmueble.getTipoInmueble(),
                                 inmueble.getTipoOperacion(),
                                 inmueble.getPrecio(),
                                 inmueble.getNumHab(),
                                 inmueble.getTamano(),
                                 inmueble.getPlanta(),
                                 inmueble.getDistrito(),
                                 inmueble.getCiudad(),
                                 inmueble.getFecha(),
                                 inmueble.getDescripcion(),
                                 inmueble.getEficienciaEnergetica(),
                                 inmueble.getAscensor(),
                                 inmueble.getTerraza(),
                                 inmueble.getTrastero(),
                                 inmueble.getGaraje(),
                                 inmueble.getBalcon(),
                                 inmueble.getAireAcondicionado(),
                                 inmueble.getPiscina(),
                                 inmueble.getVendedor(),
                                 inmueble.getBanios()))
            # COMMIT - Aplicar de forma persistente en la BBDD
            db.commit()
            print("Objeto Añadido")
        except Exception as e:
            # Rollback en caso de error
            print("Error al añadir en BBDD: " + e)
            db.rollback()


        # Desconexion del servidor
        db.close()