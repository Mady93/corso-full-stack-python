"""Percorsi predefiniti del progetto. L'utente può sempre indicarne altri."""

from __future__ import annotations  # permette hint moderni (es. Path | None) anche su Python 3.8

from pathlib import Path

# __file__ = questo file; resolve() = percorso assoluto; .parent.parent = due livelli sopra (cartella progetto)
CARTELLA_PROGETTO: Path = Path(__file__).resolve().parent.parent

# L'operatore / di pathlib unisce i pezzi di percorso in modo valido su ogni sistema operativo
CARTELLA_BACKUP: Path = CARTELLA_PROGETTO / "backup"