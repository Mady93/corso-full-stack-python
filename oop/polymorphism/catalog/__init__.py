"""Catalog package: the Product class hierarchy plus a duck-typed GiftCard"""

# Importo le classi così posso usarle direttamente dal package "catalog"
from .product import Product
from .book import Book
from .electronic import Electronic
from .food_item import FoodItem
from .gift_card import GiftCard


# Definisco quali classi vengono considerate parte della public API del package.
__all__ = ["Product", "Book", "Electronic", "FoodItem", "GiftCard"]