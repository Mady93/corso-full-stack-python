"""Configurazione specifica della rubrica."""

import os

# Database della rubrica: si può cambiare con la variabile d'ambiente RUBRICA_DB (la usano i test)
NOME_DB: str = os.getenv("RUBRICA_DB", "rubrica")