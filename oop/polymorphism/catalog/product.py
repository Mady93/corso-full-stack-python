"""Abstract base class: defines the common interface for all products.
 
This module is the top of the CLASS HIERARCHY (Product -> Book / Electronic
/ FoodItem) and demonstrates ENCAPSULATION:
 
    public API  <-  property  <-  internal state
 
The internal state (``_name``, ``_base_price``) is stored on "protected"
attributes (single underscore, a convention meaning "internal use only").
External code never touches them directly: it goes through the public
``name`` / ``base_price`` properties, which validate every read/write.
"""
 
from abc import ABC, abstractmethod
 
 
class Product(ABC):
    def __init__(self, name: str, base_price: float):
        # __init__ assegna attraverso i setter pubblici sottostanti,
        # quindi la validazione viene eseguita anche al momento della costruzione dell'oggetto
        self.name = name
        self.base_price = base_price


    # API pubblica (property) che proteggono lo stato interno
    @property
    def name(self) -> str:
        """Public getter: read-only view of the internal ``_name``"""
        return self._name
 
    @name.setter
    def name(self, value: str) -> None:
        """Public setter: validates before touching the internal state"""
        if not value or not value.strip():
            raise ValueError("Product name cannot be empty")
        self._name = value  # stato interno, non viene mai usato direttamente dall'esterno
 
    @property
    def base_price(self) -> float:
        return self._base_price
 
    @base_price.setter
    def base_price(self, value: float) -> None:
        if value < 0:
            raise ValueError("Base price cannot be negative")
        self._base_price = value  # stato interno, non viene mai usato direttamente dall'esterno
 

    # Interfaccia che ogni classe figlia DEVE implementare (imposto da ABC)
    @abstractmethod
    def cost(self) -> float:
        """Final price, tax included. Each subclass computes it differently"""
        raise NotImplementedError
 
    @abstractmethod
    def describe(self) -> str:
        """Human-readable description of the product"""
        raise NotImplementedError


    # Metodi dunder: rappresentazione leggibile (__str__) vs tecnica (__repr__)
    def __str__(self) -> str:
        return f"{self.name} - ${self.cost():.2f}"
 
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r}, base_price={self.base_price!r})"