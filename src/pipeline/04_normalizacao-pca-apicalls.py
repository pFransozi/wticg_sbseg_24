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
import modin.pandas as mpd
import os
import sys
from pathlib import Path
import ray
from sklearn.decomposition import PCA

PROJECT_ROOT = Path(__file__).resolve().parents()
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from paths import CSV_DIR, NPY_DIR


def config():

    os.environ["MODIN_ENGINE"] = "ray"

    runtime_env = {
        'env_vars': {
            "RAY_memory_monitor_refresh_ms": "100",
            "RAY_memory_usage_threshold": "0.85"
        }
    }
    ray.init(runtime_env=runtime_env)

def run():

    api = mpd.read_csv(CSV_DIR/"APICALLS.csv")

    api = api.fillna(0)
    api = api.drop(["Unnamed: 0.4", "Unnamed: 0.3", "Unnamed: 0.2", "Unnamed: 0.1", "Unnamed: 0"], axis=1)

    y = np.array(api["class"])
    api = api.drop('class', axis=1)
    x = api.to_numpy(na_value=0)


    pca = PCA(n_components=100, random_state=42)
    x_pca = pca.fit_transform(x)

    np.savez(NPY_DIR/"apicalls-x-pca-ordered.npy", x=x_pca)
    np.savez(NPY_DIR/"apicalls-y-full-ordered.npy", y=y)

def main():
    config()
    run()

if __name__ == "__main__":
    main()
    

