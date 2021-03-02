import logging
from typing import Optional

from cognite.well_model.client._api_client import APIClient
from cognite.well_model.client.utils._client_config import Cluster

logger = logging.getLogger(__name__)


class BaseAPI:
    def __init__(self, wells_client: APIClient):
        self.wells_client: APIClient = wells_client

    @property
    def project(self) -> str:
        return self.wells_client._config.project

    @property
    def cluster(self) -> Optional[Cluster]:
        return self.wells_client._config.cluster

    def _get_path(self, base_url: str) -> str:
        if self.cluster and self.cluster.requires_cluster_selection:
            return f"/{self.project}{base_url}?env={self.cluster}"
        return f"/{self.project}{base_url}"
