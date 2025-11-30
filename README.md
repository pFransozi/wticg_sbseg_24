# Seleção de Características Multiobjetivo para Detecção de Malwares Android

Repositório de código do trabalho:

> **Seleção de Características Multiobjetivo para Detecção de Malwares Android**  
> Publicado no WTICG / SBSEG 2024.

O objetivo deste projeto é avaliar o impacto da seleção de características multiobjetivo (via NSGA-II) em um cenário de detecção de malware Android baseado em múltiplas visões (API calls, opcodes e permissões).  
O código aqui permite **reproduzir os principais experimentos** reportados no artigo.

---

## 1. Estrutura do repositório

```text
wticg_sbseg_24/
├── data/
│   ├── dumps/         # Dumps / matrizes de resultados do NSGA-II (versão compacta)
│   └── npy/           # Matrizes numpy já ordenadas (features x samples) para cada visão
│
├── experiments/       # Scripts principais de experimento (já em .py)
│   ├── 2.1_ml_apicalls_pca.py
│   ├── 2.2_ml_opcodes_pca.py
│   ├── 2.3_ml_permissions_pca.py
│   ├── 3.1_nsga2_voting_dt.py
│   ├── 3.2_nsga2_voting_knn.py
│   └── 3.3_nsga2_voting_rf.py
│
├── results/           # Figuras geradas (curvas ROC, frentes de Pareto, etc.)
│   ├── result_nsga2_voting_dt.png
│   ├── result_nsga2_voting_knn.png
│   ├── result_nsga2_voting_rf.png
│   ├── result_roc_apicalls_pca.png
│   ├── result_roc_opcodes_pca.png
│   └── result_roc_permissions_pca.png
│
├── src/
│   ├── paths.py                       # Centraliza todos os caminhos de dados/resultados
│   └── outros-arquivos-do-experimento/
│       ├── 1.1_download_apk_por_lista.py
│       ├── 1.1_download_apk.py
│       ├── 1.2_extracao_features.py
│       ├── 1.3_create_csv_apicalls.ipynb
│       ├── 1.3_create_csv_opcodes.ipynb
│       ├── 1.3_create_csv_perms.ipynb
│       ├── 1.4_normalizacao_pca_apicalls.ipynb
│       ├── 1.4_normalizacao_pca_opcodes.ipynb
│       ├── 1.4_normalizacao_pca_permissions.ipynb
│       └── ...
│
├── requirements.txt
├── CITATION.cff
├── LICENSE
└── README.md
```
## 2. Ambiente e instalação

1) Clone o repositório
git clone https://github.com/pFransozi/wticg_sbseg_24.git
cd wticg_sbseg_24
2) Crie um ambiente virtual (opcional, mas recomendado)
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
<!-- .venv\Scripts\activate         # Windows -->
3) Instale as dependências
pip install -r requirements.txt

## 3. Dados

O repositório não contém APKs nem os dados brutos do AndroZoo, apenas artefatos processados:

* Matrizes .npy com as features já normalizadas e ordenadas.
* Dumps compactos do NSGA-II (data/dumps/), suficientes para reconstruir as frentes de Pareto e os resultados reportados.
* As pipelines completas de download/extração/normalização estão documentadas em src/outros-arquivos-do-experimento/, mas foram pensadas principalmente para transparência e não para uso cotidiano.

Caso você deseje refazer todo o fluxo desde os APKs, será necessário:

1. Ter acesso ao AndroZoo (ou a um conjunto equivalente de APKs),
2. Ajustar as chaves/tokens de acesso nos scripts de download,
3. Executar na ordem:

      * 01* (download),
      * 02_extracao_features.py,
      * 03_create_csv_*,
      * 04_normalizacao_pca_*.

Para fins de reprodução dos resultados do artigo, não é necessário refazer essas etapas: os .npy e dumps já foram incluídos em versão enxuta.

## 4. Como reproduzir os experimentos

### 4.1. Classificação com PCA (sem seleção multiobjetivo)

Scripts da Seção 2.x do artigo: avaliação de classificadores em cada visão após redução via PCA.

``` bash
# 2.1 – API calls
python experiments/2.1_ml_apicalls_pca.py

# 2.2 – Opcodes
python experiments/2.2_ml_opcodes_pca.py

# 2.3 – Permissões
python experiments/2.3_ml_permissions_pca.py
```

Cada script:

* Carrega a matriz .npy correspondente (API, opcodes ou permissões),
* Divide em treino/teste,
* Treina os classificadores (por exemplo: DT, KNN, RF),
* Gera métricas (accuracy, precision, recall, F1, ROC AUC),
* Salva figuras de curvas ROC em results/.

Os nomes das figuras seguem o padrão:
* result_roc_apicalls_pca.png
* result_roc_opcodes_pca.png
* result_roc_permissions_pca.png


### 4.2. Seleção de características com NSGA-II + voto majoritário

Scripts da Seção 3.x do artigo: aplicação do NSGA-II para seleção de subconjuntos de atributos em cada visão, seguida de comitê (votação por maioria) entre os modelos.

``` bash
# 3.1 – Comitê com Decision Tree
python experiments/3.1_nsga2_voting_dt.py

# 3.2 – Comitê com KNN
python experiments/3.2_nsga2_voting_knn.py

# 3.3 – Comitê com Random Forest
python experiments/3.3_nsga2_voting_rf.py

```

Cada script:

* Carrega os dumps do NSGA-II a partir de data/dumps/,
* Reconstrói as frentes de Pareto e a seleção de subconjuntos de features,
* Avalia o desempenho dos classificadores em cada visão,
* Combina as visões via votação por maioria (multi-view),
* Gera:
    * figuras com frentes de Pareto e/ou resumo das soluções;
    * figuras de desempenho final em results/ (por exemplo, result_nsga2_voting_dt.png).

## 5. Organização dos caminhos (paths.py)

O arquivo src/paths.py centraliza os diretórios usados nos scripts.

``` bash
from src.paths import DATA_DIR, NPY_DIR, DUMPS_DIR, RESULTS_DIR

apicalls_path = NPY_DIR / "apicalls-x-pca-ordered.npy"
```

Caso você queira alterar a estrutura de diretórios (por exemplo, mover data/ para outro local), basta editar apenas paths.py, sem precisar mexer nos scripts em experiments/.

## 6. Citação

Se este código ou os resultados forem úteis para o seu trabalho, por favor cite o artigo original.
Você também pode usar as informações em CITATION.cff.

Exemplo (BibTeX genérico – ajuste de acordo com a publicação final):

``` bibtex
@inproceedings{Fransozi2024NSGAAndroid,
  author    = {Fransozi, Philipe and Geremias, Jhonatan and Viegas, Eduardo K. and Santin, Altair O.},
  title     = {Seleção de Características Multiobjetivo para Detecção de Malwares Android},
  booktitle = {Anais Estendidos do Simpósio Brasileiro de Segurança da Informação e de Sistemas Computacionais (SBSEG)},
  year      = {2024},
  publisher = {Sociedade Brasileira de Computação (SBC)},
  address   = {Porto Alegre, RS, Brasil},
  doi       = {10.5753/sbseg_estendido.2024.241836},
  url       = {https://doi.org/10.5753/sbseg_estendido.2024.241836}
}

```