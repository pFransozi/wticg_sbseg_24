#!/usr/bin/env python
# coding: utf-8

# # Teste inicial

# ## Teste das dependências

# Na célula abaixo são importadas todas as dependências utilizadas na reprodução do experimento. Caso alguma das dependências não seja encontrada, revisar a seção [Instalação das dependências](../README.md#instalação-das-dependências) no arquivo README.

# In[1]:


import pandas
import numpy
import matplotlib.pyplot
import pickle
from time import time

from sklearn.model_selection import train_test_split

from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (roc_curve, roc_auc_score)

from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.problem import ElementwiseProblem
from pymoo.optimize import minimize
from pymoo.operators.sampling.rnd import FloatRandomSampling
from matplotlib.ticker import StrMethodFormatter


# Na celula abaixo é feita a verificação de se os arquivos necessários para reprodução do experimento estão disponíveis. Caso nenhuma mensagem de erro seja apresentada, todos os arquivos foram encontrados. Caso contrário, há duas situações:
# 
# * Caso seja algum arquivo com extensão `*.ipynb`, o arquivo deve ser obtido no repositório do artigo;
# * Caso seja algum arquivo do diretório `dumps` ou `npy`, verificar no README a seção [Download de arquivos](../README.md#download-de-arquivos).

# In[2]:


from pathlib import Path

files_to_check = ['../dumps/nsga2-maj-vot-dt.pkl'
                    , '../dumps/nsga2-maj-vot-knn.pkl'
                    , '../dumps/nsga2-maj-vot-rf.pkl'
                    , '../npy/apicalls-x-pca-ordered.npy'
                    , '../npy/apicalls-y-full-ordered.npy'
                    , '../npy/opcodes-x-pca-ordered.npy'
                    , '../npy/opcodes-y-full-ordered.npy'
                    , '../npy/perm-x-pca-ordered.npy'
                    , '../npy/perm-y-full-ordered.npy'
                    , './para-reproducao-experimento/2.1.ml_apicalls_pca.ipynb'
                    , './para-reproducao-experimento/2.2.ml_opcodes_pca.ipynb'
                    , './para-reproducao-experimento/2.3.ml_permissions_pca.ipynb'
                    , './para-reproducao-experimento/3.1.nsga2-voting-dt.ipynb'
                    , './para-reproducao-experimento/3.2.nsga2-voting-knn.ipynb'
                    , './para-reproducao-experimento/3.3.nsga2-voting-rf.ipynb']

for file in files_to_check:
    if not Path(file).is_file():
        print(f"Erro: O arquivo '{file}' não existe.")
                    

