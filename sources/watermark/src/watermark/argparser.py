from argparse import ArgumentParser, Namespace
from sys import argv
from os import getcwd
from pathlib import Path
from re import match as regex_match

# POSITION_VALUES = ("ALL", "CENTER", "N", "S", "E", "W", "NE", "SE", "SW", "NW")
POSITION_VALUES = ("ALL",)


class _Default(object):
    """Default values of parse_args()."""

    OUT_DIR = getcwd()
    TEXT_SIZE = 50
    POSITION = POSITION_VALUES[0]
    COLOR = (255, 255, 255)
    OPACITY = 127
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
        help=f"watermark position values: {{{', '.join(POSITION_VALUES)}}} [default: {_Default.POSITION}]",
        dest="POSITION",
        type=_position_parser,
        default=_Default.POSITION,
    )
    parser.add_argument(
        "--color",
        dest="COLOR",
        help="set text color (a hex color value) [default: #FFFFFF]",
        type=_color_parser,
        default=_Default.COLOR,
    )
    parser.add_argument(
        "--opacity",
        dest="OPACITY",
        help=f"set opacity level (integer between 0 and 100) [default: 50]",
        type=_opacity_level,
        default=_Default.OPACITY,
    )
    parser.add_argument(
        "--rotation",
        dest="ROTATION",
        help=f"set rotation angle [default: {_Default.ROTATION}]",
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
        dest="NOT_SAVE",
        help="do not save a file in output, use it with --show",
        action="store_true",
    )
    return parser.parse_args(argv[1:] if argv[1:] else ["-h"])


def _opacity_level(level: str) -> int:
    """Dado un valor de `level` entre 0 y 100 retorna el valor proporcional
    entre 0 y 255."""
    try:
        value = float(level)
    except:
        raise ValueError
    if not (0 <= value <= 100):
        raise ValueError
    return int(value * 255 // 100)


def _color_parser(color: str) -> tuple[int, int, int]:
    color_match = regex_match(
        r"^#?([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})$", color
    )
    if color_match is None:
        raise ValueError
    else:
        r, g, b = (
            color_match.group(1),
            color_match.group(2),
            color_match.group(3),
        )
        return (int(r, base=16), int(g, base=16), int(b, base=16))


def _position_parser(value: str) -> str:
    value = value.upper()
    if value in POSITION_VALUES:
        return value
    else:
        raise ValueError
