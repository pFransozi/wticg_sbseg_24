#!/usr/bin/env python
# coding: utf-8

# ### Apresentação

# * Carrega o CSV
# * Deleta colunas não necessárias
# * Extrai coluna class e a exclui
# * O dataframe da coluna class (y) e o dataframe das características (x) são transformados para to_numpy;
# * Aplica PCA na matrix com as características
# 
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from paths import CSV_DIR, NPY_DIR

def run():

    opcodes = pd.read_csv(CSV_DIR/"OPCODES.csv")

    opcodes = opcodes.fillna(0)
    opcodes = opcodes.drop(["Unnamed: 0.1", "Unnamed: 0"], axis=1)
    opcodes = opcodes.drop('file_name', axis=1)


    y = np.array(opcodes["class"])
    opcodes = opcodes.drop('class', axis=1)
    x = opcodes.to_numpy(na_value=0)

    pca = PCA(n_components=100, random_state=42)
    x_pca = pca.fit_transform(x)


    np.savez(NPY_DIR/"opcodes-x-pca-ordered.npy", x=x_pca)
    np.savez(NPY_DIR/"opcodes-y-full-ordered.npy", y=y)

def main():
    run()

if __name__ == "__main__":
    main()

