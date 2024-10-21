from pathlib import Path
from sys import stderr
from os.path import splitext

from PIL.Image import Image

from .argparser import parse_args
from . import generator


WATERMARK_SUFFIX = "-watermark"


def main() -> None:
    args = parse_args()

    # ** Contiene tuplas de los archivos a procesar, el primer valor de la
    # *  tupla es el archivo de origen y el segundo es el archivo de destino.
    # *  El archivo de origen debe existir y el de destino no debe existir.
    files: list[tuple[Path, Path]] = []

    _outdir: Path = args.DIR
    _files: list[Path] = args.files
    for file in _files:
        name, ext = splitext(file.name)
        files.append((file, _outdir.joinpath(f"{name}{WATERMARK_SUFFIX}{ext}")))

    for src, dst in files:
        if not src.exists():
            print(f"Not exist {src}", file=stderr)
        if dst.exists():
            print(
                "A file with the same name already exists at the destination:",
                f"{dst}",
                file=stderr,
            )

    for src, dst in files:
        match args.POSITION:
            case "ALL":
                image = generator.generate_everywhere(
                    src,
                    args.text,
                    size=args.SIZE,
                    color=args.COLOR,
                    opacity=args.OPACITY,
                    rotation=args.ROTATION,
                )
                action(image, dst, args.NOT_SAVE, args.SHOW)
            case _:
                raise NotImplementedError


def action(image: Image, output: Path, notsave: bool, show: bool) -> None:
    if not notsave:
        image.save(output)
    if show:
        image.show()
