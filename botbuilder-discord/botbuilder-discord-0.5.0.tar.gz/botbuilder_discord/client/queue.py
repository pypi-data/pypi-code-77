
from typing import List, Callable


class ResponseQueue:
    """
    Global object to store the responses given by the listener, and to send
    them to the Client and Message objects.
    """

    def __init__(self):
        self._observers: List[Callable] = []
        self._entries = {}

    def append(self, key: str, content: dict):
        """
        Called by the listener. Add a response to the _entries
        dictionary. Trigger the observers.

        :param key: The key of the new entry in the dictionary. This key is
            an unique message id.
        :param content: The content stored with this new key, in the
            dictionary. This content is another dict containing the response
            message.
        """

        # Append to the dictionary
        self._entries[key] = content

        # Trigger all the observers' functions.
        for callback in self._observers:
            callback(self._entries)

    def bind_to(self, callback: Callable):
        """
        Add a callback function to the observer list.

        :param callback: A function triggered when a new message is appended
            to the _entries dictionary.
        """
        self._observers.append(callback)

    def unbind(self, callback: Callable):
        """
        Unbind (remove) a given callback function from the observers list.
        """
        self._observers.remove(callback)


# Instantiate a global response queue
response_queue = ResponseQueue()
