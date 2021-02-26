import logging
import datetime

from abc import ABC
from abc import abstractmethod

from koala_analytics.connectors.bq_connector import BigQueryConnector


class BaseMetrics(ABC):
    def __init__(self):
        self._logger = self._create_logger()

    def _create_logger(self) -> logging.Logger:
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)

        logger.addHandler(handler)

        return logger

    @abstractmethod
    def get_metrics(self, *args, **kwargs) -> list:
        raise NotImplementedError()

    @staticmethod
    def _get_latest_timestamp(connector: BigQueryConnector, table: str) -> int:
        now = datetime.datetime.now()
        today_midnight = int(datetime.datetime(year=now.year,
                                               month=now.month,
                                               day=now.day,
                                               hour=0,
                                               minute=0).timestamp())

        bq_query = f"select max(timestamp) as latest_timestamp from {table}"
        latest_timestamp_result = connector.execute_bq_query(query=bq_query)[0]["latest_timestamp"]

        if latest_timestamp_result is None:
            return today_midnight
        else:
            return latest_timestamp_result

    @staticmethod
    def _get_times(timestamp: int) -> tuple:
        start = timestamp + 60
        end = int(datetime.datetime.now().timestamp())
        return start, end - end % 60
