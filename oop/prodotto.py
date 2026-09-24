# Consegna

# Crea una classe Prodotto per rappresentare un prodotto di un catalogo.

# La classe deve avere:

#     Nome, prezzo e quantità.
#     Un metodo per aumentare la quantità.
#     Un metodo per ridurre la quantità.
#     Un metodo per calcolare il valore totale.
#     Una rappresentazione testuale leggibile.

# Progettazione libera

# Scegli autonomamente:

#     Valori predefiniti.
#     Controlli sui dati.
#     Messaggi restituiti.
#     Type hint e docstring.
#     Comportamento in caso di quantità insufficiente.

# Crea almeno tre prodotti e verifica che ogni oggetto mantenga il proprio stato indipendente.

class Prodotto:
    """Represents a product with a name, price and quantity"""

    def __init__(
        self,
        nome: str,
        prezzo: float = 0.0,
        quantita: int = 0
    ) -> None:
        """Initializes a product"""
        self.nome = nome
        self.prezzo = prezzo
        self.quantita = quantita

    def add(self, quantita: int) -> int:
        """Increases the product quantity"""
        self.quantita += quantita
        return self.quantita

    def subtract(self, quantita: int) -> int:
        """Decreases the product quantity if sufficient quantity is available"""
        if quantita <= self.quantita:
            self.quantita -= quantita
        else:
            print(f"Insufficient quantity for product '{self.nome}'")

        return self.quantita

    def calculate_total(self) -> float:
        """Calculates the total value of the product"""
        return self.prezzo * self.quantita

    def __str__(self) -> str:
        """Returns a readable representation of the product"""
        return (
            f"Product: {self.nome} | "
            f"Price: €{self.prezzo:.2f} | "
            f"Quantity: {self.quantita} | "
            f"Total value: €{self.calculate_total():.2f}"
        )


def main() -> None:
    """Creates products and tests their methods."""

    prodotto1 = Prodotto("Laptop", 899.99, 5)
    prodotto2 = Prodotto("Mouse", 29.99, 10)
    prodotto3 = Prodotto("Keyboard", 79.99, 3)

    print(prodotto1)
    print(prodotto2)
    print(prodotto3)

    prodotto1.add(2)
    prodotto2.subtract(3)
    prodotto3.subtract(5)

    print(prodotto1)
    print(prodotto2)
    print(prodotto3)


if __name__ == "__main__":
    main()