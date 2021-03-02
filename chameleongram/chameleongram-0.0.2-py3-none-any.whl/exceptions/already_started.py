class ClientAlreadyStarted(Exception):
    def __str__(self):
        return f"Client has already been started."
