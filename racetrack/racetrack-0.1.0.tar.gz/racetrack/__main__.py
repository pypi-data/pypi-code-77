# -*- coding:utf-8 -*-
#
# Copyright (C) 2021, Saarland University
# Copyright (C) 2021, Maximilian Köhl <koehl@cs.uni-saarland.de>

from __future__ import annotations

import typing as t

import pathlib

import click

from momba import jani

from . import model


@click.group()
def main() -> None:
    """
    Racetrack
    """


@main.command()
@click.argument("track_file", type=pathlib.Path)
@click.argument("output_directory", type=pathlib.Path)
@click.option(
    "--speed-bound", type=int, default=3, help="Maximal allowed speed of the car."
)
@click.option(
    "--acceleration-bound",
    type=int,
    default=2,
    help="Maximal allowed acceleration of the car.",
)
@click.option(
    "--allow-momba-operators",
    default=False,
    is_flag=True,
    help="Use JANI extension `x-momba-operators`.",
)
@click.option(
    "--indent", type=int, default=None, help="Indentation for the JANI files."
)
def generate(
    track_file: pathlib.Path,
    output_directory: pathlib.Path,
    speed_bound: int,
    acceleration_bound: int,
    allow_momba_operators: bool,
    indent: t.Optional[int],
) -> None:
    """
    Generates a family of JANI models from the provided track file.

    TRACK_FILE A Racetrack track in ASCII format.
    OUTPUT_DIRECTORY A directory to write the JANI models to.
    """
    output_directory.mkdir(parents=True, exist_ok=True)

    track = model.Track.from_source(track_file.read_text(encoding="utf-8"))

    print("Generate scenarios...")
    scenarios = tuple(model.generate_scenarios(track, speed_bound, acceleration_bound))

    print(f"Generating {len(scenarios)} models...")

    with click.progressbar(scenarios) as progressbar:
        for scenario in progressbar:
            network = model.construct_model(scenario)
            filename = (
                "car"
                f"_{scenario.max_speed}"
                f"_{scenario.max_acceleration}"
                f"_{scenario.underground.name}"
                f"_{scenario.tank_type.name}"
                f"_{scenario.start_cell}.jani"
            )
            (output_directory / filename).write_bytes(
                jani.dump_model(
                    network,
                    indent=indent,
                    allow_momba_operators=allow_momba_operators,
                )
            )
