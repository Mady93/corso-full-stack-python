import json
from datetime import datetime
from zoneinfo import ZoneInfo

from models.api_response_success import ApiResponseSuccess


def gestisci_successo(
    data=None,
    message: str = "Operation completed successfully",
    status: int | None = None,
    path: str | None = None,
) -> None:
    """Handle a successful operation and build a structured response"""

    # Recupero la data e l'ora italiane senza millisecondi
    try:
        timestamp = datetime.now(
            ZoneInfo("Europe/Rome")
        ).strftime("%d-%m-%Y %H:%M:%S")

    except Exception:
        timestamp = datetime.now().astimezone().strftime(
            "%d-%m-%Y %H:%M:%S"
        )

    # Creo il modello standard della risposta
    risposta = ApiResponseSuccess(
        timestamp=timestamp,
        status=status,
        data=data,
        message=message,
        trace=None,
        path=path,
    )

    # Simulo una vera response JSON da API
    print(
        json.dumps(
            risposta.to_dict(),
            indent=4,
            ensure_ascii=False,
        )
    )