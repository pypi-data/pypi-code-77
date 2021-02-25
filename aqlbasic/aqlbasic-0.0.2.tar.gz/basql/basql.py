
import mysql.connector
connection=""
class basql:
    def __init__(host="localhost",database="test", user="root", password=""):
        try:
            connection = mysql.connector.connect(host=host, database=database, user=user, password=password)
        except mysql.connector.Error as error:
            print("Failed to Connect... {}".format(error))