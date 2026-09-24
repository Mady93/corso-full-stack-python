# Consegna

# Realizza una gerarchia di classi per rappresentare animali.

# Definisci una classe base con caratteristiche comuni e almeno due classi derivate con comportamenti specifici.

# Usa:

#     Attributi comuni.
#     super().
#     Almeno un metodo ridefinito.
#     Almeno un metodo aggiunto nelle derivate.
#     isinstance() o issubclass().

# Progettazione libera

# Scegli autonomamente:

#     Nome della classe base.
#     Classi derivate.
#     Attributi e metodi.
#     Output.
#     Eventuali docstring e type hint.

# La relazione deve avere senso: una classe derivata deve essere davvero un
#  tipo specializzato della classe base.

from animal import Animal
from dog import Dog
from cat import Cat


def main() -> None:
    dog = Dog("Buddy", 3)
    cat = Cat("Luna", 2)

    dog.make_sound()
    dog.fetch()

    cat.make_sound()
    cat.climb()

    # isinstance() - check objects
    print(f"Is dog an Animal? {isinstance(dog, Animal)}")
    print(f"Is cat an Animal? {isinstance(cat, Animal)}")

    # issubclass() - check classes
    print(f"Is Dog a subclass of Animal? {issubclass(Dog, Animal)}")
    print(f"Is Cat a subclass of Animal? {issubclass(Cat, Animal)}")


    # Additional checks - not required by the assignment



    # type() - get the exact type
    print(f"Dog type: {type(dog)}")
    print(f"Cat type: {type(cat)}")

    # hasattr() - check if an attribute or method exists
    print(f"Does dog have fetch? {hasattr(dog, 'fetch')}")
    print(f"Does cat have fetch? {hasattr(cat, 'fetch')}")

    # getattr() - get an attribute or method by name
    fetch_method = getattr(dog, 'fetch')
    fetch_method()

    # callable() - check if something can be called
    print(f"Is dog.fetch callable? {callable(dog.fetch)}")
    print(f"Is dog.name callable? {callable(dog.name)}")

    # __dict__ - show object attributes
    print(f"Dog attributes: {dog.__dict__}")
    print(f"Cat attributes: {cat.__dict__}")

    # Polymorphism
    # Python determines which version of the method to execute based on the object:
    # if isinstance(animal, Dog):
    #     animal.make_sound()
    # elif isinstance(animal, Cat):
    #     animal.make_sound()

    animals = [dog, cat]

    for animal in animals:
        animal.make_sound()


if __name__ == "__main__":
    main()