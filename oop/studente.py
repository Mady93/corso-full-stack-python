# Crea una classe Studente per gestire il libretto voti di uno studente universitario.

# La classe deve avere:

# Attributi: nome, matricola, una lista di esami sostenuti (vuota all'inizio).
# Un metodo per aggiungere un esame, con nome dell'esame, voto (da 18 a 30, con possibilità di lode) e crediti formativi (CFU). Deve controllare che il voto sia valido (tra 18 e 30) e sollevare un'eccezione se non lo è.
# Un metodo per calcolare la media aritmetica dei voti.
# Un metodo per calcolare la media ponderata rispetto ai CFU (cioè pesata in base ai crediti di ogni esame).
# Un metodo per calcolare il totale dei CFU conseguiti.
# Un metodo per trovare il voto più alto e quello più basso tra gli esami sostenuti.
# Una rappresentazione testuale leggibile che mostri nome, matricola, numero di esami e media ponderata.
# Requisiti aggiuntivi (parte più complessa)
# Ogni esame deve essere memorizzato come dizionario (o tupla) con chiavi: nome, voto, cfu, non come valori sparsi.
# Gestisci il caso della lode: internamente il voto può essere salvato come 31 per rappresentare "30 e lode", ma nella stampa deve apparire come "30L".
# Solleva un'eccezione personalizzata VotoNonValidoError se si prova ad aggiungere un voto fuori range (es. 35 o 10).
# Un metodo esami_superati_con_lode() che restituisca l'elenco degli esami con lode.
# Bonus facoltativo: un metodo proiezione_laurea(cfu_totali_richiesti=180) che, dato il totale di CFU richiesti per laurearsi, restituisca quanti CFU mancano ancora. 


# Un metodo bonus_laurea() che calcoli il bonus di laurea
# sulla media aritmetica e sulla media ponderata.

# Per ogni esame superato con lode viene aggiunto un bonus
# di 0,5 punti alla votazione di partenza.

# Il bonus massimo complessivo è di 3 punti,
# corrispondenti a un massimo di 6 lodi.

# Il bonus deve essere applicato sia alla votazione di partenza
# calcolata dalla media aritmetica sia a quella calcolata
# dalla media ponderata.

# Il metodo deve restituire:
# - la votazione di partenza aritmetica con il bonus
# - la votazione di partenza ponderata con il bonus





# class VotoNonValidoError(Exception):
#     """Raised when a grade is outside the valid range"""
#     pass


class Studente:
    """Represents a university student and their exam record"""

    def __init__(
        self,
        nome: str,
        matricola: str
    ) -> None:
        """Initializes a student."""
        self.nome = nome
        self.matricola = matricola
        self.esami = []

    def aggiungi_esame(
        self,
        nome_esame: str,
        voto: int,
        cfu: int,
        lode: bool = False
    ) -> None:
        """Adds an exam to the student's record"""

        # if voto < 18 or voto > 30:
        #     raise VotoNonValidoError(
        #         f"Invalid grade: {voto}. The grade must be between 18 and 30"
        #     )

        # il voto deve stare tra 18 e 30
        if voto < 18 or voto > 30:

            # stampa "Voto non valido: X. Il voto deve essere tra 18 e 30"
            print(
                f"Invalid grade: {voto}. "
                f"The grade must be between 18 and 30"
            )
             # esco dalla funzione, l'esame NON viene salvato
            return

        # i cfu devono essere positivi
        if cfu <= 0:
            # stampa "I CFU devono essere maggiori di 0"
            print("CFU must be greater than 0")

            # esco, esame NON salvato
            return

        # if cfu <= 0:
        #     raise ValueError("CFU must be greater than 0")

        # if lode and voto != 30:
        #     raise VotoNonValidoError(
        #         "Honors can only be assigned to a grade of 30"
        #     )

        # la lode è ammessa solo se il voto è 30
        if lode and voto != 30:

            # stampa "La lode può essere assegnata solo con voto 30"
            print("Honors can only be assigned to a grade of 30")

            # esco, esame NON salvato
            return
        
        if lode:
            # 31 è un trucco interno: rappresenta "30 e lode"
            voto = 31

        esame = {
            "nome": nome_esame,
            "voto": voto,
            "cfu": cfu
        }

        # aggiungo il dizionario alla lista esami
        self.esami.append(esame)

    def media_aritmetica(self) -> float:
        """Calculates the arithmetic mean of the grades"""

        # se non ci sono esami
        if not self.esami:

            # media = 0
            return 0.0

         # per il calcolo, il 31 (lode) conta come 30
        totale_voti = sum(
            30 if esame["voto"] == 31 else esame["voto"]
            for esame in self.esami
        )

        # media = somma voti / numero esami
        return totale_voti / len(self.esami)

    def media_ponderata(self) -> float:
        """Calculates the weighted average based on CFU"""

        # se non ci sono esami
        if not self.esami:

            # media = 0
            return 0.0

        # anche qui 31 -> 30 per il calcolo
        # moltiplico il voto per i cfu dell'esame (peso)
        totale_pesato = sum(
            (30 if esame["voto"] == 31 else esame["voto"])
            * esame["cfu"]
            for esame in self.esami
        )

        # media pesata = somma pesata / totale cfu
        return totale_pesato / self.totale_cfu()


    def totale_cfu(self) -> int:
        """Calculates the total number of CFU earned"""

        # somma tutti i cfu di tutti gli esami
        return sum(
            esame["cfu"]
            for esame in self.esami
        )

    def voto_massimo(self) -> int | None:
        """Returns the highest grade"""

        # se non ci sono esami
        if not self.esami:
            # ritorno None (non una stringa), più facile da controllare dopo
            return None

        # ritorno il voto più alto GREZZO (può essere anche 31)
        return max(
            esame["voto"]
            for esame in self.esami
        )

    def voto_minimo(self) -> int | None:
        """Returns the lowest grade"""

        # se non ci sono esami
        if not self.esami:
            # ritorno None
            return None

        # ritorno il voto più basso grezzo
        return min(
            esame["voto"]
            for esame in self.esami
        )


    def esami_superati_con_lode(self) -> list:
        """Returns the names of exams passed with honors"""

        # prendo solo i nomi degli esami con lode (voto salvato come 31)
        return [
            esame["nome"]
            for esame in self.esami
            if esame["voto"] == 31
        ]

    def bonus_laurea(self) -> tuple:
        """Calculates the graduation grade with the honors bonus."""

        # conto quante lodi ho totalizzato
        numero_lodi = len(self.esami_superati_con_lode())

        # ogni lode vale 0.5 punti di bonus
        # ma il bonus totale non può superare 3 punti (max 6 lodi)
        bonus = min(
            numero_lodi * 0.5,
            3.0
        )

        # converto la media aritmetica da base 30 a base 110, poi aggiungo il bonus
        voto_aritmetico = (self.media_aritmetica() / 30) * 110 + bonus

        # converto la media ponderata da base 30 a base 110, poi aggiungo il bonus
        voto_ponderato = (self.media_ponderata() / 30) * 110 + bonus

        # ritorno entrambi i valori come tupla
        return voto_aritmetico, voto_ponderato

    def proiezione_laurea(
        self,
        cfu_totali_richiesti: int = 180
    ) -> int:
        """Calculates the CFU still needed to graduate"""

        # non voglio mai un numero negativo di cfu mancanti
        # cfu richiesti - cfu già fatti = cfu mancanti
        return max(
            0,
            cfu_totali_richiesti - self.totale_cfu()
        )

    def __str__(self) -> str:
        """Returns a readable representation of the student"""

        return (
            f"Student: {self.nome} | "
            f"Student ID: {self.matricola} | "

            # stampa quanti esami ha sostenuto
            f"Exams: {len(self.esami)} | "

            # stampa la media ponderata con 2 decimali
            f"Weighted average: {self.media_ponderata():.2f}"
        )


def main() -> None:
    """Creates a student and tests the methods"""

    # creo uno studente di prova
    studente = Studente("Mario Rossi", "123456")

    # aggiungo un esame normale (voto 28, 9 cfu)
    studente.aggiungi_esame("Matematica", 28, 9)

    # questo esame ha la lode -> voto salvato come 31
    studente.aggiungi_esame(
        "Programmazione",
        30,
        12,
        lode=True
    )
    studente.aggiungi_esame("Database", 24, 6)
    studente.aggiungi_esame("Inglese", 18, 6)

    # stampa la riga riassuntiva (usa __str__)
    print(studente)

    # stampa "Media aritmetica: X.XX"
    print(f"Arithmetic average: {studente.media_aritmetica():.2f}")

    # stampa "Media ponderata: X.XX"
    print(f"Weighted average: {studente.media_ponderata():.2f}")

    # stampa "Totale CFU: X"
    print(f"Total CFU: {studente.totale_cfu()}")

    # stampa il voto massimo, convertendo 31 in "30L" solo qui
    print(
        f"Highest grade: "
        f"{'30L' if studente.voto_massimo() == 31 else studente.voto_massimo()}"
        )

    # stampa il voto minimo, convertendo 31 in "30L" solo qui
    print(
        f"Lowest grade: "
        f"{'30L' if studente.voto_minimo() == 31 else studente.voto_minimo()}"
    )

    # stampa la lista dei nomi degli esami con lode
    print(
        f"Exams with honors: "
        f"{studente.esami_superati_con_lode()}"
    )

    # stampa quanti cfu mancano per laurearsi (default 180)
    print(
        f"CFU missing for graduation: "
        f"{studente.proiezione_laurea()}"
    )

    # voto_aritmetico = media aritmetica + bonus lodi; voto_ponderato = media ponderata + bonus lodi
    # bonus_laurea() ritorna una tupla (aritmetica+bonus, ponderata+bonus): qui la spacchetto in 2 variabili separate
    voto_aritmetico, voto_ponderato = studente.bonus_laurea()

    # stampa il voto di laurea calcolato dalla media aritmetica + bonus
    print(
        f"Graduation grade (arithmetic average): "
        f"{voto_aritmetico:.2f}"
    )

    # stampa il voto di laurea calcolato dalla media ponderata + bonus
    print(
        f"Graduation grade (weighted average): "
        f"{voto_ponderato:.2f}"
    )

    # try:
    #     studente.aggiungi_esame("Fisica", 35, 9)
    # except VotoNonValidoError as errore:
    #     print(f"Error: {errore}")


    # test: voto 35 non valido -> stampa il messaggio d'errore e non lo aggiunge
    studente.aggiungi_esame("Fisica", 35, 9)


if __name__ == "__main__":
    main()