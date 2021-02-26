"""Provides additional helper classes for the simulator."""

import bisect


class StartTimeBasedDict:
    """A wrapper around dict with ordered start-time-based keys.

    This wrapper can be used, e.g., to represent different versions of an
    entity which change depending on time. For example, this is helpful for
    contact graphs that change over time.

    """

    def __init__(self, base_dict):
        assert len(base_dict)
        self.base_dict = base_dict
        self.base_dict_keys = list(sorted(base_dict.keys()))

    def _get_key_index(self, time):
        if time < self.base_dict_keys[0]:
            raise ValueError(
                f"provided time is {self.base_dict_keys[0] - time} s "
                f"before start of first item"
            )
        return bisect.bisect_right(self.base_dict_keys, time) - 1

    def get_entry_for(self, time):
        """Get the dict entry valid at the specified time."""
        return self.base_dict[self.base_dict_keys[
            self._get_key_index(time)
        ]]

    def get_entry_and_drop_predecessors(self, time):
        """Get the valid dict entry and drop its predecessors."""
        index = self._get_key_index(time)
        key = self.base_dict_keys[index]
        item = self.base_dict[key]
        for dropk in self.base_dict_keys[:index]:
            del self.base_dict[dropk]
        self.base_dict_keys[:index] = []
        assert self.base_dict_keys[0] == key
        assert key in self.base_dict
        assert self.base_dict[key] is item
        return item
