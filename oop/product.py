# Consegna
# Realizza una classe Prodotto che gestisca il prezzo di un articolo commerciale:

# Stato interno: Conservi internamente il prezzo base (senza IVA) in Euro.

# Interfaccia e lettura: Permetta di leggere il prezzo base tramite una property pubblica.

# Validazione: Rifiuti qualsiasi valore del prezzo inferiore a 0.0 Euro (il prezzo non può essere negativo). 
# In caso contrario, solleva un ValueError con un messaggio appropriato.

# Calcolo e derivazione: Offra una property calcolata prezzo_ivato che restituisca il prezzo finale
# comprensivo di IVA (es. IVA al 22%).

# Incapsulamento: Garantisca una netta separazione tra lo stato interno (con underscore) 
# e l'interfaccia pubblica.


# Progettazione libera
# Scegli autonomamente:

# Il nome dell'attributo interno (es. _prezzo_base).

# Se rendere l'IVA personalizzabile o fissa al 22%.

# Se aggiungere un'altra property calcolata (es. il valore dello sconto o il prezzo in centesimi).

# L'eventuale presenza di Type Hints (float) e Docstring. 

class Product:
    """Represent a commercial product with a base price and VAT"""

    def __init__(self, price: float) -> None:
        """Initialize a product with a base price"""

        self.price = price

    @property
    def price(self) -> float:
        """Return the base price"""
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        """Set the base price, rejecting negative values"""
        if value < 0.0:
            print("Price cannot be negative")
            return

        self._price = value

    @property
    def price_with_vat(self) -> float:
        """Return the price including 22% VAT"""
        return self._price * 1.22

    @property
    def price_in_cents(self) -> int:
        """Return the base price in cents"""
        return int(self._price * 100)


def main() -> None:
    product = Product(100.0)

    print(f"Base price: €{product.price:.2f}")
    print(f"Price with VAT: €{product.price_with_vat:.2f}")
    print(f"Price in cents: {product.price_in_cents}")

    product.price = -10.0

    print(f"Base price: €{product.price:.2f}")


if __name__ == "__main__":
    main()