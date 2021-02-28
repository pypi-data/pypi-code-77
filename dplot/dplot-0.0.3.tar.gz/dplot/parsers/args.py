from argparse import ArgumentParser

modes = ["crysol", "psaxs", "debyer", "other"]
switches = ["--" + mode for mode in modes]


def split_args(argv):
    markers = switches

    groups = []
    current = []

    for arg in argv:
        if arg in markers and len(current) > 0:
            groups.append(current.copy())
            current.clear()

        current.append(arg)

    if len(current) > 0:
        groups.append(current.copy())

    return groups


def get_group_parser() -> ArgumentParser:
    parser = ArgumentParser()

    exclusive = parser.add_mutually_exclusive_group(required=True)

    for mode in modes:
        exclusive.add_argument("--" + mode, help=mode + " input file")

    parser.add_argument('--skip', type=int)
    parser.add_argument('--headers')

    return parser


def parse_input_args(argv):
    parser = get_group_parser()

    args = parser.parse_args(argv)

    # Retrieves input file from mutually exclusive arguments
    input_file = [getattr(args, mode) for mode in modes if getattr(args, mode) is not None][0]

    setattr(args, "input", input_file)

    if args.crysol:
        args.skip = 1
        args.headers = "Q,Intensity,Scattering (in vacuo),Scattering (excluded volume),Convex border layer"

    if args.psaxs:
        args.headers = "Q,Intensity"

    if args.debyer:
        args.skip = 2
        args.headers = "Q,Intensity"

    return args


def parse_args(argv):
    parser = ArgumentParser()

    parser.add_argument('output', nargs='?')
    parser.add_argument('--title')
    parser.add_argument('--log', action="store_true")
    parser.add_argument('-x')
    parser.add_argument('-y')
    parser.add_argument('--x-label')
    parser.add_argument('--y-label')
    parser.add_argument('--verbose', action="store_true")

    args, unparsed = parser.parse_known_args(argv[1:])  # It doesn't like script name for some reason

    groups = split_args(unparsed)

    inputs = [parse_input_args(group) for group in groups]

    if any(any(getattr(input, mode) for mode in modes if mode != "other") for input in inputs):
        args.x = "Q"
        args.log = True

    return args, inputs


def print_args(args, inputs):
    print("Shared")
    for arg in vars(args):
        print("  - {}: {}".format(arg, getattr(args, arg)))

    for i, input in enumerate(inputs):
        print("Input ({})".format(i + 1))

        for arg in vars(input):
            print("  - {}: {}".format(arg, getattr(input, arg)))
