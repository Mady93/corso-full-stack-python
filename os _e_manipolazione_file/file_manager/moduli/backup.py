"""Parte A - backup di cartelle (copia ricorsiva oppure archivio ZIP).

Il modulo ha due parti:
  1) LOGICA: funzioni che fanno il lavoro; se qualcosa va storto sollevano ErroreBackup
     con un messaggio già leggibile dall'utente.
  2) INTERFACCIA: funzioni che fanno le domande da terminale e stampano i risultati.
"""

from __future__ import annotations

import shutil
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

from .analisi import analizza_cartella
from .utilita import (chiedi_conferma, chiedi_percorso, formatta_data,
                      formatta_dimensione)

PREFISSO: str = "backup_"
FORMATO_DATA: str = "%Y-%m-%d_%H-%M-%S"  # dà nomi come backup_2026-10-01_10-30-00

# Informazioni su un backup: nome, tipo, data, numero di file, ecc.
InfoBackup = Dict[str, Any]


class ErroreBackup(Exception):
    """Errore con un messaggio già pronto da mostrare all'utente."""


# 1) LOGICA
def _messaggio(errore: Exception) -> str:
    """Rende leggibile un errore di sistema o di shutil.

    shutil.Error contiene una lista di tuple (origine, destinazione, motivo): la riassumo.
    """
    if isinstance(errore, shutil.Error) and errore.args and isinstance(errore.args[0], list):
        elementi = errore.args[0]
        return f"{len(elementi)} elementi non copiati (es. {elementi[0][2]})"
    # OSError ha strerror (testo dell'errore di sistema); per gli altri errori uso str()
    return getattr(errore, "strerror", None) or str(errore)


def _dentro(percorso: Path, cartella: Path) -> bool:
    """True se 'percorso' coincide con 'cartella' o si trova al suo interno."""
    try:
        percorso.relative_to(cartella)  # solleva ValueError se 'percorso' non sta dentro 'cartella'
        return True
    except ValueError:
        return False


def _rimuovi(percorso: Path) -> None:
    """Elimina un backup (cartella o file) ignorando gli errori: serve per la pulizia."""
    if percorso.is_dir():
        shutil.rmtree(percorso, ignore_errors=True)  # rmtree elimina una cartella con tutto il contenuto
    elif percorso.exists():
        percorso.unlink()  # unlink elimina un singolo file


def crea_backup(sorgente: Path | str, destinazione: Path | str, formato: str = "cartella") -> Path:
    """Crea backup_DATA-ORA dentro 'destinazione'.

    Non sovrascrive mai un backup esistente, perché il nome contiene data e ora.

    Args:
        sorgente: cartella da salvare.
        destinazione: cartella che conterrà il backup (creata se manca).
        formato: "cartella" (copia ricorsiva) oppure "zip" (archivio compresso).

    Returns:
        Percorso del backup creato.

    Raises:
        ErroreBackup: sorgente inesistente o non valida, destinazione non valida, copia fallita.
    """
    sorgente = Path(sorgente).resolve()
    destinazione = Path(destinazione).resolve()

    if not sorgente.exists():
        raise ErroreBackup(f"La cartella sorgente non esiste: {sorgente}")
    if not sorgente.is_dir():
        raise ErroreBackup(f"La sorgente non è una cartella: {sorgente}")
    # Se il backup finisse dentro la sorgente, la copia includerebbe sé stessa all'infinito
    if _dentro(destinazione, sorgente):
        raise ErroreBackup("La destinazione non può trovarsi dentro la cartella sorgente: "
                           "il backup copierebbe anche sé stesso.")
    if destinazione.exists() and not destinazione.is_dir():
        raise ErroreBackup(f"La destinazione esiste ed è un file, non una cartella: {destinazione}")

    try:
        # mkdir(parents=True) crea anche le cartelle intermedie; exist_ok=True non dà errore se c'è già
        destinazione.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        raise ErroreBackup(f"Impossibile creare la destinazione ({_messaggio(e)}): {destinazione}")

    # strftime trasforma la data/ora attuale nel testo del nome (es. 2026-10-01_10-30-00)
    nome = PREFISSO + datetime.now().strftime(FORMATO_DATA)
    percorso_backup = destinazione / (nome + (".zip" if formato == "zip" else ""))
    if percorso_backup.exists():
        raise ErroreBackup("Esiste già un backup con questo nome (creato nello stesso secondo): "
                           "riprova tra un istante. Nessun dato è stato sovrascritto.")

    try:
        if formato == "zip":
            # make_archive crea l'archivio e aggiunge da solo ".zip" al nome; root_dir = cartella da comprimere
            shutil.make_archive(str(destinazione / nome), "zip", root_dir=sorgente)
        else:
            # copytree copia ricorsivamente; symlinks=True copia i collegamenti come collegamenti (evita cicli)
            shutil.copytree(sorgente, percorso_backup, symlinks=True)
    except (OSError, shutil.Error) as e:
        _rimuovi(percorso_backup)  # non lascio backup a metà
        raise ErroreBackup(f"Backup non riuscito, la copia incompleta è stata eliminata: {_messaggio(e)}")

    return percorso_backup


def _data_backup(percorso: Path) -> datetime:
    """Data di creazione letta dal nome del backup; se non è leggibile usa la data del file."""
    # stem = nome senza estensione (serve per togliere ".zip"); len(PREFISSO) salta "backup_"
    testo = percorso.stem if percorso.suffix == ".zip" else percorso.name
    try:
        # strptime fa il contrario di strftime: da testo a data/ora
        return datetime.strptime(testo[len(PREFISSO):], FORMATO_DATA)
    except ValueError:
        return datetime.fromtimestamp(percorso.stat().st_mtime)


def riepilogo_backup(percorso: Path | str) -> InfoBackup:
    """Raccoglie le informazioni su un backup (cartella o ZIP).

    Returns:
        Dizionario con nome, percorso, tipo, data, file, cartelle, contenuto (byte
        non compressi) e su_disco (byte realmente occupati).

    Raises:
        ErroreBackup: se l'archivio è danneggiato o il backup non è leggibile.
    """
    percorso = Path(percorso)
    try:
        if percorso.is_dir():
            a = analizza_cartella(percorso)
            tipo, n_file, n_cartelle = "cartella", a["file"], a["cartelle"]
            contenuto = su_disco = a["dimensione"]
        else:
            tipo = "zip"
            su_disco = percorso.stat().st_size
            with zipfile.ZipFile(percorso) as archivio:  # apre lo ZIP in lettura
                voci = archivio.infolist()  # infolist = elenco di tutte le voci contenute nello ZIP
            n_file = sum(1 for v in voci if not v.is_dir())  # is_dir() distingue cartelle da file nello ZIP
            n_cartelle = sum(1 for v in voci if v.is_dir())
            contenuto = sum(v.file_size for v in voci)  # file_size = dimensione originale (non compressa)
    except zipfile.BadZipFile:
        raise ErroreBackup(f"L'archivio ZIP è danneggiato: {percorso.name}")
    except OSError as e:
        raise ErroreBackup(f"Impossibile leggere il backup ({_messaggio(e)}): {percorso.name}")

    return {"nome": percorso.name, "percorso": percorso, "tipo": tipo,
            "data": _data_backup(percorso), "file": n_file, "cartelle": n_cartelle,
            "contenuto": contenuto, "su_disco": su_disco}


def verifica_backup(sorgente: Path | str,
                    percorso_backup: Path | str) -> Tuple[bool, Any, InfoBackup]:
    """Confronta il backup con la sorgente (numero di file, cartelle e byte).

    Returns:
        (uguale, statistiche della sorgente, informazioni sul backup).
    """
    s = analizza_cartella(sorgente)
    b = riepilogo_backup(percorso_backup)
    # Confronto le due terne (file, cartelle, byte): se coincidono il backup è completo
    uguale = ((s["file"], s["cartelle"], s["dimensione"])
              == (b["file"], b["cartelle"], b["contenuto"]))
    return uguale, s, b


def elenca_backup(destinazione: Path | str) -> List[Path]:
    """Elenca i backup presenti nella cartella, ordinati per nome (quindi per data).

    Raises:
        ErroreBackup: se la cartella non è leggibile.
    """
    destinazione = Path(destinazione)
    if not destinazione.is_dir():
        return []
    try:
        voci = list(destinazione.iterdir())  # iterdir dà gli elementi contenuti nella cartella
    except OSError as e:
        raise ErroreBackup(f"Impossibile leggere la cartella dei backup ({_messaggio(e)})")
    # Un backup è una cartella o uno .zip il cui nome inizia con "backup_"
    backup = [p for p in voci
              if p.name.startswith(PREFISSO) and (p.is_dir() or p.suffix == ".zip")]
    return sorted(backup, key=lambda p: p.name)  # key = criterio di ordinamento (il nome)


def elimina_backup(percorso: Path) -> None:
    """Elimina un backup in modo definitivo.

    Raises:
        ErroreBackup: se l'eliminazione non riesce.
    """
    try:
        if percorso.is_dir():
            shutil.rmtree(percorso)
        else:
            percorso.unlink()
    except OSError as e:
        raise ErroreBackup(f"Eliminazione non riuscita: {_messaggio(e)}")


def ripristina_backup(percorso: Path, destinazione: Path | str) -> None:
    """Copia il contenuto del backup nella cartella di destinazione.

    I file con lo stesso nome già presenti nella destinazione vengono sovrascritti.

    Raises:
        ErroreBackup: se la destinazione non è valida o il ripristino fallisce.
    """
    destinazione = Path(destinazione)
    if destinazione.exists() and not destinazione.is_dir():
        raise ErroreBackup(f"La destinazione esiste ed è un file, non una cartella: {destinazione}")
    try:
        destinazione.mkdir(parents=True, exist_ok=True)
        if percorso.is_dir():
            # dirs_exist_ok=True: se la cartella esiste già, unisce i contenuti invece di dare errore
            shutil.copytree(percorso, destinazione, dirs_exist_ok=True, symlinks=True)
        else:
            # unpack_archive estrae l'archivio (formato riconosciuto dall'estensione .zip)
            shutil.unpack_archive(str(percorso), str(destinazione))
    except (OSError, shutil.Error, zipfile.BadZipFile) as e:
        raise ErroreBackup(f"Ripristino non riuscito: {_messaggio(e)}")



# 2) INTERFACCIA DA TERMINALE
def crea_backup_interattivo(sorgente_default: Path | None,
                            cartella_default: Path | None) -> Path | None:
    """Guida l'utente nella creazione di un backup (sorgente, destinazione, formato).

    Args:
        sorgente_default: sorgente proposta (es. quella scelta nell'explorer).
        cartella_default: destinazione proposta.

    Returns:
        Percorso del backup creato, oppure None se annullato o fallito.
    """
    print("\n=== CREA BACKUP ===")
    sorgente = chiedi_percorso("Cartella sorgente", sorgente_default)
    if sorgente is None:
        print("Nessuna cartella indicata: operazione annullata.")
        return None
    if not sorgente.exists():
        print(f"ERRORE: la cartella sorgente non esiste: {sorgente}")
        return None
    if not sorgente.is_dir():
        print(f"ERRORE: la sorgente non è una cartella: {sorgente}")
        return None

    destinazione = chiedi_percorso("Cartella dove salvare il backup", cartella_default)
    if destinazione is None:
        print("Nessuna destinazione indicata: operazione annullata.")
        return None

    # Controllo subito, prima di fare altre domande: la copia includerebbe sé stessa
    if _dentro(destinazione, sorgente):
        print("ERRORE: la destinazione non può trovarsi dentro la cartella sorgente: "
              "il backup copierebbe anche sé stesso.")
        return None

    print("Formato del backup:")
    print("  1) cartella duplicata")
    print("  2) archivio ZIP")
    scelta = input("Scelta [1]: ").strip() or "1"  # "x or y": se l'utente preme solo Invio vale "1"
    if scelta not in ("1", "2"):
        print("Scelta non valida: operazione annullata.")
        return None
    formato = "zip" if scelta == "2" else "cartella"

    try:
        # Destinazione già presente: i backup esistenti non vengono toccati
        if destinazione.exists() and destinazione.is_dir():
            n = len(elenca_backup(destinazione))
            print(f"La destinazione esiste già e contiene {n} backup: non verranno modificati.")
        elif not destinazione.exists():
            if not chiedi_conferma(f"La cartella {destinazione} non esiste. Crearla?"):
                print("Operazione annullata.")
                return None

        percorso = crea_backup(sorgente, destinazione, formato)
        uguale, s, b = verifica_backup(sorgente, percorso)
    except ErroreBackup as e:
        print(f"ERRORE: {e}")
        return None

    print(f"\nBackup creato: {percorso}")
    print(f"  {b['file']} file, {b['cartelle']} sottocartelle, "
          f"{formatta_dimensione(b['su_disco'])} su disco")
    if s["file"] == 0 and s["cartelle"] == 0:
        print("  Nota: la cartella sorgente era vuota.")
    if uguale:
        print("Verifica: il contenuto del backup coincide con la sorgente.")
    else:
        print("ATTENZIONE: il backup non coincide con la sorgente "
              f"(sorgente: {s['file']} file, {s['cartelle']} cartelle; "
              f"backup: {b['file']} file, {b['cartelle']} cartelle).")
    return percorso


def _stampa_elenco(cartella: Path, backup: List[Path]) -> None:
    """Stampa la tabella BACKUP DISPONIBILI (nome, data, tipo, dimensione)."""
    print(f"\nBACKUP DISPONIBILI in {cartella}\n")
    # In {x:<32} il "<32" allinea a sinistra in 32 caratteri: così le colonne restano incolonnate
    print(f"{'N':>3}  {'NOME':<32} {'DATA':<20} {'TIPO':<9} DIMENSIONE")
    print("-" * 78)
    for numero, p in enumerate(backup, start=1):  # enumerate numera gli elementi partendo da 1
        try:
            r = riepilogo_backup(p)
            print(f"{numero:>3}  {r['nome']:<32} {formatta_data(r['data'].timestamp()):<20} "
                  f"{r['tipo']:<9} {formatta_dimensione(r['su_disco'])}")
        except ErroreBackup as e:
            print(f"{numero:>3}  {p.name:<32} (non leggibile: {e})")


def _scegli_backup(cartella: Path) -> Path | None:
    """Mostra l'elenco e fa scegliere un backup con il suo numero.

    Returns:
        Il backup scelto, oppure None se non ce ne sono o il numero non è valido.
    """
    backup = elenca_backup(cartella)
    if not backup:
        print(f"Nessun backup trovato in {cartella}")
        return None
    _stampa_elenco(cartella, backup)
    scelta = input("\nNumero del backup: ").strip()
    # isdigit() controlla che siano solo cifre; poi verifico che il numero sia nell'elenco
    if scelta.isdigit() and 1 <= int(scelta) <= len(backup):
        return backup[int(scelta) - 1]  # il numero mostrato parte da 1, gli indici della lista da 0
    print("Numero non valido.")
    return None


def _mostra_informazioni(cartella: Path) -> None:
    """Mostra il riepilogo dettagliato di un backup scelto dall'utente."""
    p = _scegli_backup(cartella)
    if p is None:
        return
    r = riepilogo_backup(p)
    print(f"\nNome                : {r['nome']}")
    print(f"Percorso            : {r['percorso']}")
    print(f"Tipo                : {r['tipo']}")
    print(f"Creato il           : {formatta_data(r['data'].timestamp())}")
    print(f"File contenuti      : {r['file']}")
    print(f"Sottocartelle       : {r['cartelle']}")
    print(f"Dimensione contenuto: {formatta_dimensione(r['contenuto'])}")
    print(f"Spazio su disco     : {formatta_dimensione(r['su_disco'])}")


def _elimina(cartella: Path) -> None:
    """Elimina un backup scelto dall'utente, previa conferma esplicita."""
    p = _scegli_backup(cartella)
    if p is None:
        return
    print(f"\nATTENZIONE: il backup {p.name} verrà eliminato in modo DEFINITIVO.")
    if not chiedi_conferma("Confermi l'eliminazione?"):
        print("Eliminazione annullata: nessun dato è stato toccato.")
        return
    elimina_backup(p)
    print(f"Backup eliminato: {p.name}")


def _ripristina(cartella: Path) -> None:
    """Ripristina un backup scelto; se la destinazione contiene già dei file chiede conferma."""
    p = _scegli_backup(cartella)
    if p is None:
        return
    nome_base = p.stem if p.suffix == ".zip" else p.name  # stem toglie ".zip" dal nome
    proposta = Path(cartella) / f"ripristino_{nome_base}"  # destinazione nuova: non tocca i dati originali
    destinazione = chiedi_percorso("\nCartella in cui ripristinare", proposta)
    assert destinazione is not None  # con una proposta di default il risultato non è mai None

    if destinazione.exists() and not destinazione.is_dir():
        print(f"ERRORE: la destinazione è un file, non una cartella: {destinazione}")
        return
    # any(...) è True se la cartella contiene almeno un elemento: in quel caso servono avvisi e conferma
    if destinazione.exists() and any(destinazione.iterdir()):
        print(f"ATTENZIONE: {destinazione} contiene già dei file.")
        print("I file con lo stesso nome verranno SOVRASCRITTI.")
        if not chiedi_conferma("Vuoi procedere con il ripristino?"):
            print("Ripristino annullato: nessun dato è stato toccato.")
            return

    ripristina_backup(p, destinazione)
    r = analizza_cartella(destinazione)
    print(f"Ripristino completato in {destinazione}")
    print(f"  La cartella ora contiene {r['file']} file e {r['cartelle']} sottocartelle.")


def menu_gestione_backup(cartella_default: Path | None) -> None:
    """Menu per elencare, ispezionare, eliminare e ripristinare i backup.

    Args:
        cartella_default: cartella dei backup proposta all'utente.
    """
    print("\n=== GESTIONE BACKUP ===")
    cartella = chiedi_percorso("Cartella che contiene i backup", cartella_default)
    if cartella is None:
        print("Nessuna cartella indicata.")
        return
    if not cartella.exists():
        print(f"ERRORE: la cartella non esiste: {cartella}")
        return
    if not cartella.is_dir():
        print(f"ERRORE: non è una cartella: {cartella}")
        return

    while True:
        print("\n1) Elenca i backup")
        print("2) Mostra informazioni di un backup")
        print("3) Elimina un backup")
        print("4) Ripristina un backup")
        print("0) Torna al menu principale")
        scelta = input("Scelta: ").strip()

        try:
            if scelta == "1":
                backup = elenca_backup(cartella)
                if backup:
                    _stampa_elenco(cartella, backup)
                else:
                    print(f"Nessun backup trovato in {cartella}")
            elif scelta == "2":
                _mostra_informazioni(cartella)
            elif scelta == "3":
                _elimina(cartella)
            elif scelta == "4":
                _ripristina(cartella)
            elif scelta == "0":
                return
            else:
                print("Scelta non valida.")
        except (ErroreBackup, OSError) as e:
            print(f"ERRORE: {e}")