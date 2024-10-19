from argparse import ArgumentParser, Namespace
from sys import argv
from os import getcwd
from pathlib import Path

from defines import Position, Color


class _Default(object):
    """Default values of parse_args()."""

    OUT_DIR = getcwd()
    TEXT_SIZE = 40
    POSITION = Position.CENTER
    COLOR = Color("#212121")
    OPACITY = 0
    ROTATION = 30


def parse_args() -> Namespace:
    """Parses argument passed to application from stdin."""
    parser = ArgumentParser(
        prog=f"watermark",
        description="Stamps a watermark text on images.",
    )
    parser.add_argument(
        "text",
        help="stamp these text into image",
    )
    parser.add_argument(
        "files",
        metavar="file",
        type=lambda s: Path(s).resolve(),
        nargs="+",
        help="file to be stamped",
    )
    parser.add_argument(
        "--output",
        dest="DIR",
        help=f"output directory [default: {_Default.OUT_DIR}]",
        default=_Default.OUT_DIR,
        type=lambda s: Path(s).resolve(),
    )
    parser.add_argument(
        "--size",
        dest="SIZE",
        help=f"set text size (integer >= 0) [default: {_Default.TEXT_SIZE}]",
        type=lambda i: abs(int(i)),
        default=_Default.TEXT_SIZE,
    )
    parser.add_argument(
        "--position",
        help=f"watermark position values: {{{', '.join((p.name for p in Position))}}} [default: {_Default.POSITION.name}]",
        dest="POSITION",
        type=_position_enum_parser,
        default=_Default.POSITION,
    )
    parser.add_argument(
        "--color",
        dest="COLOR",
        help=f"set text color (a hex color value) [default: {_Default.COLOR}]",
        type=Color,
        default=_Default.COLOR,
    )
    parser.add_argument(
        "--opacity",
        dest="OPACITY",
        help=f"set opacity level (integer >= 0) [default: {_Default.OPACITY}]",
        type=lambda i: abs(int(i)),
        default=_Default.OPACITY,
    )
    parser.add_argument(
        "--rotation",
        dest="ROTATION",
        help=f"set rotation angle (integer between 0 and (+/-)90) [default: {_Default.ROTATION}]",
        type=lambda i: abs(int(i)),
        default=_Default.ROTATION,
    )
    parser.add_argument(
        "--show",
        dest="SHOW",
        help="launch the system image viewer with output image",
        action="store_true",
    )
    parser.add_argument(
        "--no-save",
        dest="NO_SAVE",
        help="do not save a file in output, use it with --show",
        action="store_true",
    )
    return parser.parse_args(argv[1:] if argv[1:] else ["-h"])


def _position_enum_parser(pos: str) -> Position:
    values = [p.name for p in Position]
    pos = pos.upper()
    if pos in values:
        return Position[pos]
    else:
        raise ValueError
