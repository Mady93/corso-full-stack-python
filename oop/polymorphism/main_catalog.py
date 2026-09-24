# Mini progetto: catalogo polimorfico
# Consegna

# Realizza un piccolo catalogo con almeno due classi diverse che espongano lo stesso metodo, per esempio descrivi(), costo() o area().

# Crea una lista di oggetti diversi e percorri la lista chiamando lo stesso metodo su ogni elemento.

# Implementa anche __str__ e __repr__ per almeno una delle classi.
# Progettazione libera

# Puoi scegliere il dominio:

#     Forme geometriche.
#     Mezzi di trasporto.
#     Prodotti di un catalogo.
#     Animali.
#     Strumenti musicali.

# L'obiettivo è usare una stessa interfaccia con oggetti diversi e produrre rappresentazioni leggibili e tecniche.


"""
Test file: builds a catalog and demonstrates, step by step:
 
  - class hierarchy (Product -> Book / Electronic / FoodItem)
  - polymorphism (same method, different behavior per class)
  - __str__ vs __repr__
  - duck typing (GiftCard, unrelated to the hierarchy)
  - @override, __init__, super()
  - isinstance() and issubclass()
  - encapsulation (public API <- property <- internal state)
"""







# Spiegazione del progetto

# Ho scelto di realizzare un catalogo di prodotti usando una gerarchia di classi.
# La classe Product è la classe base astratta e contiene le caratteristiche e i comportamenti 
# comuni a tutti i prodotti. 
# Da Product derivano Book, Electronic e FoodItem. Ho scelto questa struttura per usare l'ereditarietà, 
# super() e @override.
# Le classi figlie ridefiniscono i metodi cost() e describe(), ognuna con un comportamento diverso. 
# In questo modo posso usare gli stessi metodi su oggetti diversi e dimostrare il polimorfismo.
# Ho aggiunto anche GiftCard, che non eredita da Product, ma possiede comunque i metodi cost() e describe(). 
# L'ho inserita per dimostrare il duck typing: Python può usare l'oggetto perché offre i metodi richiesti, 
# anche se non appartiene alla gerarchia.
# Ho usato @property per esporre il public API e mantenere separato lo stato interno, 
# ad esempio _name e _base_price. Questo serve a dimostrare l'incapsulamento.
# Infine, ho implementato __str__ per una rappresentazione leggibile dell'oggetto 
# e __repr__ per una rappresentazione più tecnica. Nel main.py uso una lista di oggetti diversi 
# e un unico ciclo per dimostrare concretamente il polimorfismo, oltre a isinstance() e issubclass() 
# per verificare la gerarchia.
 
from catalog import Product, Book, Electronic, FoodItem, GiftCard
 
 
def main() -> None:
    """Build the catalog and demonstrate the main OOP concepts"""
    # Book, Electronic e FoodItem appartengono alla gerarchia di Product
    catalog = [
        Book("The Name of the Rose", 15.00, "Umberto Eco", 512),
        Electronic("Wireless Headphones", 49.90, 24),
        FoodItem("Artisan Pasta", 3.50, 180),
        # GiftCard non eredita da Product, ma funziona grazie al duck typing
        GiftCard("GC-1001", 25.00),
    ]
 
    print("=== PRODUCT CATALOG ===\n")
    total: float = 0.0
 
    # Polimorfismo: uso gli stessi metodi su oggetti di classi diverse
    # Ogni classe esegue il metodo con il proprio comportamento
    for item in catalog:
        print(item.describe())
        print(f"  Final cost: ${item.cost():.2f}")
        print(f"  str()  -> {item}")
        print(f"  repr() -> {repr(item)}")
        print()
        total += item.cost()
 
    print(f"Catalog total: ${total:.2f}\n")
 
    # Controllo se un oggetto appartiene alla gerarchia
    book = catalog[0]
    gift_card = catalog[3]
 
    print("=== isinstance() / issubclass() checks ===")
    print(f"isinstance(book, Product)       -> {isinstance(book, Product)}")
    print(f"isinstance(gift_card, Product)  -> {isinstance(gift_card, Product)}")
    print(f"issubclass(Book, Product)       -> {issubclass(Book, Product)}")
    print(f"issubclass(GiftCard, Product)   -> {issubclass(GiftCard, Product)}")
    print()
 
    # Incapsulamento: modifico lo stato interno attraverso la public API
    # Il setter controlla il valore e blocca quello non valido
    # print("=== Encapsulation checks ===")
    # try:
    #     book.name = ""
    # except ValueError as e:
    #     print(f"[Check OK] Invalid assignment blocked: {e}")
 
    # Anche durante la costruzione l'assegnazione passa dal setter
    # try:
    #     Book("", 10, "Author", 100)
    # except ValueError as e:
    #     print(f"[Check OK] Invalid construction blocked: {e}")

if __name__ == "__main__":
    main()