"""
chatrelater.visualization
~~~~~~~~~~~~~~~~~~~~~~~~~

Visualize relations between chat partners using GraphViz_ (has to be
installed).

.. _GraphViz: http://www.graphviz.org/

:Copyright: 2007-2021 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

import math
from typing import List, Tuple

from graphviz import Digraph, Graph
from graphviz.dot import Dot

from .nicknames import Nickname


DEFAULT_FORMAT = 'dot'
DEFAULT_PROGRAM = 'dot'


def generate_dot(
    nicknames: List[Nickname],
    relations: List[Tuple[Nickname, Nickname, int]],
    *,
    name: str,
    format: str,
    program: str,
    directed: bool = False,
) -> Dot:
    """Create dot graph representations."""
    dot = _create_graph(name, format, program, directed=directed)
    _create_nodes(dot, nicknames)
    _create_edges(dot, relations)
    return dot


def _create_graph(
    name: str, format: str, program: str, *, directed: bool
) -> Dot:
    attrs = {
        'name': name,
        'format': format,
        'engine': program,
    }

    if directed:
        return Digraph(**attrs)
    else:
        return Graph(**attrs)


def _create_nodes(dot: Dot, nicknames: List[Nickname]) -> None:
    for nickname in nicknames:
        dot.node(nickname, label=nickname)


def _create_edges(
    dot: Dot, relations: List[Tuple[Nickname, Nickname, int]]
) -> None:
    max_count = float(max(rel[2] for rel in relations))
    max_width = 4
    for nickname1, nickname2, count in sorted(relations, key=lambda x: x[0]):
        width = math.ceil(count / max_count * max_width)
        dot.edge(nickname1, nickname2, style=f'setlinewidth({width:d})')


def write_file(dot: Dot) -> None:
    """Create a graphics file from the DOT data."""
    rendered_filename = dot.render()
    print(
        f"Wrote {dot.format} output to '{rendered_filename}' using {dot.engine}."
    )
