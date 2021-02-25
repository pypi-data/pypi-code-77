# -*- coding: utf-8 -*-

import logging

from fast_tracker.common.object_names import callable_name

_logger = logging.getLogger(__name__)


class DataSampler(object):

    def __init__(self, consumer, source, name, settings, **properties):
        """

        :param consumer:
        :param source:  是一个可调用对象，采集数据指标的函数
        :param name:  采集的数据名称
        :param settings:
        :param properties:
        """
        self.consumer = consumer  # 消费者

        self.settings = settings
        self.source_properties = source(settings)

        self.factory = self.source_properties['factory']
        self.instance = None

        self.merged_properties = dict(self.source_properties)
        self.merged_properties.update(properties)

        self.name = (name or self.merged_properties.get('name')
                     or callable_name(source))

        self.group = self.merged_properties.get('group')

        if self.group:
            self.group = self.group.rstrip('/')

        self.guid = self.merged_properties.get('guid')

        if self.guid is None and hasattr(source, 'guid'):
            self.guid = source.guid

        self.version = self.merged_properties.get('version')

        if self.version is None and hasattr(source, 'version'):
            self.version = source.version

        environ = {}

        environ['consumer.name'] = consumer
        environ['consumer.vendor'] = 'FAST'
        environ['producer.name'] = self.name
        environ['producer.group'] = self.group  # 生产者
        environ['producer.guid'] = self.guid
        environ['producer.version'] = self.version

        self.environ = environ

        _logger.debug('Initialising data sampler for %r.', self.environ)

    def start(self):
        if self.instance is None:
            self.instance = self.factory(self.environ)

            if self.instance is None:
                _logger.error('Failed to create instance of data source for '
                              '%r, returned None. Custom metrics from this data '
                              'source will not subsequently be available. If this '
                              'problem persists, please report this problem '
                              'to the provider of the data source.', self.environ)

        if hasattr(self.instance, 'start'):
            self.instance.start()

    def stop(self):
        if hasattr(self.instance, 'stop'):
            self.instance.stop()
        else:
            self.instance = None

    def metrics(self):
        if self.instance is None:
            return []

        if self.group:
            return (('%s/%s' % (self.group, key), value)
                    for key, value in self.instance())
        else:
            return self.instance()
