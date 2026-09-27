from eccezioni.eccezioni_custom import ValidazioneError, RuoloNonValidoError

RUOLI_VALIDI = ["DEV", "PM"]


class Utente:
    """Classe base per gli utenti del sistema."""

    def __init__(
        self,
        username: str,
        email: str,
        ruolo: str,
        permessi: list[str] | None = None,
        max_ticket: int = 0,
        dipartimento: str = "",
    ) -> None:

        if not username or not username.strip():
            raise ValidazioneError(
                "Lo username non puo' essere vuoto"
            )

        if not email or not email.strip():
            raise ValidazioneError(
                "L'email non puo' essere vuota"
            )

        ruolo = ruolo.upper()

        if ruolo not in RUOLI_VALIDI:
            raise RuoloNonValidoError(
                f"Ruolo '{ruolo}' non valido. "
                f"Ruoli ammessi: {', '.join(RUOLI_VALIDI)}"
            )

        if max_ticket < 0:
            raise ValidazioneError(
                "Il limite di ticket in carico non puo' essere negativo"
            )

        self._username: str = username
        self._email: str = email
        self._ruolo: str = ruolo

        self._permessi: list[str] = (
            permessi
            if permessi is not None
            else []
        )

        self._max_ticket: int = max_ticket
        self._ticket_in_carico: int = 0

        self._dipartimento: str = dipartimento

    @property
    def username(self) -> str:
        return self._username

    @property
    def email(self) -> str:
        return self._email

    @property
    def ruolo(self) -> str:
        return self._ruolo

    @property
    def max_ticket(self) -> int:
        return self._max_ticket

    @property
    def ticket_in_carico(self) -> int:
        return self._ticket_in_carico

    @property
    def dipartimento(self) -> str:
        return self._dipartimento

    def ha_permesso(self, permesso: str) -> bool:
        return permesso in self._permessi

    def get_permessi(self) -> list[str]:
        return list(self._permessi)

    def get_ruolo(self) -> str:
        return self._ruolo

    def puo_accettare_ticket(self) -> bool:
        return self._ticket_in_carico < self._max_ticket

    def impostare_limite_ticket(self, nuovo_limite: int) -> None:
        """
        Aggiorna il limite di ticket in carico. Usato dal PM per
        applicare un limite di team uguale a tutti gli sviluppatori.
        """

        if nuovo_limite < 0:
            raise ValidazioneError(
                "Il limite di ticket in carico non puo' essere negativo"
            )

        self._max_ticket = nuovo_limite

    def incrementa_ticket(self) -> None:
        self._ticket_in_carico += 1

    def decrementa_ticket(self) -> None:
        if self._ticket_in_carico > 0:
            self._ticket_in_carico -= 1

    def __str__(self) -> str:
        base = (
            f"[{self._ruolo}] "
            f"Username: {self._username} | "
            f"Email: {self._email}"
        )

        if self._ruolo == "DEV":
            base += (
                f" | Carico: "
                f"{self._ticket_in_carico}/{self._max_ticket}"
            )
        else:
            base += f" | Dipartimento: {self._dipartimento}"

        return base