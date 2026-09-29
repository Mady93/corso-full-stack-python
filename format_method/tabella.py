from typing import TypeAlias

from utility import (
    calcola_totale_generale,
    calcola_quantita_totale,
    calcola_totale_riga,
    calcola_quota,
)

from configurazione import (
    L_NOME,
    L_CAT,
    L_QTA,
    L_PREZZO,
    L_TOTALE,
    L_QUOTA,
    LARGHEZZA,
)


# Tipo usato per rappresentare una riga del magazzino.
RigaMagazzino: TypeAlias = tuple[str, str, int, float]


# ---------- funzioni per la costruzione della tabella ----------

def crea_bordo_superiore(
    l_nome: int,
    l_cat: int,
    l_qta: int,
    l_prezzo: int,
    l_totale: int,
    l_quota: int,
) -> str:
    """Crea il bordo superiore della tabella."""

    return (
        f"┌{'─' * l_nome}┬{'─' * l_cat}┬{'─' * l_qta}"
        f"┬{'─' * l_prezzo}┬{'─' * l_totale}┬{'─' * l_quota}┐"
    )


def crea_bordo_centrale(
    l_nome: int,
    l_cat: int,
    l_qta: int,
    l_prezzo: int,
    l_totale: int,
    l_quota: int,
) -> str:
    """Crea il bordo centrale della tabella."""

    return (
        f"├{'─' * l_nome}┼{'─' * l_cat}┼{'─' * l_qta}"
        f"┼{'─' * l_prezzo}┼{'─' * l_totale}┼{'─' * l_quota}┤"
    )


def crea_bordo_inferiore(
    l_nome: int,
    l_cat: int,
    l_qta: int,
    l_prezzo: int,
    l_totale: int,
    l_quota: int,
) -> str:
    """Crea il bordo inferiore della tabella."""

    return (
        f"└{'─' * l_nome}┴{'─' * l_cat}┴{'─' * l_qta}"
        f"┴{'─' * l_prezzo}┴{'─' * l_totale}┴{'─' * l_quota}┘"
    )


def crea_bordo_titolo(larghezza: int) -> str:
    """Crea il bordo superiore decorativo del titolo."""

    # Il +7 tiene conto dei bordi e dei separatori della tabella.
    larghezza_titolo = larghezza + 7

    return f"╭{'─' * (larghezza_titolo - 2)}╮"


def crea_titolo(larghezza: int) -> str:
    """Crea il titolo centrato della tabella."""

    # Calcola lo spazio disponibile all'interno del bordo.
    larghezza_titolo = larghezza + 7

    return f"│{' MAGAZZINO ':^{larghezza_titolo - 2}}│"


# ---------- VERSIONE 1: f-string ----------

def tabella_fstring(dati: list[RigaMagazzino]) -> str:
    """Genera la tabella del magazzino usando le f-string."""

    # Lista che conterrà tutte le righe della tabella.
    righe: list[str] = []

    # Crea i bordi della tabella usando le larghezze della configurazione.
    bordo_sup = crea_bordo_superiore(
        L_NOME,
        L_CAT,
        L_QTA,
        L_PREZZO,
        L_TOTALE,
        L_QUOTA,
    )

    bordo_centro = crea_bordo_centrale(
        L_NOME,
        L_CAT,
        L_QTA,
        L_PREZZO,
        L_TOTALE,
        L_QUOTA,
    )

    bordo_inf = crea_bordo_inferiore(
        L_NOME,
        L_CAT,
        L_QTA,
        L_PREZZO,
        L_TOTALE,
        L_QUOTA,
    )

    # Aggiunge il bordo e il titolo.
    righe.append(crea_bordo_titolo(LARGHEZZA))
    righe.append(crea_titolo(LARGHEZZA))

    # Aggiunge il bordo superiore delle colonne.
    righe.append(bordo_sup)

    # Aggiunge l'intestazione delle colonne.
    righe.append(
        f"│{'Prodotto':<{L_NOME}}"
        f"│{'Categoria':<{L_CAT}}"
        f"│{'Qta':>{L_QTA}}"
        f"│{'Prezzo EUR':>{L_PREZZO}}"
        f"│{'Totale EUR':>{L_TOTALE}}"
        f"│{'Quota':>{L_QUOTA}}│"
    )

    # Aggiunge il separatore tra intestazione e dati.
    righe.append(bordo_centro)

    # Calcola una sola volta il totale generale.
    totale_generale = calcola_totale_generale(dati)

    # Scorre tutti i prodotti.
    for nome, categoria, qta, prezzo in dati:

        # Calcola il totale della singola riga.
        totale = calcola_totale_riga(qta, prezzo)

        # Calcola la quota della singola riga.
        quota = calcola_quota(totale, totale_generale)

        # Aggiunge la riga del prodotto.
        righe.append(
            f"│{nome:<{L_NOME}}"
            f"│{categoria:<{L_CAT}}"
            f"│{qta:>{L_QTA}d}"
            f"│{prezzo:>{L_PREZZO}.2f}"
            f"│{totale:>{L_TOTALE},.2f}"
            f"│{quota:>{L_QUOTA}.1%}│"
        )

    # Aggiunge il separatore prima del totale.
    righe.append(bordo_centro)

    # Calcola la quantità totale.
    quantita_totale = calcola_quantita_totale(dati)

    # Aggiunge la riga dei totali.
    righe.append(
        f"│{'TOTALE':<{L_NOME}}"
        f"│{'':<{L_CAT}}"
        f"│{quantita_totale:>{L_QTA}d}"
        f"│{'':>{L_PREZZO}}"
        f"│{totale_generale:>{L_TOTALE},.2f}"
        f"│{1:>{L_QUOTA}.1%}│"
    )

    # Aggiunge il bordo inferiore.
    righe.append(bordo_inf)

    # Unisce tutte le righe con un ritorno a capo.
    return "\n".join(righe)


# ---------- VERSIONE 2: .format() ----------

def tabella_format(dati: list[RigaMagazzino]) -> str:
    """Genera la tabella del magazzino usando .format()."""

    # Lista che conterrà tutte le righe della tabella.
    righe: list[str] = []

    # Dizionario delle larghezze usato da .format().
    larghezze: dict[str, int] = {
        "ln": L_NOME,
        "lc": L_CAT,
        "lq": L_QTA,
        "lp": L_PREZZO,
        "lt": L_TOTALE,
        "lqu": L_QUOTA,
    }

    # Stringa modello per il titolo.
    titolo = "│{:^{w}}│"

    # Stringa modello per l'intestazione.
    intestazione = (
        "│{:<{ln}}│{:<{lc}}│{:>{lq}}│"
        "{:>{lp}}│{:>{lt}}│{:>{lqu}}│"
    )

    # Stringa modello per le righe dei prodotti.
    riga = (
        "│{nome:<{ln}}│{categoria:<{lc}}│{qta:>{lq}d}│"
        "{prezzo:>{lp}.2f}│{totale:>{lt},.2f}│{quota:>{lqu}.1%}│"
    )

    # Stringa modello per la riga del totale.
    riga_totale = (
        "│{:<{ln}}│{:<{lc}}│{:>{lq}d}│"
        "{:>{lp}}│{:>{lt},.2f}│{:>{lqu}.1%}│"
    )

    # Calcola la larghezza necessaria per il titolo.
    larghezza_titolo = LARGHEZZA + 7

    # Crea i bordi della tabella.
    bordo_sup = crea_bordo_superiore(
        L_NOME,
        L_CAT,
        L_QTA,
        L_PREZZO,
        L_TOTALE,
        L_QUOTA,
    )

    bordo_centro = crea_bordo_centrale(
        L_NOME,
        L_CAT,
        L_QTA,
        L_PREZZO,
        L_TOTALE,
        L_QUOTA,
    )

    bordo_inf = crea_bordo_inferiore(
        L_NOME,
        L_CAT,
        L_QTA,
        L_PREZZO,
        L_TOTALE,
        L_QUOTA,
    )

    # Aggiunge il bordo e il titolo.
    righe.append(crea_bordo_titolo(LARGHEZZA))
    righe.append(
        titolo.format(
            "MAGAZZINO",
            w=larghezza_titolo - 2,
        )
    )

    # Aggiunge il bordo superiore delle colonne.
    righe.append(bordo_sup)

    # Aggiunge l'intestazione.
    righe.append(
        intestazione.format(
            "Prodotto",
            "Categoria",
            "Qta",
            "Prezzo EUR",
            "Totale EUR",
            "Quota",
            **larghezze,
        )
    )

    # Aggiunge il separatore tra intestazione e dati.
    righe.append(bordo_centro)

    # Calcola una sola volta il totale generale.
    totale_generale = calcola_totale_generale(dati)

    # Scorre tutti i prodotti.
    for nome, categoria, qta, prezzo in dati:

        # Calcola il totale della singola riga.
        totale = calcola_totale_riga(qta, prezzo)

        # Calcola la quota della singola riga.
        quota = calcola_quota(totale, totale_generale)

        # Aggiunge la riga formattata.
        righe.append(
            riga.format(
                nome=nome,
                categoria=categoria,
                qta=qta,
                prezzo=prezzo,
                totale=totale,
                quota=quota,
                **larghezze,
            )
        )

    # Aggiunge il separatore prima del totale.
    righe.append(bordo_centro)

    # Calcola la quantità totale.
    quantita_totale = calcola_quantita_totale(dati)

    # Aggiunge la riga dei totali.
    righe.append(
        riga_totale.format(
            "TOTALE",
            "",
            quantita_totale,
            "",
            totale_generale,
            1,
            **larghezze,
        )
    )

    # Aggiunge il bordo inferiore.
    righe.append(bordo_inf)

    # Unisce tutte le righe con un ritorno a capo.
    return "\n".join(righe)