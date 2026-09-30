"""Logica del backup selettivo: validazione, selezione, copia e rotazione di 2 backup."""

import os
import shutil
from datetime import datetime
from typing import Any

# Tipo del riepilogo: dizionario con liste di file, byte totali ed errori
Riepilogo = dict[str, Any]

# Cartella dove si trova questo file (base per tutti i percorsi del progetto)
BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
# Dove vengono create le copie
OUTPUT_DIR: str = os.path.join(BASE_DIR, "backup_output")
# Cartella temporanea: la copia nasce qui e viene spostata solo a operazione finita
TEMP_DIR: str = os.path.join(OUTPUT_DIR, "_in_corso")
# Numero massimo di backup conservati
MAX_BACKUP: int = 2

# Cartelle che non voglio copiare (backup_output evita che il backup finisca dentro sé stesso)
CARTELLE_ESCLUSE: set[str] = {"__pycache__", ".venv", "venv", ".git", "node_modules",
                              ".idea", "backup_output"}
# Estensioni dei file che non voglio copiare
ESTENSIONI_ESCLUSE: set[str] = {".pyc", ".tmp", ".log"}


def valida_origine(percorso: str) -> tuple[bool, str]:
    """Controlla che l'origine sia una cartella valida e non vuota; restituisce (esito, messaggio)."""
    if not percorso.strip():
        return False, "Percorso vuoto"
    # os.path.exists: True se il percorso esiste (file o cartella)
    if not os.path.exists(percorso):
        return False, "Il percorso non esiste"
    # os.path.isdir: True solo se è una cartella
    if not os.path.isdir(percorso):
        return False, "Il percorso non è una cartella"
    # os.path.abspath: trasforma un percorso relativo in assoluto
    assoluto = os.path.abspath(percorso)
    # La cartella radice del disco ha sé stessa come genitore: la rifiuto per sicurezza
    if os.path.dirname(assoluto) == assoluto:
        return False, "Cartella radice non ammessa"
    # os.path.normcase: su Windows rende minuscoli i percorsi (maiuscole e minuscole sono equivalenti)
    output = os.path.normcase(os.path.abspath(OUTPUT_DIR))
    confronto = os.path.normcase(assoluto)
    # Rifiuto origini dentro backup_output: il backup copierebbe sé stesso
    if confronto == output or confronto.startswith(output + os.sep):
        return False, "L'origine non può essere dentro backup_output"
    # os.listdir: elenco dei nomi contenuti nella cartella
    if not os.listdir(percorso):
        return False, "La cartella è vuota"
    return True, "OK"


def nuovo_nome_backup() -> str:
    """Costruisce il percorso del nuovo backup: backup_output/backup_AAAA-MM-GG_HH-MM-SS."""
    # datetime.now().strftime: data e ora attuali nel formato scelto
    return os.path.join(OUTPUT_DIR, "backup_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))


def percorso_libero(base: str) -> str:
    """Aggiunge un suffisso _2, _3... finché trova un nome di cartella non ancora usato."""
    n = 2
    while os.path.exists(f"{base}_{n}"):
        n += 1
    return f"{base}_{n}"


def controlla_dentro_output(percorso: str) -> str:
    """Restituisce il percorso assoluto solo se sta dentro backup_output (sicurezza)."""
    assoluto = os.path.abspath(percorso)
    # os.sep: separatore del sistema (\ su Windows, / su Linux/macOS)
    if not assoluto.startswith(os.path.abspath(OUTPUT_DIR) + os.sep):
        raise ValueError("Operazione fuori da backup_output non permessa")
    return assoluto


def elimina_backup(percorso: str) -> None:
    """Elimina una cartella di backup, ma solo se sta dentro backup_output."""
    assoluto = controlla_dentro_output(percorso)
    # shutil.rmtree: elimina una cartella con tutto il contenuto (distruttivo!)
    shutil.rmtree(assoluto)


def elenca_backup() -> list[str]:
    """Restituisce i backup esistenti ordinati dal meno recente al più recente."""
    if not os.path.isdir(OUTPUT_DIR):
        return []
    nomi = [n for n in os.listdir(OUTPUT_DIR)
            if n.startswith("backup_") and os.path.isdir(os.path.join(OUTPUT_DIR, n))]
    # Il nome contiene data e ora (AAAA-MM-GG_HH-MM-SS): ordinarli come testo li ordina anche per data
    return [os.path.join(OUTPUT_DIR, n) for n in sorted(nomi)]


def backup_da_eliminare() -> list[str]:
    """Restituisce i backup meno recenti da eliminare per fare posto a quello nuovo."""
    esistenti = elenca_backup()
    # Dopo la nuova copia devono restarne al massimo MAX_BACKUP, quindi qui ne tengo MAX_BACKUP - 1
    eccesso = len(esistenti) - (MAX_BACKUP - 1)
    return esistenti[:eccesso] if eccesso > 0 else []


def pulisci_temp() -> None:
    """Elimina la cartella temporanea rimasta da un backup interrotto."""
    # os.path.exists: controllo se c'è un residuo prima di eliminarlo
    if os.path.exists(TEMP_DIR):
        elimina_backup(TEMP_DIR)


def pubblica_backup(temp: str, destinazione: str) -> str:
    """Sposta la copia completata dalla cartella temporanea alla destinazione finale."""
    controlla_dentro_output(destinazione)
    # Se il nome è già occupato aggiungo un suffisso: move dentro una cartella esistente la annidierebbe
    if os.path.exists(destinazione):
        destinazione = percorso_libero(destinazione)
    # shutil.move: sposta la cartella (a differenza di copy, l'originale sparisce)
    shutil.move(temp, destinazione)
    return destinazione


def e_escluso(nome: str, e_cartella: bool) -> bool:
    """Dice se un file o una cartella va escluso dal backup."""
    if e_cartella:
        return nome in CARTELLE_ESCLUSE
    # os.path.splitext: divide "file.txt" in ("file", ".txt"); prendo l'estensione
    return os.path.splitext(nome)[1].lower() in ESTENSIONI_ESCLUSE


def copia_selettiva(origine: str, destinazione: str) -> Riepilogo:
    """Copia origine in destinazione saltando gli elementi esclusi; restituisce il riepilogo."""
    riepilogo: Riepilogo = {"copiati": [], "esclusi": [], "errori": [], "byte": 0}

    # os.walk: visita la cartella e tutte le sottocartelle (ricorsivo), restituisce (cartella, sottocartelle, file)
    for cartella, sottocartelle, files in os.walk(origine):
        # os.path.relpath: percorso relativo all'origine (serve per ricreare la stessa struttura)
        rel = os.path.relpath(cartella, origine)

        # Rimuovo le cartelle escluse dalla lista: os.walk non entrerà al loro interno
        for d in list(sottocartelle):
            if e_escluso(d, True):
                sottocartelle.remove(d)
                # os.path.normpath: pulisce il percorso (es. "./x" diventa "x")
                riepilogo["esclusi"].append(os.path.normpath(os.path.join(rel, d)) + os.sep)

        cartella_dest = os.path.normpath(os.path.join(destinazione, rel))
        # os.makedirs: crea la cartella (e i genitori); exist_ok=True evita l'errore se esiste già
        os.makedirs(cartella_dest, exist_ok=True)

        for nome in files:
            percorso_rel = os.path.normpath(os.path.join(rel, nome))
            if e_escluso(nome, False):
                riepilogo["esclusi"].append(percorso_rel)
                continue
            try:
                sorgente = os.path.join(cartella, nome)
                # shutil.copy2: copia il file mantenendo anche i metadati (data di modifica)
                shutil.copy2(sorgente, os.path.join(cartella_dest, nome))
                riepilogo["copiati"].append(percorso_rel)
                # os.path.getsize: dimensione del file in byte
                riepilogo["byte"] += os.path.getsize(sorgente)
            except OSError as e:
                # Un file non copiabile non blocca il backup: lo segno tra gli errori
                riepilogo["errori"].append(f"{percorso_rel}: {e}")

    return riepilogo