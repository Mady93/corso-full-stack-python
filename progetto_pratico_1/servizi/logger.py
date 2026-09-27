"""
File Logger puro su disco (nessuna dipendenza esterna, solo open()).
"""

import os
from datetime import datetime

# Cartella radice del progetto: calcolata a partire dalla posizione di
# QUESTO file (servizi/logger.py), non dalla cartella da cui viene lanciato
# il programma. Cosi' il log finisce sempre nello stesso posto (progetto/logs/),
# sia che tu lanci "py main.py" dalla root, sia che tu lanci qualcosa da
# dentro tests/ o da qualunque altra cartella.
CARTELLA_PROGETTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARTELLA_LOG = os.path.join(CARTELLA_PROGETTO, "logs")
PERCORSO_LOG_DEFAULT = os.path.join(CARTELLA_LOG, "app_jira.log")


class FileLogger:
    """Registra gli eventi e le eccezioni su un file di log locale,
    sempre dentro la cartella logs/ del progetto (creata automaticamente
    se non esiste)."""

    def __init__(self, file_path: str = None) -> None:
        self._file_path: str = file_path if file_path is not None else PERCORSO_LOG_DEFAULT
        # Crea la cartella di destinazione se non esiste ancora (es. al
        # primissimo avvio del programma su una macchina nuova).
        os.makedirs(os.path.dirname(self._file_path), exist_ok=True)

    def info(self, messaggio: str, *args, **kwargs) -> None:
        self._scrivi_log("INFO", messaggio)

    def error(self, messaggio: str, *args, **kwargs) -> None:
        self._scrivi_log("ERROR", messaggio)

    def _scrivi_log(self, livello: str, messaggio: str) -> None:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        riga = f"[{now}] [{livello}] {messaggio}\n"
        try:
            # UNICO punto del progetto che scrive su disco: qui salvo solo
            # righe di log testuali (audit trail: chi ha fatto cosa e quando),
            # NON lo stato dell'applicazione.
            # Utenti/ticket/sprint restano solo in RAM
            # dentro GestionaleJira e si perdono alla chiusura.
            with open(self._file_path, "a", encoding="utf-8") as f:
                f.write(riga)
        except Exception as e:
            # Fallback volontario: se anche la scrittura su disco fallisce
            # (es. permessi), non vogliamo che l'intera app crashi solo
            # per un problema di logging.
            print(f"Errore nella scrittura del file log: {e}")