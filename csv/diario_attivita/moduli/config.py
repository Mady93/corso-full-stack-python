# Percorsi e costanti condivisi da tutti i moduli.
# Se cambia un nome di file o di cartella, si modifica solo qui.

import os

# Questo file sta in moduli/: la cartella del progetto è un livello sopra
CARTELLA_PROGETTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARTELLA_DATI = os.path.join(CARTELLA_PROGETTO, "dati")

FILE_DIARIO = os.path.join(CARTELLA_DATI, "diario.txt")
FILE_LOG = os.path.join(CARTELLA_DATI, "attivita.log")
FILE_EXPORT = os.path.join(CARTELLA_DATI, "attivita_export.csv")

CSV_DEFAULT = "attivita_esempio.csv"   # file proposto per l'importazione
CAMPI_CSV = ["id", "data_ora", "categoria", "descrizione", "durata_minuti"]