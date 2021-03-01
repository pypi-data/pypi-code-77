import logging
from typing import List

from requests import Response

from cognite.well_model.client._api_client import APIClient
from cognite.well_model.client.api.api_base import BaseAPI
from cognite.well_model.client.utils._deserialize import deserialize_list
from cognite.well_model.model.model_utils import model_to_dict
from cognite.well_model.model.models import (
    CasingIngestion,
    GetSequenceDTO,
    Well,
    Wellbore,
    WellboreIngestion,
    WellIngestion,
)

logger = logging.getLogger("WellsAPI")


class IngestionAPI(BaseAPI):
    def __init__(self, wells_client: APIClient):
        super().__init__(wells_client)

    def ingest_casings(self, ingestions: List[CasingIngestion]):
        path = self._get_path("/ingestion/casings")
        data_request_serialized = [model_to_dict(x) for x in ingestions]
        response: Response = self.wells_client.post(path, data_request_serialized)
        return deserialize_list(response.json(), GetSequenceDTO)

    def ingest_wells(self, ingestions: List[WellIngestion]):
        path = self._get_path("/ingestion/wells")
        data_request_serialized = [model_to_dict(x) for x in ingestions]
        response: Response = self.wells_client.post(path, data_request_serialized)
        return deserialize_list(response.json(), Well)

    def ingest_wellbores(self, ingestions: List[WellboreIngestion]):
        path = self._get_path("/ingestion/wellbores")
        data_request_serialized = [model_to_dict(x) for x in ingestions]
        response: Response = self.wells_client.post(path, data_request_serialized)
        return deserialize_list(response.json(), Wellbore)
