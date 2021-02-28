#!/usr/bin/env python3
import sys

import pandas
import seaborn
from matplotlib import pyplot

from dplot.parsers import parse_args, print_args

args, sources = parse_args(sys.argv)

if args.verbose:
    print_args(args, sources)

df = None

guessed_title = ""

for source in sources:
    header_names = source.headers.split(",") if source.headers else None

    frame = pandas.read_csv(source.input, sep=r"\s+", skiprows=source.skip, names=header_names, index_col=args.x)

    if args.verbose:
        print(frame)

    if df is None:
        df = frame
    else:
        df = pandas.merge(left=df, right=frame, left_index=True, right_index=True, how='outer')

    if args.title is None:
        with open(source.input) as f:
            for raw_line in f:
                line = raw_line.rstrip()

                try:
                    line_chunks = line.split()
                    split = list(map(float, line_chunks))
                    break
                except Exception as e:
                    guessed_title += line + "\n"

if args.verbose:
    print(df)

if len(sources) == 1 and df.shape[1] == 1:
    plot = seaborn.relplot(x=args.x, y=(set(df.keys()) - set(args.x)).pop(), kind="line", data=df)
    args.y = (set(df.keys()) - set(args.x)).pop()
else:
    plot = seaborn.relplot(kind="line", data=df)

plot.set(title=args.title or guessed_title, xlabel=args.x_label or args.x, ylabel=args.y_label or args.y)

seaborn.set_theme(style="darkgrid")

if args.log:
    plot.fig.get_axes()[0].set_yscale('log')

if args.output == "-":
    pyplot.show()
else:
    plot.savefig(args.output)
