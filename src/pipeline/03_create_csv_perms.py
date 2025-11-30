#!/usr/bin/env python
# coding: utf-8

# ### Apresentação

# Este notebook carrega os arquivos de cada APK que contêm as características da view PERMISSIONS, gerando um único CSV.
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
     sys.path.insert(0, str(SRC_DIR))

from paths import FEATURES_DIR, CSV_DIR


# In[2]:


ray.shutdown()
os.environ["MODIN_ENGINE"] = "ray"

runtime_env = {
    'env_vars': {
        "RAY_memory_monitor_refresh_ms": "100",
        "RAY_memory_usage_threshold": "0.85"
     }
}
ray.init(runtime_env=runtime_env)


# In[3]:


def is_valid_file(file_name, file_type):
    return file_name.endswith(file_type)

def is_permission_file(file_name):
    return is_valid_file(file_name, "-analysis-permissions.csv")

def is_apicall_file(file_name):
    return is_valid_file(file_name, "-analysis-apicalls.csv")

def is_opcode_file(file_name):
    return is_valid_file(file_name, "-analysis-opcodes.csv")


# In[4]:


files = sorted(os.scandir(FEATURES_DIR), key=lambda e: e.name)
count = 0
total_files = len(files)


# In[ ]:


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
            df_tmp = mpd.read_csv(file.path)
            df_tmp['file_name'] = file.name.split('-')[0]
            permission_df_list_tmp.append(df_tmp)
        elif is_apicall_file(file.name):
             continue
        elif is_opcode_file(file.name):
             continue

        if len(permission_df_list_tmp) == 6000:
            print('Concatenando lote')
            permission_df_list.append(mpd.concat(permission_df_list_tmp, ignore_index=True))
            
            permission_df_list_tmp = []




if len(permission_df_list_tmp) > 0:
    print('Concatenando resto permission')
    permission_df_list.append(mpd.concat(permission_df_list_tmp, ignore_index=True))
    permission_df_list_tmp = []

id = str(uuid.uuid4())
            
print('Concateo final permission')
df_permissions = mpd.concat(permission_df_list, ignore_index=True)
print('Salvando permissions')
df_permissions.to_csv(CSV_DIR / f"PERMISSIONS-{id}.csv")

