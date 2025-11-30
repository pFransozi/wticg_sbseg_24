from subprocess import run
from pathlib import Path
import sys

SCRIPTS = [
    "2.1.ml_apicalls_pca.py",
    "2.2.ml_opcodes_pca.py",
    "2.3.ml_permissions_pca.py",
    "3.1.nsga2-voting-dt.py",
    "3.2.nsga2-voting-knn.py",
    "3.3.nsga2-voting-rf.py",

]

def main():

    root = Path(__file__).resolve().parents[1]

    for script in SCRIPTS:
        print(f"\n=== Rodando {script} ===")
        # Use the current interpreter (e.g., the virtualenv Python) to avoid missing deps.
        run([sys.executable, str(root / "experiments" / script)], check=True)

if __name__ == "__main__":
    main()
