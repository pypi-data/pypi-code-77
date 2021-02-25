import datetime
import logging
import os
import six
from pymongo import errors
from scrapy.exporters import BaseItemExporter
from crawlab.db.mongo import get_col
from crawlab.utils.config import get_task_id
# from crawlab.utils import save_item_mongo

def not_set(string):
    """Check if a string is None or ''.
    :returns: bool - True if the string is empty
    """
    if string is None:
        return True
    elif string == '':
        return True
    return False

class CrawlabMongoPipeline(BaseItemExporter):
    # item buffer
    current_item = 0
    item_buffer = []
    duplicate_key_count = 0
    config = {
            'buffer': None,
            'append_timestamp':False,
            # 'uri': 'mongodb://localhost:27017',
            # 'fsync': False,
            # 'write_concern': 0,
            'database':  os.environ.get('CRAWLAB_MONGO_DB') or 'test',
            'separate_collections': False,
            'replica_set': None,
            'unique_key': None,
            'stop_on_duplicate': 0,
        }
    def __init__(self, **kwargs):
        """Constructor."""
        super(CrawlabMongoPipeline, self).__init__(**kwargs)

        self.logger = logging.getLogger('scrapy-mongodb-pipeline')

    def configure(self):
        options = [
            # ('uri', 'MONGODB_URI'),
            # ('fsync', 'MONGODB_FSYNC'),
            # ('write_concern', 'MONGODB_REPLICA_SET_W'),
            # ('database', 'MONGODB_DATABASE'),
            # ('collection', 'MONGODB_COLLECTION'),
            ('separate_collections', 'MONGODB_SEPARATE_COLLECTIONS'),
            ('replica_set', 'MONGODB_REPLICA_SET'),
            ('unique_key', 'MONGODB_UNIQUE_KEY'),
            ('buffer', 'MONGODB_BUFFER_DATA'),
            ('append_timestamp', 'MONGODB_ADD_TIMESTAMP'),
            ('stop_on_duplicate', 'MONGODB_STOP_ON_DUPLICATE')
        ]
        # 加载 settings中的配置
        for key, setting in options:
            if not not_set(self.settings[setting]):
                self.config[key] = self.settings[setting]

        # Check for illegal configuration
        if self.config['buffer'] and self.config['unique_key']:
            msg = (
                u'IllegalConfig: Settings both MONGODB_BUFFER_DATA '
                u'and MONGODB_UNIQUE_KEY is not supported'
            )
            self.logger.error(msg)
            raise SyntaxError(msg)
    def load_spider(self, spider):
        self.crawler = spider.crawler
        self.settings = spider.settings
    def open_spider(self, spider):
        self.load_spider(spider)
        self.configure()
        if self.config['stop_on_duplicate']:
            tmpValue = self.config['stop_on_duplicate']
            if tmpValue < 0:
                msg = (
                    u'Negative values are not allowed for'
                    u' MONGODB_STOP_ON_DUPLICATE option.'
                )
                self.logger.error(msg)
                raise SyntaxError(msg)

            self.stop_on_duplicate = self.config['stop_on_duplicate']

        else:
            self.stop_on_duplicate = 0
    def process_item(self, item, spider):
        item = dict(self._get_serialized_fields(item))

        item = dict((k, v) for k, v in six.iteritems(item) if v is not None and v != "")
        item['task_id'] = get_task_id()
        # save_item_mongo(item_dict)
        # return item

        if self.config['buffer']:
            self.current_item += 1

            if self.config['append_timestamp']:
                item['scrapy-crawlab-mongo'] = {'ts': datetime.datetime.utcnow()}

            self.item_buffer.append(item)

            if self.current_item == self.config['buffer']:
                self.current_item = 0
                try:
                    return self.insert_item(self.item_buffer, spider)
                finally:
                    item_buffer = []

            return item
        self.insert_item(item, spider)
    def insert_item(self, item, spider):
        """Process the item and add it to MongoDB.
        :type item: (Item object) or [(Item object)]
        :param item: The item(s) to put into MongoDB
        :type spider: BaseSpider object
        :param spider: The spider running the queries
        :returns: Item object
        """
        if not isinstance(item, list):
            item = dict(item)

            if self.config['append_timestamp']:
                item['scrapy-crawlab-mongo'] = {'ts': datetime.datetime.utcnow()}

        # collection_name = os.environ.get('CRAWLAB_COLLECTION') or 'test'
        collection = get_col(spider.name)
        if self.config['unique_key'] is None:
            try:
                collection.insert(item, continue_on_error=True)
                self.logger.debug(u'Stored item(s) in MongoDB {0}/{1}'.format(
                    self.config['database'], collection.name))

            except errors.DuplicateKeyError:
                self.logger.debug(u'Duplicate key found')
                if self.stop_on_duplicate > 0:
                    self.duplicate_key_count += 1
                    if self.duplicate_key_count >= self.stop_on_duplicate:
                        self.crawler.engine.close_spider(
                            spider,
                            'Number of duplicate key insertion exceeded'
                        )
        else:
            key = {}

            if isinstance(self.config['unique_key'], list):
                for k in dict(self.config['unique_key']).keys():
                    key[k] = item[k]
            else:
                key[self.config['unique_key']] = item[self.config['unique_key']]

            collection.update(key, item, upsert=True)

            self.logger.debug(u'Stored item(s) in MongoDB {0}/{1}'.format(
                self.config['database'], collection.name))

        return item