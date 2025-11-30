import os
import sys
import requests
import threading
import time
from queue import Queue
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from paths import APKS_DIR, LOGS_DIR

# API key para o download
APIKEY = ""

# Caminhos para os arquivos de hash
GOODWARE_FILE = APKS_DIR / "0.lista-apk-goodware.txt"
MALWARE_FILE = APKS_DIR/"0.lista-apk-malware.txt"

# Diretórios de destino
GOODWARE_DIR = APKS_DIR/"goodware/"
MALWARE_DIR = APKS_DIR/"malware/"

# Arquivo de log para erros
LOG_FILE = LOGS_DIR / "download_errors.log"

# Número de tentativas
RETRY_LIMIT = 5

# Delay entre solicitações em segundos
REQUEST_DELAY = 10

# Tempo limite para a resposta do servidor em segundos
TIMEOUT = 120

# Número de threads a serem usadas
NUM_THREADS = 10

# Criar diretórios de destino se não existirem
os.makedirs(GOODWARE_DIR, exist_ok=True)
os.makedirs(MALWARE_DIR, exist_ok=True)

# Limpar arquivo de log anterior, se existir
with open(LOG_FILE, 'w') as log_file:
    log_file.write('')

# Função para verificar se o arquivo já existe
def file_exists(dest_dir, sha256):
    for filename in os.listdir(dest_dir):
        if sha256 in filename:
            return True
    return False

# Função para fazer o download
def download_apk(sha256, dest_dir):
    if file_exists(dest_dir, sha256):
        print(f"O arquivo com hash {sha256} já foi baixado.")
        return
    
    url = f"https://androzoo.uni.lu/api/download?apikey={APIKEY}&sha256={sha256}"
    attempt = 1
    success = False

    while attempt <= RETRY_LIMIT:
        print(f"Tentativa {attempt} para baixar APK com hash: {sha256}")
        try:
            response = requests.get(url, stream=True, timeout=TIMEOUT)
            if response.status_code == 200:
                content_disposition = response.headers.get('Content-Disposition')
                if content_disposition and 'filename=' in content_disposition:
                    filename = content_disposition.split('filename=')[1].strip('"')
                else:
                    filename = sha256 + '.apk'
                
                filepath = os.path.join(dest_dir, filename)

                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)

                print(f"Arquivo salvo como: {filepath}")
                success = True
                break
            else:
                print(f"Erro ao baixar o APK com hash: {sha256} na tentativa {attempt}")
                print(f"Erro: {response.status_code} {response.text}")

        except requests.RequestException as e:
            print(f"Erro ao baixar o APK com hash: {sha256} na tentativa {attempt}")
            print(f"Erro: {e}")

        attempt += 1
        time.sleep(REQUEST_DELAY)

    if not success:
        with open(LOG_FILE, 'a') as log_file:
            log_file.write(f"{sha256}\n")

# Função que será executada em cada thread
def worker(queue):
    while not queue.empty():
        sha256, dest_dir = queue.get()
        if sha256:
            download_apk(sha256, dest_dir)
        queue.task_done()

# Função para ler hashes e enfileirá-los para download
def process_files(goodware_file, malware_file, num_threads):
    queue = Queue()

    with open(goodware_file, 'r') as gf, open(malware_file, 'r') as mf:
        goodware_lines = gf.readlines()
        malware_lines = mf.readlines()

    max_length = max(len(goodware_lines), len(malware_lines))
    for i in range(max_length):
        if i < len(goodware_lines):
            sha256 = goodware_lines[i].strip()
            if sha256:
                queue.put((sha256, GOODWARE_DIR))
        if i < len(malware_lines):
            sha256 = malware_lines[i].strip()
            if sha256:
                queue.put((sha256, MALWARE_DIR))

    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=worker, args=(queue,))
        thread.start()
        threads.append(thread)

    queue.join()

    for thread in threads:
        thread.join()

# Processar arquivos
process_files(GOODWARE_FILE, MALWARE_FILE, NUM_THREADS)
