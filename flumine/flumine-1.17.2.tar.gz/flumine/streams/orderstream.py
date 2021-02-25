import queue
import logging
from betfairlightweight import BetfairError, filters
from tenacity import retry

from .basestream import BaseStream
from ..events.events import CurrentOrdersEvent
from .. import config

logger = logging.getLogger(__name__)

RETRY_WAIT = BaseStream.RETRY_WAIT


class OrderStream(BaseStream):
    @retry(wait=RETRY_WAIT)
    def run(self) -> None:
        logger.info(
            "Starting OrderStream {0}".format(self.stream_id),
            extra={
                "stream_id": self.stream_id,
                "customer_strategy_refs": config.hostname,
                "conflate_ms": self.conflate_ms,
                "streaming_timeout": self.streaming_timeout,
            },
        )
        if not self._output_thread.is_alive():
            logger.info(
                "Starting output_thread (OrderStream {0})".format(self.stream_id)
            )
            self._output_thread.start()

        self._stream = self.betting_client.streaming.create_stream(
            unique_id=self.stream_id, listener=self._listener
        )
        try:
            self.stream_id = self._stream.subscribe_to_orders(
                order_filter=filters.streaming_order_filter(
                    customer_strategy_refs=[config.hostname],
                    partition_matched_by_strategy_ref=True,
                    include_overall_position=False,
                ),
                conflate_ms=self.conflate_ms,
            )
            self._stream.start()
        except BetfairError:
            logger.error(
                "OrderStream {0} run error".format(self.stream_id), exc_info=True
            )
            raise
        except Exception:
            logger.critical(
                "OrderStream {0} run error".format(self.stream_id), exc_info=True
            )
            raise
        logger.info("Stopped OrderStream {0}".format(self.stream_id))

    def handle_output(self) -> None:
        """Handles output from stream."""
        while self.is_alive():
            try:
                order_books = self._output_queue.get(
                    block=True, timeout=self.streaming_timeout
                )
            except queue.Empty:  # todo snap every 5s or so anyway
                if self.flumine.markets.live_orders:
                    order_books = self._listener.snap(
                        market_ids=self.flumine.markets.open_market_ids
                    )
                else:
                    continue
            if order_books:
                self.flumine.handler_queue.put(CurrentOrdersEvent(order_books))

        logger.info("Stopped output_thread (OrderStream {0})".format(self.stream_id))
