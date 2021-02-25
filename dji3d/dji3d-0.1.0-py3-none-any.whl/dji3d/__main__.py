import argparse
import sys


def main() -> int:

    # Handle CLI args
    ap = argparse.ArgumentParser(
        prog="dji3d",
        description="DJI3D is a tool for graphing 3d positional data extracted from DJI drone telemetry",
    )
    ap.add_argument("infile", help="Raw drone video file with telemetry data")
    ap.add_argument("-i", "--interactive", help="Run interactively",
                    action="store_true", required=False)
    ap.add_argument("-f", "--format", help="Output format", choices=["graph", "csv", "json"], default="graph", required=False)
    ap.add_argument("-o", "--output", help="Output location", required=False)
    args = ap.parse_args()

    # Handle text-only formats not being interactive
    if args.format in ["csv", "json"] and args.interactive:
        print("Interactive mode can not be used with text-based output formats")
        return 1

    # Handle non-interactive with no output
    if not args.interactive and not args.output:
        print("If not running in interactive mode, an output file must be specified with -o")
        return 1
    
    
    


if __name__ == "__main__":
    sys.exit(main())
