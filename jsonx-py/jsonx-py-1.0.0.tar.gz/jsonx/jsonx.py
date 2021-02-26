import json
import re
from typing import List, Union


def unflatten(data: dict) -> Union[list, dict]:
    hydrated_data = []
    list_path_regex = "^\[([0-9]+)\]$"
    list_pattern = re.compile(list_path_regex)

    # decide if data should be dict or list
    keys = list(data.keys())
    for key in keys:
        root_segment = key.split(".")[0]
        if not list_pattern.match(root_segment):
            hydrated_data = {}

    def set_value(data: Union[dict, list], full_path: List[str], value) -> Union[list, dict]:
        if len(full_path) == 0:
            raise ValueError("full_path should be a non-empty list of strings")
        elif len(full_path) == 1:
            segment = full_path[0]

            if list_pattern.match(segment):
                assert type(data) == list
                index = int(re.search(list_path_regex, segment).group(1))

                # fill the list with null values until we have enough to address the index
                while len(data) < index + 1:
                    data.append(None)

                data[index] = value
            else:
                data[segment] = value
        else:
            current_segment = full_path.pop(0)
            next_segment = full_path[0]

            # check if current segment is a list
            if list_pattern.match(current_segment):
                assert type(data) == list
                index = int(re.search(list_path_regex, current_segment).group(1))

                while len(data) < index + 1:
                    data.append(None)

                if data[index] == None:
                    if list_pattern.match(next_segment) and not data[index]:
                        data[index] = []
                    else:
                        data[index] = {}

                set_value(data=data[index], full_path=full_path, value=value)

            else:
                # current segment is a dict key
                if not data.get(current_segment):
                    data[current_segment] = [] if list_pattern.match(next_segment) else {}

                set_value(data=data[current_segment], full_path=full_path, value=value)

        return data

    for key, value in data.items():
        path = key.split(".")

        set_value(data=hydrated_data, full_path=path, value=value)

    return hydrated_data
