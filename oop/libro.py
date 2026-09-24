# Consegna

# Crea una classe Libro con:

#     Attributi per titolo, autore e numero di pagine.
#     Un metodo che stampa una descrizione del libro.
#     Un metodo che indica se il libro è breve o lungo secondo una soglia scelta da te.

# Crea almeno due oggetti Libro con valori diversi e chiama i loro metodi.
# Progettazione

# Scegli autonomamente:

#     Parametri obbligatori e valori predefiniti.
#     Testo dei messaggi.
#     Soglia per la classificazione.
#     Eventuali type hint e docstring.

# L'obiettivo è distinguere chiaramente classe, attributi, metodo, istanza e stato indipendente degli oggetti.

class Libro:
    """Represents a book with title, author, description and number of pages"""

    def __init__(
        self,
        titolo: str,
        autore: str,
        descrizione_breve: str,
        numero_pagine: int = 0
    ):
        """Initializes a book"""
        self.titolo = titolo
        self.autore = autore
        self.descrizione_breve = descrizione_breve
        self.numero_pagine = numero_pagine

    def descrizione(self) -> None:
        """Prints the short description of the book"""
        
        # # prima lettera maiuscola + tutto il resto minuscolo
        # descrizione = descrizione.capitalize()

        # # prende il primo carattere e lo rende minuscolo
        # descrizione = descrizione[0].lower() + descrizione[1:]

        descrizione = self.descrizione_breve.lower()

        print(
        f"The book '{self.titolo}', written by {self.autore}, "
        f"is about {descrizione}"
    )

    def classificazione(self, soglia: int = 200) -> None:
        """Indicates whether the book is short or long based on the threshold."""
        if self.numero_pagine < soglia:
            print(f"The book '{self.titolo}' by {self.autore} has {self.numero_pagine} pages, so it is short")
        else:
            print(f"The book '{self.titolo}' by {self.autore} has {self.numero_pagine} pages, so it is long")


def main() -> None:
    romanzo_distopico = Libro(
        "1984",
        "George Orwell",
        "A dystopian novel about a society controlled by a totalitarian regime",
        328
    )

    philosophical = Libro(
        "The Little Prince",
        "Antoine de Saint-Exupéry",
        "A story that explores friendship, love and the meaning of relationships",
        96
    )

    romanzo_distopico.descrizione()
    romanzo_distopico.classificazione()

    philosophical.descrizione()
    philosophical.classificazione(100)


if __name__ == "__main__":
    main()








#     class Computer:
#     def __init__(self, modello):
#         self.modello = modello
#         # Creazione di un'istanza della classe interna
#         self.cpu = self.CPU() 

#     def mostra_info(self):
#         return f"Computer: {self.modello}, CPU: {self.cpu.marca}"

#     # Classe dentro la classe
#     class CPU:
#         def __init__(self):
#             self.marca = "Intel"
#             self.velocita = "3.5 GHz"

# # Utilizzo
# pc = Computer("Asus")
# print(pc.mostra_info())          # Output: Computer: Asus, CPU: Intel
# print(pc.cpu.velocita)           # Output: 3.5 GHz

# # È anche possibile istanziare direttamente la classe interna usando la classe esterna
# processore = Computer.CPU()
# print(processore.marca)          # Output: Intel 