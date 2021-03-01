from math import floor


def bar(width: int, percent: float) -> str:
    bar = ""
    percent_per_block = 1.0 / width
    remaining_percent = percent

    for _ in range(width):
        fill_percent_of_this_block = min(
            1.0, (1.0 / percent_per_block) * remaining_percent
        )
        remaining_percent -= min(remaining_percent, percent_per_block)
        bar += block(fill_percent_of_this_block)

    return bar


def block(percent: float) -> str:
    return " " if percent == 0.0 else chr(0x258F - floor(percent / (1.0 / 7)))
