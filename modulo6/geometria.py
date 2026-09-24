def area_triangolo(base: float, altezza: float) -> float:
    """
    Calcola l'area di un triangolo.
    """
    return (base * altezza) / 2


def area_rettangolo(base: float, altezza: float) -> float:
    """
    Calcola l'area di un rettangolo.
    """
    return base * altezza


def area_cerchio(raggio: float) -> float:
    """
    Calcola l'area di un cerchio.
    """
    from math import pi

    return pi * raggio ** 2


def calcola_area(figura: str, *args: float) -> float:
    """
    Calcola l'area della figura geometrica indicata.
    """

    if figura == "triangolo":
        return area_triangolo(args[0], args[1])

    elif figura == "rettangolo":
        return area_rettangolo(args[0], args[1])

    elif figura == "cerchio":
        return area_cerchio(args[0])

    return 0