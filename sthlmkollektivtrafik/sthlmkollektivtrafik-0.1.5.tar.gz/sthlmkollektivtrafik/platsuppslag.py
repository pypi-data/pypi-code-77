# Platsuppslag
# https://www.trafiklab.se/api/sl-platsuppslag
# version: 2020-07-10

import requests
import json
import sys
import os
import logging

class search:
    def __init__(self, searchString):

        key = os.environ.get('SKT_location_API')

        self.log = []

        logging.debug('This is a debug message')
        try:
            response = requests.get("http://api.sl.se/api2/typeahead.json?key=" + key + "&searchstring=" + searchString + "&stationsonly=true")
            data = response.text
            parsed = json.loads(data)
            self.log.append("Succesfully called the api.")
        except Exception as e:
            self.log.append(e)

        try:
            self.all = parsed
            self.log.append((int(parsed["StatusCode"]), parsed["ExecutionTime"], parsed["Message"]))
            self.responses = len(parsed["ResponseData"])
            self.stations = parsed["ResponseData"]
            self.name = parsed["ResponseData"][0]["Name"]
            self.id = int(parsed["ResponseData"][0]["SiteId"])
            self.type = parsed["ResponseData"][0]["Type"]
        except Exception as e:
            self.log.append(e)