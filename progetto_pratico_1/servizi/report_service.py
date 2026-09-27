"""
Generatore di statistiche/metriche di progetto a partire dai dati
attualmente presenti in memoria nel GestionaleJira.
"""


class ReportService:
    """Genera report e statistiche sui dati attualmente presenti in memoria."""

    def __init__(self, gestionale) -> None:
        self._gestionale = gestionale

    def calcola_statistiche(self) -> dict:
        """Calcola i totali per stato e la percentuale di avanzamento globale."""
        tickets = self._gestionale.elenca_ticket()
        totale = len(tickets)

        if totale == 0:
            return {
                "Totale Ticket": 0,
                "Stato": "Nessun ticket presente nel sistema",
            }

        completati = len([t for t in tickets if t.stato == "DONE"])
        in_corso = len([t for t in tickets if t.stato == "IN_PROGRESS"])
        in_review = len([t for t in tickets if t.stato == "IN_REVIEW"])
        todo = len([t for t in tickets if t.stato == "TODO"])

        percentuale = (completati / totale) * 100

        return {
            "Totale Ticket": totale,
            "TODO": todo,
            "In Progress": in_corso,
            "In Review": in_review,
            "Completati (DONE)": completati,
            "Avanzamento Globale": f"{percentuale:.1f}%",
        }