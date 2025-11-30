#!/usr/bin/env python
# coding: utf-8

"""
Gera o CSV de APICALLS em blocos, evitando vários notebooks quase iguais.

Lê todos os arquivos `*-analysis-apicalls.csv` do diretório de features,
escreve arquivos parciais e, por padrão, concatena em um CSV final.
Use `--no-merge` se preferir apenas os parciais.
"""

import argparse
import shutil
from itertools import islice
from pathlib import Path
import sys

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from paths import FEATURES_DIR, CSV_DIR


def chunked(iterable, size):
    it = iter(iterable)
    while True:
        batch = list(islice(it, size))
        if not batch:
            break
        yield batch


def read_apicall_files(file_paths):
    frames = []
    for path in file_paths:
        df = pd.read_csv(path)
        df["file_name"] = Path(path).name.split("-")[0]
        frames.append(df)
    return pd.concat(frames, ignore_index=True)


def write_part(files_batch, out_dir, part_index):
    part_path = out_dir / f"APICALLS-part-{part_index:03d}.csv"
    df = read_apicall_files(files_batch)
    df.to_csv(part_path, index=False)
    return part_path


def merge_parts(part_paths, final_path):
    if not part_paths:
        return

    header_written = False
    with final_path.open("w", newline="") as out_file:
        for path in part_paths:
            with path.open("r", newline="") as in_file:
                if header_written:
                    next(in_file)  # skip header
                else:
                    header_written = True
                shutil.copyfileobj(in_file, out_file)


def parse_args():
    parser = argparse.ArgumentParser(description="Gera CSV de APICALLS em blocos.")
    parser.add_argument(
        "--features-dir",
        type=Path,
        default=FEATURES_DIR,
        help="Diretório onde estão os arquivos *-analysis-apicalls.csv.",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=CSV_DIR,
        help="Diretório para salvar os CSVs parciais/final.",
    )
    parser.add_argument(
        "--files-per-chunk",
        type=int,
        default=15000,
        help="Quantidade de arquivos de apicalls por bloco.",
    )
    parser.add_argument(
        "--pattern",
        default="*-analysis-apicalls.csv",
        help="Padrão glob para encontrar arquivos de apicalls.",
    )
    parser.add_argument(
        "--no-merge",
        action="store_true",
        help="Não gerar o CSV final, apenas os parciais.",
    )
    parser.add_argument(
        "--output-name",
        default="APICALLS-completo.csv",
        help="Nome do CSV final (quando merge estiver habilitado).",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    features_dir = args.features_dir
    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(features_dir.glob(args.pattern))
    if not files:
        print(f"Nenhum arquivo encontrado com padrão {args.pattern} em {features_dir}")
        sys.exit(1)

    part_paths = []
    for idx, batch in enumerate(chunked(files, args.files_per_chunk), start=1):
        print(f"Lendo bloco {idx}: {len(batch)} arquivos")
        part_path = write_part(batch, out_dir, idx)
        part_paths.append(part_path)
        print(f"Bloco salvo em {part_path}")

    if not args.no_merge:
        final_path = out_dir / args.output_name
        print(f"Concatenando {len(part_paths)} partes em {final_path}")
        merge_parts(part_paths, final_path)
        print("Concluído.")
    else:
        print("Merge final pulado (--no-merge).")


if __name__ == "__main__":
    main()
