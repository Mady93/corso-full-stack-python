"""Crea la cartella workspace_prova/ con file di più tipi, una sottocartella e elementi da escludere."""

import os

# Cartella dove si trova questo file
BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
RADICE: str = os.path.join(BASE_DIR, "workspace_prova")

# Percorso relativo del file -> contenuto di prova
FILE: dict[str, str] = {
    "app.py": "print('app')\n",
    "utils.py": "def somma(a, b):\n    return a + b\n",
    "note.txt": "appunti di prova\n",
    "dati.csv": "nome,voto\nmario,30\n",
    "logo.png": "finto contenuto immagine",
    "log.tmp": "file temporaneo da escludere\n",
    "progetto1/main.py": "print('progetto1')\n",
    "progetto1/config.json": '{"debug": true}\n',
    "__pycache__/app.cpython-312.pyc": "bytecode finto",
    ".venv/pyvenv.cfg": "home = finto\n",
}


def crea_workspace_prova() -> None:
    """Scrive tutti i file di prova, creando le sottocartelle necessarie."""
    for percorso_rel, contenuto in FILE.items():
        percorso = os.path.join(RADICE, percorso_rel)
        # os.makedirs: crea le cartelle mancanti; exist_ok=True evita errori se esistono già
        os.makedirs(os.path.dirname(percorso), exist_ok=True)
        # "w" = scrittura: crea il file o lo sovrascrive
        with open(percorso, "w", encoding="utf-8") as f:
            f.write(contenuto)
    print(f"Cartella di prova creata in {RADICE}")


if __name__ == "__main__":
    crea_workspace_prova()