# -------------------------------------------------------------------------------
# Copyright 2006-2020 UT-Battelle, LLC. See LICENSE for more information.
# -------------------------------------------------------------------------------


class Message:
    """
    Base class for all IPS messages. **Should not be used in actual
    communication.**
    """
    SUCCESS = 0
    FAILURE = 1
    delimiter = ''
    identifier = 'MESSAGE'
    counter = 0

    def __init__(self, sender_id, receiver_id):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.message_id = None

    def get_message_id(self):
        if self.message_id is None:
            delim = self.delimiter
            self.message_id = delim.join([self.identifier,
                                          str(self.sender_id),
                                          str(self.receiver_id),
                                          str(self.counter)])
            self.__class__.counter += 1
        return self.message_id


class ServiceRequestMessage(Message):
    r"""
    Message used by components to request the result of a service action by
    one of the IPS managers.

      * *sender_id*: component id of the sender
      * *receiver_id*: component id of the receiver (framework)
      * *target_comp_id*: component id of target component (typically framework)
      * *target_method*: name of method to be invoked on component *target_comp_id*
      * *\*args*: any number of arguments.  These are specific to the target method.
    """
    counter = 0
    delimiter = '|'
    identifier = 'REQUEST'

    def __init__(self, sender_id, receiver_id, target_comp_id, target_method, *args, **keywords):
        Message.__init__(self, sender_id, receiver_id)
        self.target_comp_id = target_comp_id
        self.target_method = target_method
        self.args = args
        self.keywords = keywords
        self.message_id = self.get_message_id()


class ServiceResponseMessage(Message):
    r"""
    Message used by managers to respond with the result of the service action
    to the calling component.

      * *sender_id*: component id of the sender (framework)
      * *receiver_id*: component id of the receiver (calling component)
      * *request_msg_id*: id of request message this is a response to.
      * *status*: either Message.SUCCESS or Message.FAILURE
      * *\*args*: any number of arguments.  These are specific to type of response.
    """
    counter = 0
    delimiter = '|'
    identifier = 'RESPONSE'

    def __init__(self, sender_id, receiver_id, request_msg_id, status, *args):
        Message.__init__(self, sender_id, receiver_id)
        self.request_msg_id = request_msg_id
        self.status = status
        self.args = args
        self.message_id = self.get_message_id()


class MethodInvokeMessage(Message):
    r"""
    Message used by components to invoke methods on other components.

      * *sender_id*: component id of the sender
      * *receiver_id*: component id of the receiver
      * *call_id*: identifier of the call (generated by caller)
      * *target_method*: method to be invoked on the receiver
      * *\*args*: arguments to be passed to the *target_method*
    """
    counter = 0
    delimiter = '|'
    identifier = 'INVOKE'

    def __init__(self, sender_id, receiver_id, call_id, target_method, *args, **keywords):
        Message.__init__(self, sender_id, receiver_id)
        self.call_id = call_id
        self.target_method = target_method
        self.args = args
        self.keywords = keywords
        self.message_id = self.get_message_id()


class MethodResultMessage(Message):
    r"""
    Message used to relay the return value after a method invocation.

      * *sender_id*: component id of the sender (callee)
      * *receiver_id*: component id of the receiver (caller)
      * *call_id*: identifier of the call (generated by caller)
      * *status*: either Message.SUCCESS or Message.FAILURE indicating the success of failure of the invocation.
      * *\*args*: other information to be passed back to the caller.
    """
    counter = 0
    delimiter = '|'
    identifier = 'RESULT'

    def __init__(self, sender_id, receiver_id, call_id, status, *args):
        Message.__init__(self, sender_id, receiver_id)
        self.call_id = call_id
        self.args = args
        self.status = status
        self.message_id = self.get_message_id()


class ExitMessage(Message):
    r"""
    Message used to communicate the exit status of a component.

    * *sender_id*: component id that is telling the component to die (framework)
    * *receiver_id*: component id that is to die
    * *status*: either Messages.SUCCESS or Messages.FAILURE indicating if the exit request is due to the simulation finishing successfully or in error.
    * *\*args*: other information passed to the component to die.
    """
    counter = 0
    delimiter = '|'
    identifier = 'EXIT'

    def __init__(self, sender_id, receiver_id, status, *args):
        Message.__init__(self, sender_id, receiver_id)
        self.status = status
        self.args = args
        self.message_id = self.get_message_id()
