"""Parte B - file explorer testuale.

Gli elementi si scelgono con il NUMERO mostrato nell'elenco oppure con il NOME.
Per i comandi che chiedono un secondo dato (nuovo nome, destinazione) il programma lo
domanda a parte, così nomi e percorsi con spazi non danno problemi.
I percorsi relativi scritti dall'utente sono relativi alla cartella corrente dell'explorer,
non a quella da cui è stato lanciato il programma.
"""

from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Callable, List

from .analisi import analizza_cartella, stampa_analisi
from .utilita import chiedi_conferma, formatta_data, formatta_dimensione

LIMITE_RIGHE: int = 50  # righe mostrate dal comando 'leggi'
LIMITE_RISULTATI: int = 100  # risultati mostrati da 'cerca' ed 'ext'

AIUTO: str = """
COMANDI
  ls                        mostra il contenuto della cartella corrente
  cd <n|nome>               entra in una cartella
  su   (oppure cd ..)       torna alla cartella precedente
  home                      va alla cartella home
  inizio                    torna alla cartella da cui hai iniziato
  pwd                       mostra il percorso assoluto
  info [n|nome]             dimensione, estensione e data di modifica
  cerca <testo>             cerca per nome, anche nelle sottocartelle
  ext <estensione>          elenca i file con quell'estensione (es. ext .txt)
  analizza                  statistiche sulla cartella corrente
  leggi <n|nome>            mostra un file di testo
  nuova-cartella            crea una cartella
  nuovo-file                crea un file vuoto
  rinomina <n|nome>         rinomina un elemento
  copia <n|nome>            copia un file
  sposta <n|nome>           sposta un file
  elimina <n|nome>          elimina un file (con conferma)
  seleziona                 usa la cartella corrente come sorgente del backup
  aiuto                     mostra questo elenco
  esci                      torna al menu principale
"""


# ---------------- visualizzazione ----------------

def elenca(cartella: Path) -> List[Path]:
    """Restituisce il contenuto di una cartella: prima le cartelle, poi i file, in ordine alfabetico.

    Raises:
        OSError: se la cartella non è leggibile.
    """
    # iterdir() dà gli elementi della cartella; sorted ordina con la chiave (è un file?, nome minuscolo):
    # False < True, quindi le cartelle vengono prima dei file
    return sorted(cartella.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))


def mostra_cartella(corrente: Path) -> List[Path]:
    """Stampa la cartella corrente e restituisce la lista degli elementi mostrati.

    La lista serve a risolvere i numeri scritti dall'utente (es. 'cd 2').
    """
    print("\nEXPLORER")
    print(f"Percorso corrente: {corrente}\n")
    try:
        elementi = elenca(corrente)
    except OSError as e:
        print(f"Impossibile leggere la cartella: {e.strerror or e}")
        return []
    if not elementi:
        print("(cartella vuota)")
    for numero, p in enumerate(elementi, start=1):  # enumerate numera gli elementi da 1
        etichetta = "[DIR] " if p.is_dir() else "[FILE]"
        print(f"{numero:>3}. {etichetta} {p.name}")  # {numero:>3} = numero allineato a destra su 3 caratteri
    return elementi


def scegli(argomento: str, elementi: List[Path]) -> Path | None:
    """Trova l'elemento indicato dall'utente con numero o nome.

    Returns:
        L'elemento scelto, oppure None (dopo aver stampato il motivo) se non è valido.
    """
    if not argomento:
        print("Indica il numero o il nome dell'elemento.")
        return None
    if argomento.isdigit():  # isdigit() è True se il testo contiene solo cifre
        n = int(argomento)
        if 1 <= n <= len(elementi):
            return elementi[n - 1]  # il numero mostrato parte da 1, gli indici della lista da 0
        print(f"Numero non valido: scegli tra 1 e {len(elementi)}.")
        return None
    for p in elementi:
        if p.name == argomento:
            return p
    for p in elementi:  # secondo tentativo: ignorando maiuscole e minuscole
        if p.name.lower() == argomento.lower():
            return p
    print(f"Elemento non trovato: {argomento}")
    return None


def mostra_info(p: Path) -> None:
    """Mostra nome, tipo, percorso assoluto, estensione, dimensione e data di modifica."""
    try:
        st = p.stat()  # stat() legge i metadati del file (dimensione, date)
    except OSError as e:
        print(f"Impossibile leggere le informazioni: {e.strerror or e}")
        return
    print(f"\nNome         : {p.name}")
    print(f"Tipo         : {'cartella' if p.is_dir() else 'file'}")
    print(f"Percorso     : {p.resolve()}")  # resolve() = percorso assoluto
    if p.is_dir():
        a = analizza_cartella(p)
        print(f"Dimensione   : {formatta_dimensione(a['dimensione'])} (contenuto totale, "
              f"{a['file']} file)")
    else:
        print(f"Estensione   : {p.suffix or '(nessuna)'}")  # suffix = estensione, es. ".txt"
        print(f"Dimensione   : {formatta_dimensione(st.st_size)} ({st.st_size} byte)")
    print(f"Modificato il: {formatta_data(st.st_mtime)}")


# ---------------- ricerca ----------------

def _cerca(base: Path, condizione: Callable[[Path], bool], solo_file: bool = False) -> List[Path]:
    """Visita tutte le sottocartelle di 'base' e raccoglie gli elementi che rispettano la condizione.

    Args:
        base: cartella da cui partire.
        condizione: funzione che riceve un percorso e dice se va incluso.
        solo_file: se True ignora le cartelle e considera solo i file.
    """
    trovati: List[Path] = []
    # os.walk visita ricorsivamente: a ogni giro dà (cartella, nomi sottocartelle, nomi file)
    for cartella, sottocartelle, nomi_file in os.walk(base):
        nomi = nomi_file if solo_file else sottocartelle + nomi_file
        for nome in nomi:
            p = Path(cartella) / nome
            if condizione(p):
                trovati.append(p)
    return sorted(trovati, key=lambda p: str(p).lower())


def _stampa_risultati(base: Path, trovati: List[Path], criterio: str) -> None:
    """Stampa i risultati di una ricerca (percorsi relativi a 'base') e il loro numero."""
    if not trovati:
        print(f"Nessun risultato per {criterio}.")
        return
    for p in trovati[:LIMITE_RISULTATI]:  # [:N] prende solo i primi N elementi della lista
        etichetta = "[DIR] " if p.is_dir() else "[FILE]"
        print(f"  {etichetta} {p.relative_to(base)}")  # relative_to() toglie 'base' dall'inizio del percorso
    if len(trovati) > LIMITE_RISULTATI:
        print(f"  ... mostrati i primi {LIMITE_RISULTATI}")
    parola = "risultato" if len(trovati) == 1 else "risultati"
    print(f"\n{len(trovati)} {parola} per {criterio}")


def cerca_per_nome(base: Path, testo: str) -> None:
    """Cerca nella cartella e nelle sottocartelle gli elementi il cui nome contiene 'testo'."""
    if not testo:
        print("Scrivi il testo da cercare, es. 'cerca appunti'.")
        return
    trovati = _cerca(base, lambda p: testo.lower() in p.name.lower())
    _stampa_risultati(base, trovati, f"nome contenente '{testo}'")


def filtra_per_estensione(base: Path, estensione: str) -> None:
    """Elenca i file (anche nelle sottocartelle) con l'estensione indicata, con o senza punto."""
    if not estensione:
        print("Scrivi l'estensione, es. 'ext .txt'.")
        return
    estensione = "." + estensione.lstrip(".").lower()  # lstrip(".") toglie il punto iniziale, poi lo rimetto
    trovati = _cerca(base, lambda p: p.suffix.lower() == estensione, solo_file=True)
    _stampa_risultati(base, trovati, f"estensione '{estensione}'")


# ---------------- operazioni sui file ----------------

def _nome_valido(nome: str) -> bool:
    """Un nome è valido se non è vuoto, non è '.' o '..' e non contiene separatori di percorso."""
    return (bool(nome) and nome not in (".", "..")
            and "/" not in nome and "\\" not in nome)


def crea_cartella(corrente: Path) -> None:
    """Chiede un nome e crea una nuova cartella dentro la cartella corrente."""
    nome = input("Nome della nuova cartella: ").strip()
    if not _nome_valido(nome):
        print("Nome non valido: non può essere vuoto né contenere / o \\.")
        return
    try:
        (corrente / nome).mkdir()  # mkdir() crea la cartella; solleva FileExistsError se esiste già
        print(f"Cartella creata: {nome}")
    except FileExistsError:
        print(f"Esiste già un elemento chiamato '{nome}': non è stato modificato nulla.")
    except OSError as e:
        print(f"Impossibile creare la cartella: {e.strerror or e}")


def crea_file(corrente: Path) -> None:
    """Chiede un nome e crea un file vuoto dentro la cartella corrente."""
    nome = input("Nome del nuovo file: ").strip()
    if not _nome_valido(nome):
        print("Nome non valido: non può essere vuoto né contenere / o \\.")
        return
    try:
        # touch() crea il file vuoto; exist_ok=False lo fa fallire se esiste già (così non tocca file altrui)
        (corrente / nome).touch(exist_ok=False)
        print(f"File vuoto creato: {nome}")
    except FileExistsError:
        print(f"Esiste già un elemento chiamato '{nome}': non è stato modificato nulla.")
    except OSError as e:
        print(f"Impossibile creare il file: {e.strerror or e}")


def rinomina(elemento: Path) -> None:
    """Chiede un nuovo nome e rinomina il file o la cartella, senza sovrascrivere altri elementi."""
    nuovo = input(f"Nuovo nome per '{elemento.name}': ").strip()
    if not _nome_valido(nuovo):
        print("Nome non valido: non può essere vuoto né contenere / o \\.")
        return
    destinazione = elemento.with_name(nuovo)  # with_name() dà lo stesso percorso ma con un altro nome finale
    # samefile() è True se i due percorsi indicano lo stesso elemento (utile se cambio solo maiuscole)
    if destinazione.exists() and not destinazione.samefile(elemento):
        print(f"Esiste già un elemento chiamato '{nuovo}': rinomina annullata.")
        return
    try:
        elemento.rename(destinazione)  # rename() cambia il nome sul disco
        print(f"Rinominato: {elemento.name} -> {nuovo}")
    except OSError as e:
        print(f"Impossibile rinominare: {e.strerror or e}")


def _chiedi_destinazione(corrente: Path, elemento: Path, verbo: str) -> Path | None:
    """Chiede dove copiare o spostare un file e controlla che l'operazione sia sensata.

    Args:
        corrente: cartella corrente (base dei percorsi relativi scritti dall'utente).
        elemento: file da copiare o spostare.
        verbo: "copiare" o "spostare", usato nel messaggio.

    Returns:
        Il percorso finale del file, oppure None se annullato o non valido.
    """
    testo = input(f"Destinazione per {verbo} '{elemento.name}' (cartella o nuovo nome): ").strip().strip('"')
    if not testo:
        print("Nessuna destinazione indicata: operazione annullata.")
        return None
    # Unire corrente / percorso: se l'utente scrive un percorso assoluto, questo prevale su 'corrente'
    destinazione = (corrente / Path(testo).expanduser()).resolve()
    if destinazione.is_dir():
        destinazione = destinazione / elemento.name  # se indica una cartella, il file ci va dentro
    if not destinazione.parent.is_dir():
        print(f"La cartella di destinazione non esiste: {destinazione.parent}")
        return None
    if destinazione == elemento.resolve():
        print("Origine e destinazione coincidono: operazione annullata.")
        return None
    if destinazione.exists():
        print(f"Esiste già: {destinazione}")
        if not chiedi_conferma("Vuoi sovrascriverlo?"):
            print("Operazione annullata: nessun dato è stato modificato.")
            return None
    return destinazione


def copia_file(corrente: Path, elemento: Path) -> None:
    """Copia un file (non una cartella) nella destinazione scelta dall'utente."""
    if not elemento.is_file():
        print(f"'{elemento.name}' è una cartella: questa operazione copia solo file.")
        return
    destinazione = _chiedi_destinazione(corrente, elemento, "copiare")
    if destinazione is None:
        return
    try:
        shutil.copy2(elemento, destinazione)  # copy2 copia il file mantenendo anche la data di modifica
        print(f"File copiato in: {destinazione}")
    except OSError as e:
        print(f"Impossibile copiare: {e.strerror or e}")


def sposta_file(corrente: Path, elemento: Path) -> None:
    """Sposta un file (non una cartella) nella destinazione scelta dall'utente."""
    if not elemento.is_file():
        print(f"'{elemento.name}' è una cartella: questa operazione sposta solo file.")
        return
    destinazione = _chiedi_destinazione(corrente, elemento, "spostare")
    if destinazione is None:
        return
    try:
        shutil.move(str(elemento), str(destinazione))  # move sposta il file (anche tra dischi diversi)
        print(f"File spostato in: {destinazione}")
    except OSError as e:
        print(f"Impossibile spostare: {e.strerror or e}")


def elimina_file(elemento: Path) -> None:
    """Elimina un file (non una cartella) dopo una conferma esplicita."""
    if not elemento.is_file():
        print(f"'{elemento.name}' è una cartella: per sicurezza l'explorer elimina solo file.")
        return
    print(f"ATTENZIONE: '{elemento.name}' verrà eliminato in modo DEFINITIVO.")
    if not chiedi_conferma("Confermi l'eliminazione?"):
        print("Eliminazione annullata: il file non è stato toccato.")
        return
    try:
        elemento.unlink()  # unlink() elimina il file
        print(f"File eliminato: {elemento.name}")
    except OSError as e:
        print(f"Impossibile eliminare: {e.strerror or e}")


def leggi_file(elemento: Path) -> None:
    """Mostra le prime LIMITE_RIGHE righe di un file di testo (UTF-8)."""
    if not elemento.is_file():
        print(f"'{elemento.name}' è una cartella: si possono leggere solo file di testo.")
        return
    righe: List[str] = []
    try:
        with open(elemento, "r", encoding="utf-8") as file:  # "r" = lettura; with chiude il file da solo
            for riga in file:  # scorrere il file dà una riga alla volta, senza caricarlo tutto in memoria
                righe.append(riga.rstrip("\n"))  # rstrip("\n") toglie l'a capo finale
                if len(righe) > LIMITE_RIGHE:  # ne leggo una in più per sapere se ce ne sono altre
                    break
    except UnicodeDecodeError:  # succede con file binari (immagini, ecc.)
        print("Il file non sembra un file di testo (UTF-8): non lo mostro.")
        return
    except OSError as e:
        print(f"Impossibile leggere il file: {e.strerror or e}")
        return

    print(f"\n--- {elemento.name} ---")
    if not righe:
        print("(file vuoto)")
    for riga in righe[:LIMITE_RIGHE]:
        print(riga)
    if len(righe) > LIMITE_RIGHE:
        print(f"[...] mostrate solo le prime {LIMITE_RIGHE} righe")


# ---------------- ciclo dei comandi ----------------

def esplora(iniziale: Path | str) -> Path | None:
    """Ciclo dei comandi dell'explorer.

    Args:
        iniziale: cartella da cui iniziare.

    Returns:
        La cartella scelta con il comando 'seleziona' (sorgente per il backup), oppure None.
    """
    iniziale = Path(iniziale).resolve()
    corrente = iniziale
    selezionata: Path | None = None
    elementi = mostra_cartella(corrente)
    print("\nScrivi 'aiuto' per l'elenco dei comandi.")

    while True:
        riga = input("\nexplorer> ").strip()
        if not riga:
            continue
        # partition(" ") divide al primo spazio: "cd documenti" -> ("cd", " ", "documenti")
        comando, _, argomento = riga.partition(" ")
        comando = comando.lower()
        argomento = argomento.strip().strip('"').strip("'")

        if comando == "esci":
            return selezionata

        elif comando == "aiuto":
            print(AIUTO)

        elif comando == "ls":
            elementi = mostra_cartella(corrente)

        elif comando in ("su", "..") or (comando == "cd" and argomento == ".."):
            # La cartella radice ha come genitore sé stessa: lì non si può salire
            if corrente.parent == corrente:
                print("Sei già nella cartella radice: non si può salire oltre.")
            else:
                corrente = corrente.parent  # .parent = cartella che contiene quella corrente
                elementi = mostra_cartella(corrente)

        elif comando == "cd":
            scelto = scegli(argomento, elementi)
            if scelto is None:
                continue
            if not scelto.is_dir():
                print(f"'{scelto.name}' è un file, non una cartella.")
                continue
            try:
                os.listdir(scelto)  # provo a leggerla: se manca il permesso ottengo subito l'errore
            except OSError as e:
                print(f"Non posso entrare in '{scelto.name}': {e.strerror or e}")
                continue
            corrente = scelto
            elementi = mostra_cartella(corrente)

        elif comando == "home":
            corrente = Path.home()  # Path.home() = cartella personale dell'utente
            elementi = mostra_cartella(corrente)

        elif comando == "inizio":
            corrente = iniziale
            elementi = mostra_cartella(corrente)

        elif comando == "pwd":
            print(corrente.resolve())

        elif comando == "info":
            # Senza argomento mostra le informazioni della cartella corrente
            scelto = scegli(argomento, elementi) if argomento else corrente
            if scelto is not None:
                mostra_info(scelto)

        elif comando == "cerca":
            cerca_per_nome(corrente, argomento)

        elif comando == "ext":
            filtra_per_estensione(corrente, argomento)

        elif comando == "analizza":
            stampa_analisi(analizza_cartella(corrente))

        elif comando == "leggi":
            scelto = scegli(argomento, elementi)
            if scelto is not None:
                leggi_file(scelto)

        elif comando == "seleziona":
            selezionata = corrente
            print(f"Cartella selezionata come sorgente del backup: {corrente}")

        elif comando in ("nuova-cartella", "nuovo-file"):
            if comando == "nuova-cartella":
                crea_cartella(corrente)
            else:
                crea_file(corrente)
            elementi = mostra_cartella(corrente)  # aggiorno l'elenco per mostrare la novità

        elif comando in ("rinomina", "copia", "sposta", "elimina"):
            scelto = scegli(argomento, elementi)
            if scelto is None:
                continue
            if comando == "rinomina":
                rinomina(scelto)
            elif comando == "copia":
                copia_file(corrente, scelto)
            elif comando == "sposta":
                sposta_file(corrente, scelto)
            else:
                elimina_file(scelto)
            elementi = mostra_cartella(corrente)  # aggiorno l'elenco dopo la modifica

        else:
            print(f"Comando sconosciuto: '{comando}'. Scrivi 'aiuto' per l'elenco.")