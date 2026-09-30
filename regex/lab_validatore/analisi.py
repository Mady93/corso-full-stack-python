import re
from collections import Counter

PATTERN_DATI = {
    "email": r"[\w.+-]+@[\w-]+(?:\.[\w-]+)*\.[a-zA-Z]{2,}",
    "telefono": r"\+?\d{2,3}[ ]?\d{3}[ ]?\d{6,7}",
    "url": r"https?://[^\s\"']+",
}

# Pattern con gruppi: giorno, mese, anno
PATTERN_DATA = r"(\d{1,2})/(\d{1,2})/(\d{4})"

MAX_TESTO = 10000


def analizza_testo(testo):
    testo = testo.strip()
    if not testo:
        return None
    testo = testo[:MAX_TESTO]

    parole = re.findall(r"\w+", testo.lower())
    frasi = [f for f in re.split(r"[.!?]+", testo) if f.strip()]

    return {
        "caratteri": len(testo),
        "parole": len(parole),
        "frasi": len(frasi),
        "top_parole": Counter(parole).most_common(5),
        "parola_piu_lunga": max(parole, key=len) if parole else "",
    }


def estrai_dati(testo):
    dati = {}
    for nome, pattern in PATTERN_DATI.items():
        dati[nome] = re.findall(pattern, testo)

    # date: uso i gruppi per validare giorno e mese
    date = []
    for m in re.finditer(PATTERN_DATA, testo):
        giorno, mese, anno = int(m.group(1)), int(m.group(2)), m.group(3)
        if 1 <= giorno <= 31 and 1 <= mese <= 12:
            date.append(f"{giorno:02d}/{mese:02d}/{anno}")
    dati["data"] = date

    return dati