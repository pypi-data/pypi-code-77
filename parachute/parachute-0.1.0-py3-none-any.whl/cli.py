#!/usr/bin/env python3
import argparse
import datetime
import json
import sys
import time
from dataclasses import dataclass
from typing import Any
from typing import Dict
from typing import List

from pymavlink import mavutil
from tqdm import tqdm


@dataclass(order=True)
class Param:
    name: str
    value: Any
    index: int
    type: int

    def as_dict(self) -> Dict[str, Any]:
        return {"value": self.value, "index": self.index, "type": self.type}


class Communicator:
    def __init__(self, craft_name: str, socket: str):
        self._master = mavutil.mavlink_connection(socket)
        self._master.wait_heartbeat()
        self.craft_name = craft_name

    def write_params(self, params: List[Param]):
        filename = (
            f"{self.craft_name}_"
            f"{datetime.datetime.now().strftime('%Y_%m_%d_%H_%M')}"
            ".json"
        )
        with open(filename, "w") as outfile:
            json.dump(
                {param.name: param.as_dict() for param in sorted(params)},
                outfile,
                indent=2,
                sort_keys=True,
            )

    def read_params(self) -> List[Param]:
        # From https://www.ardusub.com/developers/pymavlink.html.
        self._master.mav.param_request_list_send(
            self._master.target_system, self._master.target_component, 1
        )
        params = []
        pbar = tqdm(total=1, dynamic_ncols=True)
        while True:
            # Read all messages, as AP eventually freezes if we try to
            # ignore too many message types.
            message = self._master.recv_match(blocking=True).to_dict()

            if message.get("mavpackettype", "") != "PARAM_VALUE":
                # Ignore non-parameter messages.
                continue

            name, value, type, count, index = (
                message["param_id"],
                message["param_value"],
                message["param_type"],
                message["param_count"],
                message["param_index"],
            )
            pbar.total = count
            pbar.update(1)
            params.append(Param(name, value, index, type))
            if index == count - 1:
                break
        pbar.close()
        return params


def cli():
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument(
        "craft_name", help="The name of the craft",
    )
    parser.add_argument(
        "socket", help="The path to the socket",
    )

    args = parser.parse_args()

    c = Communicator(args.craft_name, args.socket)
    print("Reading parameters...")
    params = c.read_params()
    print("Writing to file...")
    c.write_params(params)
    print("Done.")


if __name__ == "__main__":
    cli()
