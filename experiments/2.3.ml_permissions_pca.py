#!/usr/bin/env python
# coding: utf-8

# ### Apresentação
# Este arquivo faz a classificação de malware para Android utilizando a *view* permissões, sem seleção de características. O resultado final deste *notebook* mostra os resultados utilizados no artigo.
# ### Inicialização
# Inicializa todas as bibliotecas utilizadas neste notebook.

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

from sklearn.model_selection import train_test_split

from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import ( roc_curve, roc_auc_score)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from paths import NPY_DIR, RESULTS_DIR

OUTPUT_FILE = RESULTS_DIR / "result_roc_permissions_pca.png"
RANDOM_STATE = 42
TRAIN_SIZE = 0.7

def load_data():
    apicalls_y_path = NPY_DIR / "perm-y-full-ordered.npz"
    apicalls_x_path = NPY_DIR / "perm-x-pca-ordered.npz"

    exists_apicalls_y = os.path.exists(apicalls_y_path)
    exists_apicalls_x = os.path.exists(apicalls_x_path)

    missing_files = []

    if not exists_apicalls_y:
        missing_files.append(apicalls_y_path)

    if not exists_apicalls_x:
        missing_files.append(apicalls_x_path)


    if missing_files:
        missing_files_str = " e ".join(missing_files)
        print(f"O(s) arquivo(s) {missing_files_str} não existe(m) no diretório esperado. \nLeia o arquivo README, seção Download de arquivos.")
        sys.exit("Interrompendo a execução do notebook.")


    y = np.load(open(apicalls_y_path, "rb"))['y']
    X = np.load(open(apicalls_x_path, "rb"))['x']

    return X, y

def run_experiment():

    X, y = load_data()
    x_train, x_test, y_train, y_test = train_test_split(X, y, train_size=TRAIN_SIZE, random_state=RANDOM_STATE)


    # ### Treino e teste
    # Treina e testa os classificadores RF, DT, kNN;

    rf = RandomForestClassifier(n_estimators=100, random_state=RANDOM_STATE, n_jobs=-1)
    rf.fit(x_train, y_train)

    dt = DecisionTreeClassifier(min_samples_split=100, random_state=42)
    dt.fit(x_train, y_train)

    knn = KNeighborsClassifier(n_neighbors=100, n_jobs=-1)
    knn.fit(x_train, y_train)


    # ### Métricas
    # #### RF

    rf_y_test_predict_proba = rf.predict_proba(x_test)
    rf_fpr, rf_tpr, rf_threshold = roc_curve(y_test, rf_y_test_predict_proba[:,1], pos_label=1)
    rf_auc = roc_auc_score(y_test, rf_y_test_predict_proba[:,1])

    # #### DT
    dt_y_test_predict_proba = dt.predict_proba(x_test)
    dt_fpr, dt_tpr, dt_threshold = roc_curve(y_test, dt_y_test_predict_proba[:,1], pos_label=1)
    dt_auc = roc_auc_score(y_test, dt_y_test_predict_proba[:,1])
    # #### kNN
    knn_y_test_predict_proba = knn.predict_proba(x_test)
    knn_fpr, knn_tpr, knn_threshold = roc_curve(y_test, knn_y_test_predict_proba[:,1], pos_label=1)
    knn_auc = roc_auc_score(y_test, knn_y_test_predict_proba[:,1])


    # ### Resultado
    plt.figure(figsize=(7, 7))
    plt.plot(dt_fpr, dt_tpr,label=f"DT ({round(dt_auc,2)})",linewidth=4, linestyle='dashed')
    plt.plot(rf_fpr, rf_tpr,label=f"RF ({round(rf_auc,2)})",linewidth=4, linestyle='solid')
    plt.plot(knn_fpr, knn_tpr,label=f"kNN ({round(knn_auc,2)})",linewidth=4, linestyle='dotted')
    plt.legend(frameon=False, loc=4)
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Taxa de Falso Positivo')
    plt.ylabel('Taxa de Verdadeiro Positivo')
    plt.savefig(OUTPUT_FILE)

def main():
    run_experiment()

if __name__ == "__main__":
    main()
