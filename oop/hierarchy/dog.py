from typing import override
from animal import Animal

class Dog(Animal):
    """Represent a dog"""

    def __init__(self, name: str, age: int) -> None:
        """Initialize a dog with a name and an age"""

        super().__init__(name, age)

    @override
    def make_sound(self) -> None:
        """Make the dog sound"""

        print("Woof!")

    def fetch(self) -> None:
        """Make the dog fetch the ball"""
        
        print(f"{self.name} is fetching the ball")