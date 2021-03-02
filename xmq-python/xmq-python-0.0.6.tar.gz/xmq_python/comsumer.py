from .adapters.comsumer_amqp import ComsumerAMQP
from .mq_type import *


class Comsumer(object):
    def __init__(self, mq_type='AMQP', **mq_options):
        if mq_type == MQ_TYPE_AMQP:
            self.__agent = ComsumerAMQP(**mq_options)
        else:
            self.__agent = ComsumerAMQP(**mq_options)

    def Register(self, topic_group: str, topic: str, callback, **route):
        self.__agent.Register(topic_group, topic, callback, **route)

    def Start(self):
        self.__agent.Start()

    def Stop(self):
        self.__agent.Stop()
