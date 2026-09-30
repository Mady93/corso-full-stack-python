"""Confronta workspace_prova con l'ultimo backup (contenuto byte per byte)."""

import filecmp
import os

from backup import BASE_DIR, CARTELLE_ESCLUSE, ESTENSIONI_ESCLUSE, elenca_backup

ORIGINE = os.path.join(BASE_DIR, "workspace_prova")


def file_attesi(radice: str) -> set[str]:
    """Elenca i percorsi relativi dei file che dovrebbero essere stati copiati."""
    trovati = set()
    for cartella, sottocartelle, files in os.walk(radice):
        # Tolgo le cartelle escluse, come fa il backup
        sottocartelle[:] = [d for d in sottocartelle if d not in CARTELLE_ESCLUSE]
        for f in files:
            if os.path.splitext(f)[1].lower() not in ESTENSIONI_ESCLUSE:
                trovati.add(os.path.relpath(os.path.join(cartella, f), radice))
    return trovati


backups = elenca_backup()
if not backups:
    print("Nessun backup trovato in backup_output")
else:
    copia = backups[-1]
    print(f"Confronto con: {copia}")
    attesi = file_attesi(ORIGINE)
    copiati = file_attesi(copia)
    print("Mancanti nella copia:", sorted(attesi - copiati) or "nessuno")
    print("In più nella copia:", sorted(copiati - attesi) or "nessuno")
    diversi = [f for f in attesi & copiati
               # shallow=False: confronta il contenuto, non solo dimensione e data
               if not filecmp.cmp(os.path.join(ORIGINE, f), os.path.join(copia, f), shallow=False)]
    print("Contenuto diverso:", diversi or "nessuno")