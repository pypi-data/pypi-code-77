from netmanager import NetRequest


class FirebaseRTDB:
    """ -- USAGE EXAMPLE ----------------------
        >>> from netmanager import FirebaseRTDB
        >>> url = "https://my-default-rtdb"
        >>> db = FirebaseRTDB(url)
        >>> db.get("users")
        <class 'str'>

        >>> db.set("users/user1/key", "value")
        <class 'int'>
        ---------------------------------------
    """

    def __init__(self, database_url):
        self.url = database_url + "/"

    def get(self, path = "/"):
        response = NetRequest(self.url + path + "/.json")
        return response.result

    def set(self, path = "/", data = "null"):
        response = NetRequest(self.url + path + ".json", "PUT", str(data))
        return response.status
