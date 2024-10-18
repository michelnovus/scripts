from argparse import ArgumentParser, Namespace
from sys import argv
from os import getcwd
from pathlib import Path


def parse_args() -> Namespace:
    parser = ArgumentParser(
        prog=f"watermark",
        description="Stamps a watermark text on images.",
    )
    parser.add_argument(
        "files",
        metavar="file",
        type=lambda s: Path(s).resolve(),
        nargs="+",
        help="files to be stamped",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="DIR",
        help=f"output directory [default: {getcwd()}]",
        default=getcwd(),
        type=lambda s: Path(s).resolve(),
    )
    return parser.parse_args(argv[1:] if argv[1:] else ["-h"])
