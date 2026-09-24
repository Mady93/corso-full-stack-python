from typing import override
from animal import Animal

class Cat(Animal):
    """Represent a cat."""

    def __init__(self, name: str, age: int) -> None:
        """Initialize a cat with a name and an age"""

        super().__init__(name, age)

    @override
    def make_sound(self) -> None:
        """Make the cat sound"""

        print("Meow!")

    def climb(self) -> None:
        """Make the cat climb"""

        print(f"{self.name} is climbing")