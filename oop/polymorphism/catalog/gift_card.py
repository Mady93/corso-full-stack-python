"""GiftCard: a DUCK TYPING example.
 
This class does NOT inherit from Product — it has no relationship at all
with the class hierarchy. But it exposes the same two methods, ``cost()``
and ``describe()``, with the same signatures. "If it walks like a duck and
quacks like a duck..." — any code written to work with Product objects
(like the loop in main.py) will happily accept a GiftCard too, purely
because it has the right shape, not because of what it inherits from.
"""
 
 
class GiftCard:
    def __init__(self, code: str, amount: float) -> None:
        # GiftCard non eredita da Product, ma espone gli stessi metodi
        # necessari per il duck typing
        if not code:
            raise ValueError("Gift card code cannot be empty")
        if amount <= 0:
            raise ValueError("Gift card amount must be positive")
        self._code = code      # stato interno
        self._amount = amount  # stato interno
 
    @property
    def code(self) -> str:
        # Getter: permette di leggere il codice dall'esterno
        return self._code
 
    @property
    def amount(self) -> float:
        # Getter: permette di leggere l'importo dall'esterno
        return self._amount
 
    def cost(self) -> float:
        # Le gift card non hanno tasse
        return self._amount
 
    def describe(self) -> str:
        return f"Gift card {self._code}"
 
    def __str__(self) -> str:
        return f"{self.describe()} - ${self.cost():.2f}"
 
    def __repr__(self) -> str:
        return f"GiftCard(code={self._code!r}, amount={self._amount!r})"