# Funzioni di utilità usate per costruire la tabella.


def calcola_totale_generale(dati) -> float:
    """Calcola il valore totale di tutti i prodotti."""

    return sum(
        qta * prezzo
        for _, _, qta, prezzo in dati
    )


def calcola_quantita_totale(dati) -> int:
    """Calcola la quantità complessiva dei prodotti."""

    return sum(
        qta
        for _, _, qta, _ in dati
    )


def calcola_totale_riga(qta: int, prezzo: float) -> float:
    """Calcola il valore totale di una singola riga."""

    return qta * prezzo


def calcola_quota(totale: float, totale_generale: float) -> float:
    """Calcola la percentuale del totale di una riga sul totale generale."""

    return totale / totale_generale