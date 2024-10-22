from argparse import ArgumentParser, Namespace
from sys import argv
from os import getcwd
from pathlib import Path
from re import match as regex_match

from .generator import Position


class _Default:
    """Default values of parse_args()."""

    OUT_DIR = Path(getcwd())
    TEXT_SIZE = 50
    POSITION = Position.ALL
    COLOR = (255, 255, 255)
    OPACITY = 127
    ROTATION = 30


class _Formatter:
    @staticmethod
    def file(value: str) -> Path:
        return Path(value).resolve()

    @staticmethod
    def positive_integer(value: str) -> int:
        return abs(int(value))

    @staticmethod
    def position(value: str) -> Position:
        return Position[value]

    @staticmethod
    def color(value: str) -> tuple[int, int, int]:
        color_match = regex_match(
            r"^#?([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})$", value
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

    @staticmethod
    def opacity(value: str) -> int:
        """Dado un valor de `level` entre 0 y 100 retorna el valor proporcional
        entre 0 y 255."""
        try:
            level = float(value)
        except:
            raise ValueError
        if not (0 <= level <= 100):
            raise ValueError
        return int(level * 255 // 100)


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
        nargs="+",
        help="file to be stamped",
        type=_Formatter.file,
    )
    parser.add_argument(
        "--output",
        dest="DIR",
        help=f"output directory [default: {_Default.OUT_DIR}]",
        type=_Formatter.file,
        default=_Default.OUT_DIR,
    )
    parser.add_argument(
        "--size",
        dest="SIZE",
        help=f"set text size (integer >= 0) [default: {_Default.TEXT_SIZE}]",
        type=_Formatter.positive_integer,
        default=_Default.TEXT_SIZE,
    )
    parser.add_argument(
        "--position",
        help=f"watermark position values: {{{', '.join([pos.name for pos in Position])}}} [default: {_Default.POSITION}]",
        dest="POSITION",
        type=_Formatter.position,
        default=_Default.POSITION,
    )
    parser.add_argument(
        "--color",
        dest="COLOR",
        help="set text color (a hex color value) [default: #FFFFFF]",
        type=_Formatter.color,
        default=_Default.COLOR,
    )
    parser.add_argument(
        "--opacity",
        dest="OPACITY",
        help=f"set opacity level (integer between 0 and 100) [default: 50]",
        type=_Formatter.opacity,
        default=_Default.OPACITY,
    )
    parser.add_argument(
        "--rotation",
        dest="ROTATION",
        help=f"set rotation angle [default: {_Default.ROTATION}]",
        type=_Formatter.positive_integer,
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
    parser.add_argument(
        "--dry-run",
        dest="DRY_RUN",
        help="no execute watermark generation",
        action="store_true",
    )
    return parser.parse_args(argv[1:] if argv[1:] else ["-h"])
