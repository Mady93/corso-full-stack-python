class Animal:
    """Represent a generic animal"""

    def __init__(self, name: str, age: int) -> None:
        """Initialize an animal with a name and an age"""

        self.name = name
        self.age = age

    def make_sound(self) -> None:
        """Make a generic animal sound"""

        print("The animal makes a sound")