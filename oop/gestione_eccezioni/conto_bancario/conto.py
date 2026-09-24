from exceptions.app_exception import ( SaldoInsufficienteError, ValidationError )

class Conto:
    """Represent a bank account"""

    def __init__(
        self,
        intestatario: str,
        saldo: float = 0.0,
    ) -> None:
        """Initialize a bank account"""

        if saldo < 0:
            raise ValidationError(
                "The initial balance cannot be negative"
            )

        self._intestatario = intestatario
        self._saldo = saldo

    @property
    def intestatario(self) -> str:
        """Return the account holder"""
        return self._intestatario

    @property
    def saldo(self) -> float:
        """Return the current balance"""
        return self._saldo

    def deposita(self, importo: float) -> None:
        """Deposit money into the account"""

        if importo <= 0:
            raise ValidationError(
                "The deposit amount must be greater than zero"
            )

        self._saldo += importo

    def preleva(self, importo: float) -> None:
        """Withdraw money from the account."""

        if importo <= 0:
            raise ValidationError(
                "The withdrawal amount must be greater than zero"
            )

        if importo > self._saldo:
            raise SaldoInsufficienteError(
                "Withdrawal rejected: insufficient funds"
            )

        self._saldo -= importo