import re

EMAIL_PATTERN = r"[a-z0-9._%+-]+@[a-z0-9-]+(\.[a-z0-9-]+)*\.[a-z]{2,}"
MAX_LEN = 200
MAX_PASSWORD = 64


def pulisci(testo):
    return testo.strip()


def valida_email(raw):
    email = pulisci(raw).lower()
    if not email:
        return False, "Input vuoto"
    if len(email) > MAX_LEN:
        return False, "Troppo lunga"
    if ".." in email:
        return False, "Punti consecutivi non ammessi"
    if re.fullmatch(EMAIL_PATTERN, email):
        return True, "Email valida"
    return False, "Formato non valido"


def valida_password(raw):
    if not raw:
        return False, ["Input vuoto"]
    if len(raw) > MAX_PASSWORD:
        return False, [f"Massimo {MAX_PASSWORD} caratteri"]
    if not raw.isprintable():
        return False, ["Caratteri non stampabili non ammessi"]

    errori = []
    if len(raw) < 8:
        errori.append("Almeno 8 caratteri")
    if not re.search(r"[A-Z]", raw):
        errori.append("Manca una maiuscola")
    if not re.search(r"[a-z]", raw):
        errori.append("Manca una minuscola")
    if not re.search(r"\d", raw):
        errori.append("Manca un numero")
    if not re.search(r"[!@#$%^&*]", raw):
        errori.append("Manca un simbolo (!@#$%^&*)")
    if " " in raw:
        errori.append("Spazi non ammessi")
    return len(errori) == 0, errori