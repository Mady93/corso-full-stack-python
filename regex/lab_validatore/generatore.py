import os
import random
import string

DOMINI = ["gmail.com", "uniroma2.it", "mail.co.uk", "azienda.it"]


def genera_email(n):
    emails = []
    for _ in range(n):
        nome = "".join(random.choices(string.ascii_lowercase, k=random.randint(4, 8)))
        email = f"{nome}@{random.choice(DOMINI)}"
        if random.random() < 0.4:  # 40% rotte di proposito
            email = random.choice([
                email.replace("@", ""),
                email.replace(".", ""),
                "@" + email.split("@")[1],
                email + "@",
            ])
        emails.append(email)
    return emails


def salva_lista(percorso, elementi):
    cartella = os.path.dirname(percorso)
    if cartella:
        os.makedirs(cartella, exist_ok=True)
    with open(percorso, "w", encoding="utf-8") as f:
        for e in elementi:
            f.write(e + "\n")