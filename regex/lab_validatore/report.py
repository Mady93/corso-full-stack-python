import os

from validatori import valida_email, valida_password

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def batch_email(lista):
    risultati = [(e, *valida_email(e)) for e in lista]
    validi = sum(1 for _, ok, _ in risultati if ok)
    return risultati, {"totale": len(lista), "validi": validi, "non_validi": len(lista) - validi}


def batch_password(lista):
    risultati = [(p, *valida_password(p)) for p in lista]
    validi = sum(1 for _, ok, _ in risultati if ok)
    return risultati, {"totale": len(lista), "validi": validi, "non_validi": len(lista) - validi}


def costruisci_report(storico):
    righe = ["--- REPORT FINALE ---"]

    email = storico["email"]
    validi = sum(1 for _, ok, _ in email if ok)
    righe.append(f"\nEMAIL: {len(email)} controllate, {validi} valide, {len(email) - validi} non valide")
    for valore, ok, msg in email:
        if not ok:
            righe.append(f"  ✘ {valore} -> {msg}")

    password = storico["password"]
    validi = sum(1 for _, ok, _ in password if ok)
    righe.append(f"\nPASSWORD: {len(password)} controllate, {validi} valide, {len(password) - validi} non valide")
    for i, (_, ok, errori) in enumerate(password, 1):
        if not ok:
            righe.append(f"  ✘ password #{i}: " + "; ".join(errori))

    testi = storico["testi"]
    righe.append(f"\nTESTI: {len(testi)} analizzati")
    for i, (analisi, dati) in enumerate(testi, 1):
        righe.append(f"  Testo {i}: {analisi['parole']} parole, {analisi['frasi']} frasi")
        for nome, trovati in dati.items():
            righe.append(f"    {nome}: {', '.join(trovati) if trovati else 'assente'}")

    return "\n".join(righe)


def salva_riga(percorso, valore):
    percorso_completo = os.path.join(BASE_DIR, percorso)
    os.makedirs(os.path.dirname(percorso_completo), exist_ok=True)
    with open(percorso_completo, "a", encoding="utf-8") as f:
        f.write(valore + "\n")
    print(f"(salvato in {percorso_completo})")


def salva_report(percorso, testo):
    percorso_completo = os.path.join(BASE_DIR, percorso)
    with open(percorso_completo, "w", encoding="utf-8") as f:
        f.write(testo)
    print(f"(salvato in {percorso_completo})")