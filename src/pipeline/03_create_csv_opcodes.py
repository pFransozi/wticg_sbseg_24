#!/usr/bin/env python
# coding: utf-8

# ### Apresentação
# Este notebook carrega os arquivos de cada APK que contêm as características da view OPCODES, gerando um único CSV.
# Cada linha representa uma APK.
# Cada coluna representa uma característica.
# 
# Os arquivos são lidos em ordem alfabetica para que cada linha dos três CSV represente o mesmo APK.

import uuid
import pandas as pd
import modin.pandas as mpd
import ray
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
     sys.path.insert(0, SRC_DIR)

from paths import FEATURES_DIR, CSV_DIR


os.environ["MODIN_ENGINE"] = "ray"

runtime_env = {
    'env_vars': {
        "RAY_memory_monitor_refresh_ms": "100",
        "RAY_memory_usage_threshold": "0.85"
     }
}
ray.init(runtime_env=runtime_env)


def is_valid_file(file_name, file_type):
    return file_name.endswith(file_type)

def is_permission_file(file_name):
    return is_valid_file(file_name, "-analysis-permissions.csv")

def is_apicall_file(file_name):
    return is_valid_file(file_name, "-analysis-apicalls.csv")

def is_opcode_file(file_name):
    return is_valid_file(file_name, "-analysis-opcodes.csv")


files = sorted(os.scandir(FEATURES_DIR), key=lambda e: e.name)
count = 0
total_files = len(files)


permission_df_list_tmp = []
permission_df_list = []
apicall_df_list_tmp = []
apicall_df_list = []
opcode_df_list_tmp = []
opcode_df_list = []

count = 0

df_opcodes = mpd.DataFrame()
df_permissions = mpd.DataFrame()
df_apicalls = mpd.DataFrame()

for file in files:
        count = count + 1
        
        print(chr(27) + "[2J")
        print(f"{count}/{total_files}")

        if is_permission_file(file.name):
             continue
        elif is_apicall_file(file.name):
             continue
        elif is_opcode_file(file.name):
            df_tmp = mpd.read_csv(file.path)
            df_tmp['file_name'] = file.name.split('-')[0]
            opcode_df_list_tmp.append(df_tmp)

        if len(opcode_df_list_tmp) == 6000:
            print('Concatenando lote')
            opcode_df_list.append(mpd.concat(opcode_df_list_tmp, ignore_index=True))
            
            opcode_df_list_tmp = []




if len(opcode_df_list_tmp) > 0:
    print('Concatenando resto opcodes')
    opcode_df_list.append(mpd.concat(opcode_df_list_tmp, ignore_index=True))
    opcode_df_list_tmp = []

id = str(uuid.uuid4())
            
print('Concateo final opcodes')
df_opcodes = mpd.concat(opcode_df_list, ignore_index=True)
print('Salvando opcodes')
df_opcodes.to_csv(CSV_DIR / f"OPCODES-{id}.csv")

