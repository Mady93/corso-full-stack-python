import csv

def leggi_csv(percorso: str) -> tuple[list[tuple], list[dict]]:
    """Restituisce (righe_valide, righe_scartate)."""
    valide = []
    scartate = []

    with open(percorso, newline="", encoding="utf-8") as f:
        lettore = csv.DictReader(f)  # usa la prima riga come intestazione
        for numero, riga in enumerate(lettore, start=2):  # 2 = prima riga dati
            nome = riga["nome"].strip()
            cognome = riga["cognome"].strip()
            classe = riga["classe"].strip().upper()
            email = riga["email"].strip().lower()

            errore = valida_riga(nome, cognome, classe, email)
            if errore:
                scartate.append({"riga": numero, "motivo": errore, **riga})
            else:
                valide.append((nome, cognome, classe, email))

    return valide, scartate


def valida_riga(nome, cognome, classe, email) -> str | None:
    if not nome or not cognome:
        return "nome o cognome vuoto"
    if "@" not in email:
        return "email non valida"
    if len(classe) > 10:
        return "classe troppo lunga"
    return None