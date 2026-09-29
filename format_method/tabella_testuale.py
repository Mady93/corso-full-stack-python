from typing import TypeAlias

from tabella import tabella_fstring, tabella_format


# ---------- dati ----------

# Tipo usato per rappresentare una riga del magazzino.
RigaMagazzino: TypeAlias = tuple[str, str, int, float]

# Lista dei prodotti presenti nel magazzino.
DATI: list[RigaMagazzino] = [
    ("Laptop", "Informatica", 5, 899.90),
    ("Mouse", "Informatica", 42, 12.50),
    ("Scrivania", "Arredo", 8, 149.00),
    ("Sedia", "Arredo", 15, 89.99),
    ("Lampada", "Illuminazione", 30, 24.75),
    ("Zaino", "Accessori", 12, 39.90),
]


# ---------- main ----------

def main() -> None:
    """Esegue il programma."""

    # Genera la tabella usando le f-string.
    versione_f: str = tabella_fstring(DATI)

    # Genera la tabella usando .format().
    versione_format: str = tabella_format(DATI)

    # Stampa una riga vuota.
    print()

    # Stampa la prima versione.
    print("VERSIONE CON F-STRING\n")
    print(versione_f)

    # Stampa la seconda versione.
    print("\n\nVERSIONE CON .FORMAT()\n")
    print(versione_format)


# Controlla se il file viene eseguito direttamente.
if __name__ == "__main__":
    main()
