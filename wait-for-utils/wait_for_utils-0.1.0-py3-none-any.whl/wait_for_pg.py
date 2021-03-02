"""Wait for postgres."""
import logging
import time
from typing import Any

import psycopg2

from wait_for_utils.base import BaseReady
from wait_for_utils.config import DBConfig
from wait_for_utils.utils import get_interval_unit

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


class PGReady(BaseReady):
    def _connect(
        self, user: str, password: str, host: str, port: int, database: str
    ) -> Any:
        """Create connect.

        :param user:
        :param password:
        :param host:
        :param port:
        :param database:
        :return:
        """
        conn = psycopg2.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            database=database,
        )
        return conn

    def is_ready(self, config: DBConfig) -> bool:
        """Check the connection is ready.

        :param config:
        :return:
        """
        while time.time() - self.start_time < config.timeout:
            try:
                conn = self._connect(
                    user=config.user,
                    password=config.password,
                    host=config.host,
                    port=config.port,
                    database=config.database,
                )
                logger.info("PostgreSQL is ready!")
                conn.close()
                return True
            except psycopg2.OperationalError:
                logger.info(
                    "Connection details: %s:%s/%s. PostgreSQL is not ready yet. :( "
                    "Waiting %s %s for the next check...",
                    config.host,
                    config.port,
                    config.database,
                    config.interval,
                    get_interval_unit(config.interval),
                )
                time.sleep(config.interval)
        logger.error(
            "Can't connect to PostgreSQL within %d %s :(",
            config.interval,
            get_interval_unit(config.interval),
        )
        return False
