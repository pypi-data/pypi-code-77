import json
import datetime

from influxdb import InfluxDBClient
from influxdb.resultset import ResultSet

from koala_analytics.metrics.base_metrics import BaseMetrics


class InfluxMetrics(BaseMetrics):

    def __init__(self, host: str, port: int, username: str, password: str, database: str):
        super().__init__()
        self._client = self._create_client(host, port, username, password, database)

    def get_metrics(self, metrics: list, *args, **kwargs) -> list:

        formatted_data = []

        self._logger.info(f"Fetching InfluxDB metrics.")

        for metric in metrics:
            self._logger.info(f"* Fetching prometheus metric {metric} *")

            raw_data = self._get_metric(influx_query=metric)

            data = self._format_influx_data(raw_data)
            self._logger.info(f"    Fetched {len(data)} rows.")
            formatted_data.extend(data)

        self._logger.info(f"\n** Fetched {len(formatted_data)} rows in total **")
        return formatted_data

    def _get_metric(self, influx_query: str):
        result = self._client.query(influx_query)

        return result

    @staticmethod
    def _format_influx_data(result: ResultSet, time_key: str = "time"):
        data = []
        for key, values in result.items():
            current_values = [row for row in values]

            for value in current_values:
                value["prop"] = json.dumps(key[1])
                value["metric"] = key[0]

            data.extend(current_values)

        for value in data:
            value["timestamp"] = int(datetime.datetime.strptime(value[time_key], "%Y-%m-%dT%H:%M:%SZ").timestamp())
            value.pop(time_key)

        return data

    @staticmethod
    def _create_client(host: str, port: int, username: str, password: str, database: str):
        return InfluxDBClient(host=host,
                              port=port,
                              username=username,
                              password=password,
                              database=database)
