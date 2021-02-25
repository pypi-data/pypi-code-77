# Copyright 2019 Axis Communications AB.
#
# For a full list of individual contributors, please see the commit history.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""EiffelSourceChangeSubmittedEvent.

https://github.com/eiffel-community/eiffel/blob/master/eiffel-vocabulary/EiffelSourceChangeSubmittedEvent.md
"""
from eiffellib.events.eiffel_base_event import (EiffelBaseEvent, EiffelBaseLink,
                                                EiffelBaseData, EiffelBaseMeta)


class EiffelSourceChangeSubmittedLink(EiffelBaseLink):
    """Link object for eiffel source change submitted event."""


class EiffelSourceChangeSubmittedData(EiffelBaseData):
    """Data object for eiffel source change submitted event."""


class EiffelSourceChangeSubmittedEvent(EiffelBaseEvent):
    """Eiffel source change submitted event."""

    version = "3.0.0"

    def __init__(self, version=None):
        """Initialize data, meta and links."""
        super(EiffelSourceChangeSubmittedEvent, self).__init__(version)
        self.meta = EiffelBaseMeta("EiffelSourceChangeSubmittedEvent", self.version)
        self.links = EiffelSourceChangeSubmittedLink()
        self.data = EiffelSourceChangeSubmittedData()
