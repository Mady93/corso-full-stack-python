from validatori import valida_email, valida_password
from analisi import analizza_testo, estrai_dati, MAX_TESTO
from report import batch_email, batch_password, costruisci_report, salva_riga, salva_report

FILE_EMAIL = "input_prova/emails.txt"
FILE_PASSWORD = "input_prova/passwords.txt"
FILE_TESTO = "input_prova/testo.txt"

storico = {"email": [], "password": [], "testi": []}


def raccogli_elementi(etichetta):
    print(f"Inserisci {etichetta} (riga vuota per finire):")
    elementi = []
    while True:
        riga = input("> ")
        if riga == "":
            break
        elementi.append(riga)
    return elementi


def stampa_batch(risultati, riepilogo):
    for valore, ok, msg in risultati:
        esito = msg if isinstance(msg, str) else "; ".join(msg)
        print("✔" if ok else "✘", valore, "-", esito if esito else "Password valida")
    print(riepilogo)


def menu_email():
    raw = input("Email: ")
    salva_riga(FILE_EMAIL, raw)
    ok, msg = valida_email(raw)
    storico["email"].append((raw, ok, msg))
    print("✔" if ok else "✘", msg)


def menu_password():
    raw = input("Password: ")
    salva_riga(FILE_PASSWORD, raw)
    ok, errori = valida_password(raw)
    storico["password"].append(("***", ok, errori))
    print("✔ Password valida" if ok else "✘ " + "; ".join(errori))


def menu_testo():
    testo = input("Testo: ")
    analisi = analizza_testo(testo)
    if analisi is None:
        print("✘ Testo vuoto")
        return
    if len(testo.strip()) > MAX_TESTO:
        print(f"⚠ Testo troppo lungo, analizzo solo i primi {MAX_TESTO} caratteri")
    salva_riga(FILE_TESTO, testo)
    dati = estrai_dati(testo)
    storico["testi"].append((analisi, dati))
    for k, v in analisi.items():
        print(f"{k}: {v}")
    for nome, trovati in dati.items():
        print(f"{nome}: {trovati if trovati else 'assente'}")


def menu_batch():
    print("1) Email  2) Password")
    tipo = input("> ").strip()
    if tipo == "1":
        elementi = raccogli_elementi("email")
        for e in elementi:
            salva_riga(FILE_EMAIL, e)
        risultati, riepilogo = batch_email(elementi)
        storico["email"].extend(risultati)
    elif tipo == "2":
        elementi = raccogli_elementi("password")
        for p in elementi:
            salva_riga(FILE_PASSWORD, p)
        risultati, riepilogo = batch_password(elementi)
        storico["password"].extend(("***", ok, err) for _, ok, err in risultati)
    else:
        print("Scelta non valida")
        return
    stampa_batch(risultati, riepilogo)


def menu_report():
    testo = costruisci_report(storico)
    print(testo)
    salva_report("input_prova/report.txt", testo)


AZIONI = {
    "1": ("Valida email", menu_email),
    "2": ("Valida password", menu_password),
    "3": ("Analizza testo", menu_testo),
    "4": ("Batch (inserimento multiplo)", menu_batch),
    "5": ("Report", menu_report),
}


def main():
    while True:
        for k, (nome, _) in AZIONI.items():
            print(f"{k}) {nome}")
        print("0) Esci")
        scelta = input("> ").strip()
        if scelta == "0":
            break
        if scelta in AZIONI:
            AZIONI[scelta][1]()
        else:
            print("Scelta non valida")


if __name__ == "__main__":
    main()