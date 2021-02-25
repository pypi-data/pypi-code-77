class Base:
    def __init__(self, data):
        for key, dat in data.items():
            self.__dict__.update({key.strip('_'):dat})