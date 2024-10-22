from pathlib import Path
from sys import stderr
from os.path import splitext
import time

from tqdm import tqdm

from .argparser import parse_args
from .generator import Watermark


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

    watermark = Watermark(
        args.text,
        position=args.POSITION,
        size=args.SIZE,
        color=args.COLOR,
        opacity=args.OPACITY,
        rotation=args.ROTATION,
    )

    it = tqdm(files) if len(files) > 1 else files
    msg = f"{len(files)} files" if len(files) > 1 else f'"{files[0][0]}"'
    print(f":: Stamping {msg}.", file=stderr)
    for src_file, dst_file in it:

        # if type(it) == type(list):
        #     it.set_description(str(src_file.name))  # type: ignore

        if args.DRY_RUN:
            time.sleep(0.33)
            continue

        image = watermark.generate(src_file)
        if not args.NOT_SAVE:
            image.save(dst_file)
        if args.SHOW:
            image.show()
