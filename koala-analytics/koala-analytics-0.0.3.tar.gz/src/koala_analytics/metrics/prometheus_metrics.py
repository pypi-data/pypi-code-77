import requests
import datetime


from koala_analytics.metrics.base_metrics import BaseMetrics
from koala_analytics.connectors.bq_connector import BigQueryConnector


class PrometheusMetrics(BaseMetrics):

    def __init__(self, metrics: dict):
        super().__init__()
        self._metrics = metrics

    def get_metrics(self, connector: BigQueryConnector, table: str,  *args, **kwargs):
        latest_timestamp = self._get_latest_timestamp(connector, table)
        start, end = self._get_times(latest_timestamp)

        start_dt = datetime.datetime.fromtimestamp(start).strftime("%d-%m-%Y %H:%M:%S")
        end_dt = datetime.datetime.fromtimestamp(end).strftime("%d-%m-%Y %H:%M:%S")

        formatted_data = []

        self._logger.info(f"Fetching prometheus metrics from {start_dt} to {end_dt}\n")

        for metric, url in self._metrics.items():
            self._logger.info(f"* Fetching prometheus metric {metric} *")

            raw_data = self._get_metric(url=url,
                                        metric=metric,
                                        start=start,
                                        end=end)

            data = self._format_metric_data(data=raw_data, metric=metric)
            self._logger.info(f"    Fetched {len(data)} rows.")
            data = self._verify_formatted_data(formatted_data=data,
                                               metric=metric,
                                               start=start,
                                               end=end)
            formatted_data.extend(data)

        self._logger.info(f"\n** Fetched {len(formatted_data)} rows in total **")
        return formatted_data

    @staticmethod
    def _get_metric(url: str, metric: str, start: int, end: int, step: int = 60) -> dict:
        response = requests.get(url, params={"query": metric,
                                             "start": start,
                                             "end": end,
                                             "step": step})
        response.raise_for_status()
        return response.json()

    @staticmethod
    def _verify_formatted_data(formatted_data: list, metric: str, start: int, end: int, step: int = 60):
        number_of_points = int((end-start)/step) + 1
        expected_timestamps = [start + i*step for i in range(number_of_points)]
        actual_timestamps = [row["timestamp"] for row in formatted_data]

        difference = list(set(expected_timestamps).difference(actual_timestamps))

        for timestamp in difference:
            formatted_data.append({"timestamp": timestamp,
                                   "metric": metric,
                                   "value": "0"})

        return formatted_data

    @staticmethod
    def _format_metric_data(data: dict, metric: str) -> list:
        formatted_data = []
        raw_data = data["data"]["result"]

        for result in raw_data:
            for row in result["values"]:
                formatted_data.append({"timestamp": row[0],
                                       "metric": metric,
                                       "value": row[1]})

        return formatted_data
