import json
import traceback
from datetime import datetime
from types import TracebackType
from zoneinfo import ZoneInfo

from models.api_error_response import ApiErrorResponse

# -----------------------------------------------------------------------------
# IMPLEMENTAZIONE PER FASTAPI / HTTP (Da decommentare per utilizzo futuro)
# -----------------------------------------------------------------------------
# from fastapi import FastAPI, Request
# from fastapi.responses import JSONResponse
# from exceptions.app_exception import AppException
#
# app = FastAPI()
#
# @app.exception_handler(AppException)
# async def gestisci_eccezione_http(request: Request, errore: AppException):
#     """Gestore globale delle eccezioni custom per endpoint HTTP in FastAPI."""
#
#     # 1. Recupero lo status HTTP dall'eccezione (es. Enum status.value o default 400)
#     status_code = getattr(errore, "status", 400)
#     if hasattr(status_code, "value"):
#         status_code = status_code.value
#
#     # 2. Istanzio il modello ApiErrorResponse
#     risposta = ApiErrorResponse(
#         timestamp=datetime.now(ZoneInfo("Europe/Rome")).strftime("%d-%m-%Y %H:%M:%S"),
#         status=status_code,
#         errors=None,
#         message=str(errore),
#         trace=traceback.format_exc().splitlines(),  # Impostare a None in produzione per sicurezza
#         path=request.url.path                      # Path estratto in automatico dalla richiesta HTTP
#     )
#
#     # 3. Restituisco la risposta HTTP reale invece di stampare a consolle
#     return JSONResponse(
#         status_code=status_code,
#         content=risposta.to_dict()
#     )
# -----------------------------------------------------------------------------


def gestisci_eccezione(
    tipo: type[BaseException],
    errore: BaseException,
    tb: TracebackType | None,
    path: str | None = None,
) -> None:
    """Handle an exception and build a structured error response"""

    # Recupero la data e l'ora italiane senza millisecondi
    try:
        timestamp = datetime.now(
            ZoneInfo("Europe/Rome")
        ).strftime("%d-%m-%Y %H:%M:%S")

    except Exception:
        timestamp = datetime.now().astimezone().strftime(
            "%d-%m-%Y %H:%M:%S"
        )

    # Recupero lo stack trace.
    if tb is not None:
        # Genera il traceback e lo divide riga per riga eliminando i \n finali
        trace_text = "".join(traceback.format_exception(tipo, errore, tb))
        trace = trace_text.splitlines()
    else:
        trace = None

    # Recupero lo status solo se presente.
    status = getattr(errore, "status", None)

    if status is not None:
        status = status.value

    # Creo il modello standard della risposta
    risposta = ApiErrorResponse(
        timestamp=timestamp,
        status=status,
        errors=None,
        message=str(errore),
        trace=trace,
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