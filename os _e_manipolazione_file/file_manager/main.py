"""File manager da terminale: explorer testuale + backup di cartelle.

Questo file coordina soltanto il menu: la logica sta nel pacchetto moduli/.
  moduli/explorer.py  percorsi e contenuti
  moduli/backup.py    copia e archiviazione
  moduli/analisi.py   statistiche sull'albero di cartelle
"""

from __future__ import annotations

from pathlib import Path
from typing import Callable, Dict, Optional, Tuple

from moduli import (
    analizza_cartella,
    stampa_analisi,
    crea_backup_interattivo,
    menu_gestione_backup,
    esplora,
    chiedi_percorso,
)
from moduli.config import CARTELLA_BACKUP

# Stato condiviso tra le voci del menu:
# sorgente - cartella scelta nell'explorer (proposta come sorgente del backup)
# cartella_backup - ultima cartella in cui sono stati salvati i backup
stato: Dict[str, Optional[Path]] = {"sorgente": None, "cartella_backup": CARTELLA_BACKUP}


def chiedi_cartella_esistente(messaggio: str) -> Path | None:
    """Chiede una cartella e controlla che esista.

    Returns:
        Il percorso, oppure None (dopo aver stampato l'errore) se non esiste o non è una cartella.
    """
    # "A or B": se non c'è una sorgente selezionata propongo la cartella da cui è stato lanciato il programma
    percorso = chiedi_percorso(messaggio, stato["sorgente"] or Path.cwd())
    if percorso is None:
        return None
    if not percorso.exists():
        print(f"ERRORE: il percorso non esiste: {percorso}")
        return None
    if not percorso.is_dir():
        print(f"ERRORE: il percorso non è una cartella: {percorso}")
        return None
    return percorso


def voce_esplora() -> None:
    """Voce 1: apre l'explorer; se l'utente usa 'seleziona' ricorda la cartella come sorgente."""
    iniziale = chiedi_cartella_esistente("Cartella da esplorare")
    if iniziale is None:
        return
    selezionata = esplora(iniziale)
    if selezionata is not None:
        stato["sorgente"] = selezionata
        print(f"\nCartella selezionata come sorgente del backup: {selezionata}")
        print("Usa la voce 3 del menu per creare il backup.")


def voce_analizza() -> None:
    """Voce 2: analizza una cartella e ne stampa le statistiche."""
    cartella = chiedi_cartella_esistente("Cartella da analizzare")
    if cartella is not None:
        stampa_analisi(analizza_cartella(cartella))


def voce_crea_backup() -> None:
    """Voce 3: crea un backup e ricorda la cartella in cui è stato salvato."""
    percorso = crea_backup_interattivo(stato["sorgente"], stato["cartella_backup"])
    if percorso is not None:
        stato["cartella_backup"] = percorso.parent


def voce_gestisci_backup() -> None:
    """Voce 4: apre il menu di gestione dei backup."""
    menu_gestione_backup(stato["cartella_backup"])


# Ogni voce: tasto - (testo mostrato, funzione da chiamare). Per aggiungere una voce basta una riga.
VOCI_MENU: Dict[str, Tuple[str, Callable[[], None]]] = {
    "1": ("Esplora cartella", voce_esplora),
    "2": ("Analizza cartella", voce_analizza),
    "3": ("Crea backup", voce_crea_backup),
    "4": ("Gestisci backup", voce_gestisci_backup),
}


def main() -> None:
    """Mostra il menu principale finché l'utente non sceglie di uscire."""
    try:
        while True:
            print("\nFILE MANAGER\n")
            for tasto, (descrizione, _) in VOCI_MENU.items():
                print(f"{tasto}. {descrizione}")
            print("5. Esci")
            scelta = input("Scelta: ").strip()

            if scelta == "5":
                print("Arrivederci!")
                break
            elif scelta in VOCI_MENU:
                VOCI_MENU[scelta][1]()  # [1] = la funzione della voce, poi () la esegue
            else:
                print("Scelta non valida.")
    except (KeyboardInterrupt, EOFError):  # Ctrl+C oppure fine dell'input: esco senza errori rossi
        print("\nUscita.")


if __name__ == "__main__":
    main()