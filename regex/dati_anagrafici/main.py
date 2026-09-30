import re
import json


def main() -> None:
    """Analizza e valida dati anagrafici tramite espressioni regolari."""

    # Dati da analizzare.
    persone = [
        "Mario Rossi, CF: RSSMRA85M01H501Z, email: mario.rossi@email.it, tel: 3331234567",
        "Anna Bianchi, CF: BNCHAN92A41F205X, email: anna.bianchi@gmail.com, tel: 3479876543",
        "Luca Verdi, CF: VRDLCU88T15L219K, email: luca.verdi@azienda.it, tel: 3295551234",
        "Paolo Blu, CF: BLUPLA90A01H501, email: paolo.blu@email.it, tel: 3212345678",
        "Giulia Neri, CF: NREGIU90B52H501A, email: giulia.neri@email, tel: 3201234567",
        "Sara Rossi, CF: RSSSRA91B41H501C, email: sara.rossi@email.it, tel: 2123456789",
        "Marco Verdi, CF: VERDI123, email: marco.verdi@email, tel: 333987654",
        "Elena Conti, CF: CNTLNE88C45F205D, email: elena.conti+test@mail.azienda.co.uk, tel: 3334567890",
        "Davide Neri, CF: NREDVD90D12H501E, email: davide.neri@email.it, tel: 333 123 4567",
        "Laura Blu, CF: BLULRA91E23L219F, email: laura.blu@gmail.com, tel: 347-123-4567",
    ]


    # PATTERN
    # Permette lettere, lettere accentate, apostrofi e spazi per nomi/cognomi composti.
    pattern_nome = re.compile(
        r"^[A-Za-zÀ-ÖØ-öø-ÿ']+(?:\s+[A-Za-zÀ-ÖØ-öø-ÿ']+)*$"
    )

    pattern_cognome = re.compile(
        r"^[A-Za-zÀ-ÖØ-öø-ÿ']+(?:\s+[A-Za-zÀ-ÖØ-öø-ÿ']+)*$"
    )

    # Codice fiscale italiano di 16 caratteri.
    pattern_cf = re.compile(
        r"^[A-Z]{6}\d{2}[A-Z]\d{2}[A-Z]\d{3}[A-Z]$"
    )

    # Email con parte locale, @, dominio ed estensione.
    pattern_email = re.compile(
        r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+"
        r"@"
        r"[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+$"
    )

    # Numero cellulare italiano di 10 cifre.
    # Sono ammessi spazi, punti, trattini e il prefisso +39.
    pattern_telefono = re.compile(
        r"^(?:\+39[\s.-]?)?3\d{2}[\s.-]?\d{3}[\s.-]?\d{4}$"
    )


    # RISULTATI
    registrate = []
    rifiutate = []

    
    # ANALISI DEI RECORD
    for persona in persone:

    
        # ESTRAZIONE
       
        # Estrae nome e cognome separandoli correttamente prima della prima virgola.
        dati_nome = re.match(
            r"^([A-Za-zÀ-ÖØ-öø-ÿ']+)\s+([A-Za-zÀ-ÖØ-öø-ÿ'\s]+?)(?=\s*,)",
            persona
        )

        # Estrae codice fiscale.
        dati_cf = re.search(
            r"CF:\s*([^,]+)",
            persona
        )

        # Estrae email.
        dati_email = re.search(
            r"email:\s*([^,]+)",
            persona
        )

        # Estrae telefono.
        dati_telefono = re.search(
            r"tel:\s*(.+)$",
            persona
        )

        # Recupera i valori estratti.
        nome = dati_nome.group(1).strip() if dati_nome else None
        cognome = dati_nome.group(2).strip() if dati_nome else None
        codice_fiscale = dati_cf.group(1).strip() if dati_cf else None
        email = dati_email.group(1).strip() if dati_email else None
        telefono = dati_telefono.group(1).strip() if dati_telefono else None

        # Lista degli errori del record.
        errori = []


        
        # VALIDAZIONE NOME
        if nome is None:
            errori.append({
                "campo": "nome",
                "valore": None,
                "formato_accettato": (
                    "Una o più lettere, comprese le lettere accentate."
                ),
                "esempio_corretto": "Mario",
                "motivo": "Il nome non è stato trovato."
            })

        elif not pattern_nome.fullmatch(nome):
            errori.append({
                "campo": "nome",
                "valore": nome,
                "formato_accettato": (
                    "Una o più lettere, comprese le lettere accentate."
                ),
                "esempio_corretto": "Mario",
                "motivo": "Il nome contiene caratteri non validi."
            })


        
        # VALIDAZIONE COGNOME
        if cognome is None:
            errori.append({
                "campo": "cognome",
                "valore": None,
                "formato_accettato": (
                    "Una o più lettere, comprese le lettere accentate."
                ),
                "esempio_corretto": "Rossi",
                "motivo": "Il cognome non è stato trovato."
            })

        elif not pattern_cognome.fullmatch(cognome):
            errori.append({
                "campo": "cognome",
                "valore": cognome,
                "formato_accettato": (
                    "Una o più lettere, comprese le lettere accentate."
                ),
                "esempio_corretto": "Rossi",
                "motivo": "Il cognome contiene caratteri non validi."
            })


        
        # VALIDAZIONE CODICE FISCALE
        if codice_fiscale is None:
            errori.append({
                "campo": "codice_fiscale",
                "valore": None,
                "formato_accettato": (
                    "16 caratteri: 6 lettere, 2 numeri, 1 lettera, "
                    "2 numeri, 1 lettera, 3 numeri e 1 lettera."
                ),
                "esempio_corretto": "RSSMRA85M01H501Z",
                "motivo": "Il codice fiscale non è stato trovato."
            })

        elif not pattern_cf.fullmatch(codice_fiscale):

            if len(codice_fiscale) != 16:
                motivo = (
                    f"Il codice fiscale contiene "
                    f"{len(codice_fiscale)} caratteri invece dei "
                    f"16 richiesti."
                )
            else:
                motivo = (
                    "La sequenza di lettere e numeri "
                    "non rispetta il formato richiesto."
                )

            errori.append({
                "campo": "codice_fiscale",
                "valore": codice_fiscale,
                "formato_accettato": (
                    "16 caratteri: 6 lettere, 2 numeri, 1 lettera, "
                    "2 numeri, 1 lettera, 3 numeri e 1 lettera."
                ),
                "esempio_corretto": "RSSMRA85M01H501Z",
                "motivo": motivo
            })


        
        # VALIDAZIONE EMAIL
        if email is None:
            errori.append({
                "campo": "email",
                "valore": None,
                "formato_accettato": (
                    "Indirizzo composto da parte locale, "
                    "@, dominio ed estensione."
                ),
                "esempio_corretto": "mario.rossi@email.it",
                "motivo": "L'indirizzo email non è stato trovato."
            })

        elif not pattern_email.fullmatch(email):

            if "@" not in email:
                motivo = "Manca il carattere @."

            elif "." not in email.split("@")[-1]:
                motivo = (
                    "Manca l'estensione del dominio, "
                    "ad esempio .it o .com."
                )

            else:
                motivo = (
                    "La struttura dell'indirizzo email "
                    "non rispetta il formato richiesto."
                )

            errori.append({
                "campo": "email",
                "valore": email,
                "formato_accettato": (
                    "Indirizzo composto da parte locale, "
                    "@, dominio ed estensione."
                ),
                "esempio_corretto": "mario.rossi@email.it",
                "motivo": motivo
            })


        
        # VALIDAZIONE TELEFONO
        if telefono is None:
            errori.append({
                "campo": "telefono",
                "valore": None,
                "formato_accettato": (
                    "Numero cellulare italiano di 10 cifre "
                    "che inizia con 3. Sono ammessi spazi, "
                    "punti, trattini e il prefisso +39."
                ),
                "esempio_corretto": "3331234567",
                "motivo": "Il numero di telefono non è stato trovato."
            })

        elif not pattern_telefono.fullmatch(telefono):

            # Rimuove i separatori per controllare il numero effettivo di cifre.
            cifre = re.sub(
                r"[\s.-]",
                "",
                telefono
            )

            # Rimuove il prefisso internazionale.
            if cifre.startswith("+39"):
                cifre = cifre[3:]

            if not cifre.isdigit():
                motivo = "Il numero contiene caratteri non validi."

            elif len(cifre) != 10:
                motivo = (
                    f"Il numero contiene {len(cifre)} cifre "
                    "invece delle 10 richieste."
                )

            elif not cifre.startswith("3"):
                motivo = (
                    "Il numero cellulare italiano "
                    "deve iniziare con 3."
                )

            else:
                motivo = (
                    "La struttura del numero "
                    "non rispetta il formato richiesto."
                )

            errori.append({
                "campo": "telefono",
                "valore": telefono,
                "formato_accettato": (
                    "Numero cellulare italiano di 10 cifre "
                    "che inizia con 3. Sono ammessi spazi, "
                    "punti, trattini e il prefisso +39."
                ),
                "esempio_corretto": "3331234567",
                "motivo": motivo
            })



        # REGISTRAZIONE O RIFIUTO
        if not errori:

            # Nasconde il telefono solamente se è valido.
            pattern_telefono_sub = re.compile(
                r"(?:\+39[\s.-]?)?3\d{2}[\s.-]?\d{3}[\s.-]?\d{4}"
            )
            testo_trasformato = pattern_telefono_sub.sub("***", persona)

            registrate.append({
                "nome": nome,
                "cognome": cognome,
                "codice_fiscale": codice_fiscale,
                "email": email,
                "telefono": telefono,
                "testo_trasformato": testo_trasformato
            })

        else:
            rifiutate.append({
                "nome": nome,
                "cognome": cognome,
                "codice_fiscale": codice_fiscale,
                "email": email,
                "telefono": telefono,
                "errori": errori
            })


    
    # RISPOSTA PER IL FRONTEND
    risposta = {
        "success": True,
        "registrate": registrate,
        "rifiutate": rifiutate
    }

    print(
        json.dumps(
            risposta,
            indent=4,
            ensure_ascii=False
        )
    )


if __name__ == "__main__":
    main()