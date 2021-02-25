"""
MVG library
-----------
For more inforamation see README.md.
"""

# pylint: disable=R0913

import json
import logging
import requests
from requests.exceptions import HTTPError

logger = logging.getLogger(__name__)


def va_raise_for_status(response):
    """
    Will call raise_for_status from the requests
    library on the response object.
    In case logger is set to DEBUG
    addititional additional error information is logged.
    The additional information is also present in the
    raised exception as e.response.json().


    Parameters
    ----------
    response
        response requests response object

    Raises
    -----
    HTTPError
        the original HTTPError from raise_for_status

    """

    try:
        response.raise_for_status()
    except HTTPError as exc:
        logger.debug(str(exc))
        if response.text:
            logger.debug(str(response.text))
            raise exc
    # return


class MVG:
    """Class for a session providing an API to the vibium server"""

    def __init__(self, endpoint: str, token: str):
        """
        Constructor

        On instantiation of a MVG object the session parameters
        are stored for future calls.
        In case token is "NO TOKEN", will insert the harcoded
        valid token from testcases.

        Parameters
        ----------
        endpoint: str
            the server address (URL).

        token: str
            the token used for authentication and authorization.

        """

        self.endpoint = endpoint
        self.token = token

    def _get_headers(self):
        """
        Return headers. Currently only authorization header.
        {'Authorization': 'Bearer TOKEN'}

        Returns
        ------
        headers : dict
        """
        headers = {"Authorization": f"Bearer {self.token}"}
        return headers

    def get_endpoint(self):
        """
        Accessor function.

        Returns
        -------
        endpoint : str
        Endpoint sent to constructor
        """
        return self.endpoint

    def get_token(self):
        """
        Accessor function.

        Returns
        -------
        token : str
        Token  sent to constructor
        """
        return self.token

    def say_hello(self):
        """
        Retrievs information about the API.
        This call does not require a valid token.

        Returns
        ------
        message : dict
        Hello message with info on MVG API.
        """
        logger.info("Getting API info for: %s", self.endpoint)

        # Build url
        url = self.endpoint

        # send request (do the call)
        response = requests.get(url, headers=self._get_headers())

        # check status code
        va_raise_for_status(response)

        # return list of IDs
        return response.json()["message"]

    def create_source(self, sid: str, meta: dict):
        """
        Creates a source on the server side.

        Parameters
        ----------
        sid : str
            source Id

        meta : dict
            meta information
        """

        logger.info("endpoint %s", self.endpoint)
        logger.info("creating source with source id=%s", sid)
        logger.info("metadata: %s", meta)

        # Build url
        url = self.endpoint + "/sources/"

        # Package info to be submitted to db
        source_info = {"source_id": sid, "meta": meta}

        # send request (do the call)
        response = requests.post(url, json=source_info, headers=self._get_headers())

        # check status code
        va_raise_for_status(response)

        # In example

    def list_sources(self):
        """Lists all sources (sensors) on the server side

        Returns
        -------
        list of all source id:s known to the server

        """

        logger.info("endpoint %s", self.endpoint)
        logger.info("listing sources")

        # Build url
        url = self.endpoint + "/sources/"

        # send request (do the call)
        response = requests.get(url, headers=self._get_headers())

        # check status code
        va_raise_for_status(response)

        # return list of IDs
        return response.json()

    # In example
    def get_source(self, sid: str):
        """Returns the information stored for a source representing
        on the given endpoint.

        Parameters
        ----------
        sid: str
            source Id.

        Returns
        -------
        source_information: (dict)
            Information stored about the source.
        """

        logger.info("endpoint %s", self.endpoint)
        logger.info("retrieving source with source id=%s", sid)

        # Build url
        url = self.endpoint + f"/sources/{sid}"

        # send request (do the call)
        response = requests.get(url, headers=self._get_headers())

        # check status code
        va_raise_for_status(response)

        # return list of IDs
        return response.json()

    # In example
    def update_source(self, sid: str, meta: dict):
        """
        Replaces source meta information on the server side.

        Parameters
        ----------
        sid: str
            source Id.

        meta: dict
            meta information to replace old meta information.
        """

        logger.info("endpoint %s", self.endpoint)
        logger.info("updating source with source id=%s", sid)
        logger.info("metadata: %s", meta)

        # Build url
        url = self.endpoint + f"/sources/{sid}"

        # send request (do the call)
        response = requests.put(url, data=json.dumps(meta), headers=self._get_headers())

        # check status code
        va_raise_for_status(response)

    # In example
    def delete_source(self, sid: str):
        """Deletes a source on the given endpoint.

        Parameters
        ----------
        sid: str
            source Id.
        """

        logger.info("endpoint %s", self.endpoint)
        logger.info("deleting source with source id=%s", sid)

        # Build url
        url = self.endpoint + f"/sources/{sid}"

        # send request (do the call)
        response = requests.delete(url, headers=self._get_headers())

        # check status code
        va_raise_for_status(response)

    ####################################
    # Measurements
    # in example
    def create_measurement(
        self, sid: str, duration: float, timestamp: int, data: list, meta: dict
    ):
        """Stores a measurement on the server side.

        Although it is up to the client side to handle the
        scaling of data it is recommended that the values
        represent the acceleration in g.
        The timestamp shall represent the time when the measurement was
        recorded.

        Parameters
        ----------
        sid: str
            source Id.

        duration: float
            duration of the measurement in seconds.

        timestamp: int
            in milliseconds since EPOCH.

        data: list
            list of float values.

        meta: dict
            Meta information to attach to data.

        """

        logger.info("endpoint %s", self.endpoint)
        logger.info("creating measurement from source id=%s", sid)
        logger.info("  duration:  %s", duration)
        logger.info("  timestamp: %s", timestamp)
        logger.info("  meta data: %s", meta)

        # Build url
        url = self.endpoint + "/sources/" + sid + "/measurements"

        # Package info for db to be submitted
        meas_struct = {
            "source_id": sid,  # should be source_id
            "timestamp": timestamp,
            "duration": duration,
            "data": data,
            "meta": meta,
        }

        # send request (do the call)
        response = requests.post(url, json=meas_struct, headers=self._get_headers())
        va_raise_for_status(response)

    # in example
    def read_measurements(self, sid: str):
        """Retrieves all measurements for all timestamps for a source.

        Parameters
        ----------
        sid : str
            source Id.

        Returns
        -------
        An array of arrays of single measurements.

        """
        logger.info("endpoint %s", self.endpoint)
        logger.info("retrieving all measurements from source id=%s", sid)

        # Build url
        url = self.endpoint + f"/sources/{sid}/measurements"

        # send request (do the call)
        response = requests.get(url, headers=self._get_headers())

        # check status code
        va_raise_for_status(response)

        # Step 2: read actual measurement data for all timestamps
        timestamps = response.json()
        logger.info("%s measurements in database", len(timestamps))

        all_measurements = []
        for m_time in timestamps:
            all_measurements.append(
                self.read_single_measurement(sid, m_time["timestamp"])
            )

        return all_measurements

    # in example
    def read_single_measurement(self, sid: str, timestamp: int):
        """
        Retrieves all measurements for one single timestamps from source Id.

        The format of the returned measurement is
        an array with the first value being the time stamp and the
        subsequent values being the data (samples).

        Parameters
        ----------
        sid : str
            source Id.

        timestamp : int
            in milliseconds since EPOCH.

        Returns
        -------
        array of measurements.
        """

        logger.info("endpoint %s", self.endpoint)
        logger.info("retrieving measurements from source id=%s", sid)
        logger.info("timestamp=%s", timestamp)

        # Build url
        url = self.endpoint + f"/sources/{sid}/measurements/{timestamp}"

        # send request (do the call)
        response = requests.get(url, headers=self._get_headers())

        # check status code
        va_raise_for_status(response)

        return response.json()

    # in example
    def update_measurement(self, sid: str, timestamp: int, meta: dict):
        """Replaces meta information along measurement.
        It is not possible to update the actual measurement
        data.

        Parameters
        ----------
        sid: str
            source Id.

        timestamp: int
            in milliseconds since EPOCH. Identifies measurement.

        meta: dict
            Meta information to attach to data.
        """

        logger.info("endpoint %s", self.endpoint)
        logger.info("deleting measurement for source id=%s", sid)
        logger.info("  timestamp: %s", timestamp)

        # Build url
        url = self.endpoint + "/sources/" + sid + "/measurements/" + str(timestamp)

        # send request (do the call)
        response = requests.put(url, data=json.dumps(meta), headers=self._get_headers())
        # check status code
        va_raise_for_status(response)

    # In example
    def delete_measurement(self, sid: str, timestamp: int):
        """Deletes a measurement.

        Parameters
        ----------
        sid: str
            source Id. Identifies source.

        timestamp: int
            in milliseconds since EPOCH. Identifies measurement.

        """

        logger.info("endpoint %s", self.endpoint)
        logger.info("deleting measurement for source id=%s", sid)
        logger.info("  timestamp: %s", timestamp)

        # Build url
        url = self.endpoint + "/sources/" + sid + "/measurements/" + str(timestamp)

        # send request (do the call)
        response = requests.delete(url, headers=self._get_headers())

        # Check status code
        va_raise_for_status(response)

    # Analysis
    def supported_features(self):
        """Return all supported features.
        Presence of a feature is indicated by string with the
        feature name set to true.
        That string shall be used to specify
        that feature in an analysis request.
        This call does not require a valid token.

        Returns
        -------
        A list of supported features (strings).

        """
        logger.info("endpoint %s", self.endpoint)
        logger.info("retrieving supported features")

        # Build url
        url = self.endpoint + "/analyses/"

        # send request (do the call)
        response = requests.get(url, headers=self._get_headers())

        # check status code
        va_raise_for_status(response)

        return response.json()

    def request_analysis(
        self,
        sid: str,
        feature: str,
        parameters: dict,
        starttime: int,
        endtime: int,
    ):
        """Request an analysis on the given endpoint with given parameters.

        Parameters
        ----------
        sid : str
            source Id.

        feature : str
            name of feature to run.

        parameters : dict
            name value pairs of parameters.

        starttime : int
            start of analysis time window [optional].

        endtime : int
            start of analysis time window [optional].

        Returns
        -------
        jobid: analysis identifier

        """
        logger.info("endpoint %s", self.endpoint)
        logger.info("source id=%s", sid)
        logger.info("sending %s analysis request", feature)
        logger.inof("parameters %s", parameters)
        logger.info("from %s to %s ", starttime, endtime)

        # Build url
        url = self.endpoint + "/analyses/"

        # Package info for db to be submitted
        analysis_info = {"source_id": sid, "feature": 1, "params": parameters}

        # send request (do the call)
        response = requests.post(url, json=analysis_info, headers=self._get_headers())

        # check status code
        va_raise_for_status(response)

        return response.json()

    def get_analysis(self, jobid: str):
        """Retrieves an analysis with given jobId
        The format of the result structure depends on the feature.

        Parameters
        ----------
        jobid : str
            jobid (analysis identifier)

        Returns
        -------
        results: dict
            a diticionary with the results in case available.

        """
        logger.info("endpoint %s", self.endpoint)
        logger.info("get analysis with jobid=%s", jobid)

        # Build url
        url = self.endpoint + "/analyses/" + f"{jobid}"

        # send request (do the call)
        response = requests.get(url, headers=self._get_headers())

        # check status code
        va_raise_for_status(response)

        return response.json()
