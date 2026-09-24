#calcolare l'anno di nascita

from datetime import datetime

anno_corrente = datetime.now().year
anno_nascita = input("Inserisci la data di nascita (es. 01/01/1990 oppure 01.01.1990): ")
anno_nascita = anno_nascita.replace(".", "/")
anno_nascita_data = datetime.strptime(anno_nascita, "%d/%m/%Y")

print(f"Il tuo anno di nascita è: anno corrente {anno_corrente} - anno di nascita {anno_nascita_data.year} = {anno_corrente - anno_nascita_data.year} anni.")