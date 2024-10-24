# [MIT License] Copyright (c) 2024 Michel Novus
# Rebaptizer es un script para renombrar archivos rapidamente con regex.
#
# Dependencias:
#   - `colorama`: https://github.com/tartley/colorama

from pathlib import Path
import importlib.metadata 
import os
import os.path
import re
import sys
import argparse

try:
    from colorama import Fore, Style
except ModuleNotFoundError:
    print("Error: Módulo `colorama` no existe!", file=sys.stderr)
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "Regex",
        help="Patrón Regex que debe coincidir con los nombres de los archivos \
            buscados. Coloca dentro los grupos `(?P<C>\\d+)` y `(?P<S>\\d+)` para \
            indicar la posición de número de capitulo (obligatorio) y \
            temporada (opcional) respectivamente.",
    )
    parser.add_argument(
        "-o",
        "--new-name",
        required=True,
        help="Nuevo nombre de los archivos. \
            Coloca los placeholder `$S` (para temporada) y `$C` (para capitulo) \
            en el nuevo nombre para indicar la posicion del número si corresponde",
    )
    parser.add_argument("-p", "--path", help="Path to change filenames")
    metadata = importlib.metadata.metadata("rebaptizer")
    parser.add_argument(
        "--version", action="version", version=f"{metadata['Name']} {metadata['Version']}"
    )
    args = parser.parse_args()

    ## Constantes del programa.
    ## Indica que patrón debe coincidir con los nombres de los archivos.
    PATTERN = rf"{args.Regex}"
    ## Está o no presente el valor de temporada.
    SEASON_GROUP = True if PATTERN.find("(?P<S>\\d+)") != -1 else False
    ## Función de formateo del nuevo nombre del archivo.
    FORMAT = lambda season, chapter: args.new_name.replace("$S", season).replace(
        "$C", chapter
    )
    ## Directorio objetivo.
    DIRECTORY = Path(args.path if args.path is not None else os.getcwd())

    print(
        f"{Style.BRIGHT}:: Se procesará en el directorio:{Style.RESET_ALL}",
        f"{Fore.YELLOW}{DIRECTORY}{Fore.RESET}",
        file=sys.stderr,
    )
    print(
        f"   {Style.BRIGHT}¿continuar?{Style.RESET_ALL}",
        f"[{Style.BRIGHT}{Fore.GREEN}Y{Fore.RESET}{Style.RESET_ALL}\
    /{Fore.LIGHTRED_EX}n{Fore.RESET}] ",
        end="",
        flush=True,
        file=sys.stderr,
    )
    if input() not in ("y", "Y", ""):
        print(f"[{Fore.LIGHTRED_EX}cancelado{Fore.RESET}]", file=sys.stderr)
        sys.exit(1)

    files: list[Path] = []
    for dirpath, _, filenames in os.walk(DIRECTORY):
        for filename in filenames:
            if filename != sys.argv[0]:
                files.append(Path(os.path.join(dirpath, filename)))
    files.sort()

    rename_files: list[tuple[Path, Path]] = []
    regex = re.compile(PATTERN)
    for file in files:
        re_match = regex.match(str(file.name))
        if re_match is not None:
            if SEASON_GROUP:
                season_num = re_match.group("S")
            else:
                season_num = "?"
            chapter_num = f"{re_match.group('C').zfill(2)}"
            new_name = FORMAT(season_num, chapter_num)
            rename_tuple = (file, file.parent.joinpath(new_name))
            rename_files.append(rename_tuple)

    print(file=sys.stderr)
    print("-" * 80, file=sys.stderr)
    for old_f, new_f in rename_files:
        print(
            f"{Fore.LIGHTYELLOW_EX}{os.path.basename(old_f)}{Fore.RESET}\
    {Style.BRIGHT}  >>  {Style.RESET_ALL}\
    {Fore.GREEN}{os.path.basename(new_f)}{Fore.RESET}",
            file=sys.stderr,
        )

    print("-" * 80, file=sys.stderr)
    print(file=sys.stderr)
    print(
        f"{Style.BRIGHT}\
    :: Se renombraran los archivos listados arriba.{Style.RESET_ALL}",
        file=sys.stderr,
    )
    print(
        f"   {Style.BRIGHT}¿continuar?{Style.RESET_ALL}",
        f"[{Style.BRIGHT}{Fore.GREEN}Y{Fore.RESET}{Style.RESET_ALL}\
    /{Fore.LIGHTRED_EX}n{Fore.RESET}] ",
        end="",
        flush=True,
        file=sys.stderr,
    )
    if input() not in ("y", "Y", ""):
        print(f"[{Fore.LIGHTRED_EX}cancelado{Fore.RESET}]", file=sys.stderr)
        sys.exit(1)
    for old, new in rename_files:
        old.rename(new)
    print(f"[{Fore.GREEN}completado!{Fore.RESET}]", file=sys.stderr)
