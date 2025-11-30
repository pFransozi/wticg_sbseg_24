import sys
import argparse
import os
import sys
from pathlib import Path
import pandas as pd
import threading

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from paths import APKS_DIR, LOGS_DIR, FEATURES_DIR


# Este script extrai as três views utilizadas em nossa pesquisa. As views são: opcodes, apicalls, permissões. 
# Essas views são extraídas dos arquivos de features resultantes do processo de extração da ferramenta AndroidPyTool
#
#


def get_goodware_class():
    return 0

def get_malware_class():
    return 1

def get_filename(filename, suffix, extension):
    return f"{filename}-{suffix}.{extension}"

def get_filename_opcode_csv(base_filename):
    return get_filename(base_filename, "analysis-opcodes", "csv")

def get_filename_apicall_csv(base_filename):
    return get_filename(base_filename, "analysis-apicalls", "csv")

def get_filename_permission_csv(base_filename):
    return get_filename(base_filename, "analysis-permissions", "csv")

def is_valid_file_json(file):
    return file.is_file() and file.name.endswith('json')

def is_valid_file(file_name, file_type):
    return file_name.endswith(file_type)

def generate_permission_dict(json_permission):
    perm_dict = {}

    for permission in json_permission:

        if permission not in perm_dict:
            perm_dict[permission] = 1
        else:
            perm_dict[permission] = perm_dict[permission] + 1

    return perm_dict


# Recebe uma lista de features de apk, resultado do AndroPyTool.abs
# Para cada arquivo de feature, outros três são gerados:
# analysis-opcodes.csv -> armazena as características opcodes de uma apk;
# analysis-apicalls -> armazena as características apicalls de uma apk;
# analysis-permissions -> armazena as características permissions de uma apk;
def process_features(output_csv, apk_features_list):

    for apk_info in apk_features_list:

        filename_base = str(os.path.basename(apk_info["file_abs_path"])).split("-")[0]

        try:
            pd_json = pd.read_json(apk_info["file_abs_path"])

            dfs_opcodes = pd.DataFrame(pd_json["Static_analysis"]["Opcodes"], index=[0])
            dfs_opcodes["class"] = apk_info["class"]
            dfs_opcodes.to_csv(os.path.join(output_csv, get_filename_opcode_csv(filename_base)))

            dfs_apicalls = pd.DataFrame(pd_json["Static_analysis"]["API calls"], index=[0])
            dfs_apicalls["class"] = apk_info["class"]
            dfs_apicalls.to_csv(os.path.join(output_csv, get_filename_apicall_csv(filename_base)))

            dfs_permissions = pd.DataFrame(generate_permission_dict(pd_json["Static_analysis"]["Permissions"]), index=[0])
            dfs_permissions["class"] = apk_info["class"]
            dfs_permissions.to_csv(os.path.join(output_csv, get_filename_permission_csv(filename_base)))
        
        except Exception as e:
            print(f"APK: {filename_base}; Error: {e}")
            continue

def process_apks(apk_features_list, output_csv, chunk_size):
    
    threads = []

    for i in range(0, len(apk_features_list), chunk_size):
        threads.append(threading.Thread(target=process_features, args=(output_csv, apk_features_list[i:i+chunk_size])))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

def load_json_malware(input_dir):
    return load_json(input_dir, get_malware_class())

def load_json_goodware(input_dir):
    return load_json(input_dir, get_goodware_class())

def load_json(input_dir, classification):
    apk_features_list = []
    
    with os.scandir(input_dir) as files:
        for file in files:
            if is_valid_file_json(file):
                apk_features_list.append({"file_abs_path": os.path.abspath(file.path), "class":classification})

    return apk_features_list

def load_apks_list(input_malware, input_goodware):
    apk_features_list = []
    
    apk_features_list = load_json_malware(input_malware) if input_malware else []
    apk_features_list += load_json_goodware(input_goodware) if input_goodware else []

    return apk_features_list


def main():

    dir_output = FEATURES_DIR
    dir_goodware = APKS_DIR/"goodware/Features_files/" # diretório onde AndroPyTool exporta as features de cada APKS;
    dir_malware = APKS_DIR/"malware/Features_files"    # diretório onde AndroPyTool exporta as features de cada APKS;
    chuck_size = 250


    apk_features_list = load_apks_list(input_goodware=dir_goodware, input_malware=dir_malware)
    process_apks(apk_features_list, dir_output, chuck_size)


if __name__ == "__main__":
    main()