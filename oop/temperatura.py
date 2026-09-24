# Mini progetto: classe Temperatura
# Consegna

# Realizza una classe Temperatura che:

#     Conservi internamente il valore in Celsius.
#     Permetta di leggere la temperatura tramite una property.
#     Rifiuti valori inferiori allo zero assoluto.
#     Calcoli Celsius e Fahrenheit tramite property o metodi.
#     Offra un'interfaccia pubblica chiara.

# Progettazione libera

# Scegli autonomamente:

#     Nome dell'attributo interno.
#     Tipo di errore o messaggio.
#     Uso di setter e getter.
#     Formattazione dei risultati.
#     Eventuali docstring e type hint.

# L'obiettivo è applicare underscore, property, validazione e separazione tra interfaccia pubblica e stato interno.

class Temperatura:
    """Represents a temperature stored internally in Celsius"""

    def __init__(self, celsius: float) -> None:
        """Initializes a temperature"""

        self.celsius = celsius

    @property
    def celsius(self) -> float:
        """Returns the temperature in Celsius"""
        return self._celsius

    @celsius.setter
    def celsius(self, valore: float) -> None:
        """Sets the temperature in Celsius"""
        if valore < -273.15:
            raise ValueError("Temperature cannot be below absolute zero")
        self._celsius = valore

    @property
    def fahrenheit(self) -> float:
        """Returns the temperature in Fahrenheit"""
        return (self._celsius * 9 / 5) + 32


def main() -> None:
    temperatura = Temperatura(25)

    print(f"Celsius: {temperatura.celsius} °C")
    print(f"Fahrenheit: {temperatura.fahrenheit} °F")

    temperatura.celsius = 30

    print(f"Celsius: {temperatura.celsius} °C")
    print(f"Fahrenheit: {temperatura.fahrenheit} °F")


if __name__ == "__main__":
    main()

