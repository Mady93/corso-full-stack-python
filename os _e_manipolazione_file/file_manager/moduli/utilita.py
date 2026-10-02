"""Funzioni di supporto condivise: formattazione e domande all'utente."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path


def formatta_dimensione(byte: int) -> str:
    """Converte un numero di byte in testo leggibile.

    Args:
        byte: dimensione in byte.

    Returns:
        Testo con unità adatta, es. 1536 -> '1.5 KB'.
    """
    if byte < 1024:
        return f"{byte} B"
    valore = float(byte)
    for unita in ("KB", "MB", "GB", "TB"):
        valore /= 1024  # a ogni giro passo all'unità successiva (dividendo per 1024)
        if valore < 1024 or unita == "TB":
            return f"{valore:.1f} {unita}"  # .1f = un solo decimale
    return f"{byte} B"  # non si arriva mai qui: serve solo a soddisfare il controllo dei tipi


def formatta_data(timestamp: float) -> str:
    """Converte un timestamp (secondi dal 1970) in 'AAAA-MM-GG HH:MM:SS'."""
    # fromtimestamp: secondi -> data/ora locale; strftime: data/ora -> testo col formato indicato
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


def chiedi_conferma(messaggio: str) -> bool:
    """Chiede s/n finché la risposta non è valida.

    Returns:
        True se l'utente conferma, False se rifiuta.
    """
    while True:
        # strip() toglie gli spazi ai bordi; lower() rende tutto minuscolo
        risposta = input(f"{messaggio} (s/n): ").strip().lower()
        if risposta in ("s", "si", "sì"):
            return True
        if risposta in ("n", "no"):
            return False
        print("Rispondi con 's' oppure 'n'.")


def chiedi_percorso(messaggio: str, default: Path | str | None = None) -> Path | None:
    """Chiede un percorso all'utente.

    Args:
        messaggio: testo della domanda.
        default: percorso usato se l'utente preme solo Invio.

    Returns:
        Path assoluto, oppure None se non c'è risposta né default.
    """
    suggerimento = f" [Invio = {default}]" if default else ""
    # strip('"') e strip("'") tolgono le virgolette che compaiono quando si trascina un percorso nel terminale
    testo = input(f"{messaggio}{suggerimento}: ").strip().strip('"').strip("'")
    if not testo:
        return Path(default).resolve() if default else None
    # expanduser() trasforma "~" nella cartella home; resolve() dà il percorso assoluto e pulito
    return Path(testo).expanduser().resolve()