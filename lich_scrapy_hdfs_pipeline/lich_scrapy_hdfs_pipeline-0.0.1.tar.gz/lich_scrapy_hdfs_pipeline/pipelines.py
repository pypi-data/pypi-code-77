# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from typing import Optional

from os_scrapy_kafka_pipeline.pipelines import KafkaPipeline, KafKaRecord
from twisted.internet import threads
from twisted.internet.defer import DeferredList

S_URL = "url"
S_REQUEST = "request"
S_META = "meta"
S_HDFS_STORES = "hdfs.stores"
S_HDFS_ENV = "hdfs.env"
S_HDFS_SAVER_TYPE = "hdfs.saver_type"


class LichScrapyHdfsPipeline(KafkaPipeline):
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def kafka_record(self, store, meta) -> Optional[KafKaRecord]:
        if (
            not isinstance(store, dict)
            or "kafka.topic" not in store
            or "kafka.brokers" not in store
        ):
            return None
        record = KafKaRecord()
        record.meta = meta
        record.topic = store.get("kafka.topic", None)
        record.key = store.get("kafka.key", None)
        record.partition = store.get("kafka.partition", None)
        bootstrap_servers = store.get("kafka.brokers", None)
        if isinstance(bootstrap_servers, str):
            record.bootstrap_servers = bootstrap_servers.split(",")
        return record

    def process_item(self, item, spider):
        if not (
            S_META in item
            and isinstance(item[S_META], dict)
            and S_HDFS_STORES in item[S_META]
            and S_HDFS_ENV in item[S_META]
            and isinstance(item[S_META][S_HDFS_STORES], list)
            and not item[S_META].get("kafka.skip", False)
        ):
            return item
        meta = item[S_META]
        hdfs_stores = meta[S_HDFS_STORES]
        sends = []
        for store in hdfs_stores:
            record = self.kafka_record(store, meta)
            if not record:
                self.logger.debug(f"invalid store {store}")
                continue
            try:
                self.kafka_value(item, record)
            except:
                self.log(item, record)
                continue
            sends.append(threads.deferToThread(self.send, item, record))
        if sends:
            sends_deferred = DeferredList(sends, consumeErrors=True)
            sends_deferred.addCallback(lambda _: item)
            return sends_deferred

        return item

    def on_send_fail(self, item, record, e):
        super(KafkaPipeline, self).on_send_fail(item, record, e)
        if not isinstance(e, MessageSizeTooLargeError):
            return
        res = item[S_RESPONSE]
        if isinstance(res[S_FAILURE], MessageSizeTooLargeError):
            return
        rsp = res.copy()
        if S_BODY in rsp:
            rsp[S_BODY] = b""
        retry_item = FetchRecord(
            request=item[S_REQUEST], meta=item[S_META], response=rsp
        )
        self.process_item(retry_item, None)

    def _log_msg(self, item, record):
        msg = super(LichScrapyHdfsPipeline, self)._log_msg(item, record)
        return f"{item[S_REQUEST][S_URL]} {msg}"
