#  Copyright (c) 2020. Davi Pereira dos Santos and Rafael Amatte Bisão
#  This file is part of the oka project.
#  Please respect the license. Removing authorship by any means
#  (by code make up or closing the sources) or ignoring property rights
#  is a crime and is unethical regarding the effort and time spent here.
#  Relevant employers or funding agencies will be notified accordingly.
#
#  oka is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  oka is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with oka.  If not, see <http://www.gnu.org/licenses/>.
#

from dataclasses import dataclass

from tatu.okast import default_url


@dataclass
class Oka:
    """Handle posts from command line to spare the user from accessing the web to publish results."""
    # TODO: put sync here also
    id: str = None
    url: str = default_url
    token: str = None

    def __lshift__(self, other):
        """Can receive a Data object or a tuple (data, name, description)."""
        from oka.io import send  # Import is here just to avoid being directly importable from oka module.
        if isinstance(other, tuple):
            send(other[0], self.url, self.token, *other[1:])
        send(other, self.url, self.token)

    def __rmatmul__(self, other):
        from oka.io import get  # Import is here just to avoid being directly importable from oka module.
        return get(other, self.url, self.token)

    # noinspection PyArgumentList
    def __call__(self, id=None, url=None):
        from oka.io import get  # Import is here just to avoid being directly importable from oka module.
        if url is None:
            url = self.url
        if id is None:
            return self.__class__(url=url)
        return get(id, url, self.token)


oka = Oka()
