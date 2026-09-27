"""
Configurazione condivisa del team.

Tenuta separata da GestionaleJira perche' la registrazione degli utenti
avviene PRIMA della scelta del progetto (schermata_autenticazione), quando
un'istanza di GestionaleJira non esiste ancora. Questo oggetto viaggia
sia nella fase di login/registrazione sia dentro GestionaleJira, cosi'
il valore resta unico e condiviso in tutta l'applicazione.
"""


class ConfigurazioneTeam:
    """Impostazioni di team decise dal Project Manager."""

    def __init__(self, limite_ticket_dev: int = 3) -> None:
        self.limite_ticket_dev: int = limite_ticket_dev