import adafruit_dht
from dbutils_phornee import MariaDBConn
from baseutils_phornee import ManagedClass
from datetime import datetime

class Sensors(ManagedClass):

    def __init__(self):
        super().__init__(execpath=__file__)
        self.homeDB = MariaDBConn()

    @classmethod
    def getClassName(cls):
        return "sensors"

    def sensorRead(self):
        """
        Read sensors information
        """
        try:
            self.homeDB.openConn(self.config['mariadbconn'])
            dhtSensor = adafruit_dht.DHT22(self.config['pin'])

            humidity = dhtSensor.humidity
            temp_c = dhtSensor.temperature

            timestamp = datetime.utcnow()

            if temp_c:
                data = {"sensor_id": self.config['temp_id'], "timestamp": timestamp, "value": temp_c}
                self.homeDB.insert('measurements', data)
                # print(SENSOR_LOCATION_NAME + " Temperature(C) {}".format(temp_c))

            if humidity:
                data = {"sensor_id": self.config['humid_id'], "timestamp": timestamp, "value": humidity}
                self.homeDB.insert('measurements', data)
                # print(SENSOR_LOCATION_NAME + " Humidity(%) {}".format(humidity,".2f"))

        except Exception as e:
            self.logger.error("RuntimeError: {}".format(e))


if __name__ == "__main__":
    sensors_instance = Sensors()
    sensors_instance.sensorRead()





