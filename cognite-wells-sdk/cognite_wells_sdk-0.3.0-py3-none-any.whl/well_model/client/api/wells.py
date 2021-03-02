import logging
import urllib.parse
from typing import Dict, List, Optional

from requests import Response

from cognite.well_model.client._api_client import APIClient
from cognite.well_model.client.api.api_base import BaseAPI
from cognite.well_model.client.api.wellbores import WellboresAPI
from cognite.well_model.client.utils._auxiliary import extend_class
from cognite.well_model.models import Well, Wellbore, WellFilter, WellItems

logger = logging.getLogger("WellsAPI")


class WellsAPI(BaseAPI):
    def __init__(self, wells_client: APIClient, wellbores_api: WellboresAPI):
        super().__init__(wells_client)
        self.wellbores_api = wellbores_api

        # wrap all wells with a lazy method
        @extend_class(Well)
        def wellbores(well) -> Optional[List[Wellbore]]:
            return self.wellbores_api.get_from_well(well_id=well.id)

    @staticmethod
    def deserialize_well_items(well_items_dict: Dict) -> WellItems:
        """
        deserialize a json dictionary to a WellItems object

        @param well_items_dict: key-word arguments to deserialize
        @return: List of wells
        """

        # if we set next_cursor=None then you can no longer access it as an attribute of WellItems
        # a solution is to init next_cursor as an empty string
        well_items: WellItems = WellItems.parse_obj(well_items_dict)
        return well_items

    def _get_label_prefix(self, prefix: str) -> List[str]:
        """
        list valid values for prefix

        @param prefix: which label to filter on
        @return: list of valid label values
        """
        path: str = self._get_path(f"/wells/{prefix}")
        response: Response = self.wells_client.get(url_path=path)
        data: List[str] = response.json()
        return data

    def blocks(self) -> List[str]:
        """ List valid block values """
        return self._get_label_prefix("blocks")

    def fields(self) -> List[str]:
        """ List valid field values """
        return self._get_label_prefix("fields")

    def operators(self) -> List[str]:
        """ List valid operator values """
        return self._get_label_prefix("operators")

    def quadrants(self) -> List[str]:
        """ List valid quadrant values """
        return self._get_label_prefix("quadrants")

    def sources(self) -> List[str]:
        """ List valid source values """
        return self._get_label_prefix("sources")

    def measurements(self) -> List[str]:
        """ List valid measurement type values """
        return self._get_label_prefix("measurements")

    def get_by_id(self, well_id: int) -> Well:
        """
        Get well from a cdf asset id

        @param well_id: cdf asset id
        @return: Well object
        """
        path: str = self._get_path(f"/wells/{well_id}")
        response: Response = self.wells_client.get(url_path=path)
        well: Well = Well.parse_raw(response.text)
        return well

    def list(self, cursor: Optional[str] = None) -> WellItems:
        """
        list all wells

        @param cursor: cursor for pagination
        @return: WellItems object
        """
        path: str = self._get_path("/wells")
        if cursor:
            path += urllib.parse.urlencode({"cursor": f"{cursor}"})
        response: Response = self.wells_client.get(url_path=path)
        well_items: WellItems = WellItems.parse_raw(response.text)
        return well_items

    def filter(self, wellFilter: WellFilter, cursor: Optional[str] = None) -> WellItems:
        """
        Get wells that matches the filter

        @param wellFilter: the applied filter
        @param cursor: cursor for paginating results
        @return: WellItems object
        """
        path: str = self._get_path("/wells/list")
        if cursor:
            path += urllib.parse.urlencode({"cursor": f"{cursor}"})
        response: Response = self.wells_client.post(url_path=path, json=wellFilter.json())
        well_items_data: WellItems = WellItems.parse_raw(response.text)
        return well_items_data
