"""
Entry point del Mini-Jira CLI Task Manager.

main.py coordina l'esecuzione: gestisce l'autenticazione (login/registrazione),
raccoglie l'input da tastiera, chiama il GestionaleJira (che applica le regole
di business) e mostra il risultato. Non contiene logica di dominio: quella
vive nei modelli e nei servizi, per poter essere testata senza simulare il menu.
"""

from eccezioni.eccezioni_custom import JiraException
from modelli.configurazione_team import ConfigurazioneTeam
from modelli.sprint import Sprint
from modelli.ticket import BugTicket, FeatureTicket
from modelli.utente import Utente
from servizi.gestionale_jira import GestionaleJira
from servizi.report_service import ReportService
from utilita.validazioni import (
    leggi_intero,
    leggi_stringa,
    valida_opzione_scelta,
)


class OperazioneAnnullata(Exception):
    """Eccezione interna usata per tornare al menu principale."""

    pass


def leggi_input_o_annulla(prompt: str, uppercase: bool = False) -> str:
    """Legge una stringa e annulla l'operazione se viene inserito 0."""

    valore = leggi_stringa(
        prompt,
        uppercase=uppercase,
    )

    if valore == "0":
        raise OperazioneAnnullata()

    return valore


# --------------------------- AUTENTICAZIONE (login / registrazione / logout ---------------------------)

def registra_nuovo_utente(
    utenti: dict,
    config_team: ConfigurazioneTeam,
) -> None:
    """Registra un nuovo utente nel sistema (dict condiviso, indipendente dal progetto)."""

    print("\n--- REGISTRAZIONE NUOVO UTENTE ---")
    print("Inserisci 0 in qualsiasi momento per annullare.")

    ruolo = leggi_input_o_annulla(
        "Ruolo (DEV per Sviluppatore / PM per Project Manager): ",
        uppercase=True,
    )

    valida_opzione_scelta(ruolo, ["DEV", "PM"])

    username = leggi_input_o_annulla("Inserisci Username unico: ")

    if username in utenti:
        raise JiraException(
            f"Username '{username}' gia' esistente. Scegline un altro."
        )

    email = leggi_input_o_annulla("Inserisci Email: ")

    permessi_per_ruolo = {
        "DEV": [
            "VIEW_TICKET",
            "COMMENT_TICKET",
            "CHANGE_STATUS",
        ],
        "PM": [
            "VIEW_TICKET",
            "COMMENT_TICKET",
            "CREATE_TICKET",
            "ASSIGN_TICKET",
            "CREATE_SPRINT",
            "MANAGE_SPRINT",
            "MANAGE_TEAM",
        ],
    }

    permessi = permessi_per_ruolo[ruolo]

    if ruolo == "DEV":
        # Il limite ticket NON lo sceglie il singolo DEV: e' un valore
        # di team, uguale per tutti, deciso dal PM (voce di menu
        # dedicata). Il DEV riceve semplicemente il limite corrente.
        max_t = config_team.limite_ticket_dev

        print(
            f"\n[INFO] Limite ticket in carico impostato dal team: "
            f"{max_t} (modificabile solo dal PM)."
        )

        dipartimento = ""

    else:
        max_t = 0

        dipartimento = leggi_input_o_annulla(
            "Dipartimento/Area (es. Frontend, Core, Mobile): "
        )

    utente = Utente(
        username,
        email,
        ruolo,
        permessi,
        max_ticket=max_t,
        dipartimento=dipartimento,
    )

    utenti[username] = utente

    print(
        f"\n[OK] Utente '{username}' registrato con successo. "
        f"Effettua il login per continuare."
    )


def login_utente(utenti: dict) -> Utente:
    """
    Mostra la lista degli utenti registrati (per evitare errori di
    battitura) e poi chiede username + email per validare l'accesso.
    """

    print("\n--- LOGIN ---")

    if not utenti:
        raise JiraException(
            "Nessun utente registrato. Registrati prima."
        )

    print("Utenti registrati:")

    for u in utenti.values():
        print(
            f" - Username: {u.username} | "
            f"Email: {u.email} | "
            f"Ruolo: {u.get_ruolo()}"
        )

    username = leggi_input_o_annulla("\nUsername: ")

    if username not in utenti:
        raise JiraException(
            f"Utente '{username}' non trovato."
        )

    email = leggi_input_o_annulla("Email: ")

    utente = utenti[username]

    if utente.email.strip().lower() != email.strip().lower():
        raise JiraException(
            "Email non corrispondente per questo utente."
        )

    print(
        f"\n[OK] Login effettuato: "
        f"{utente.username} "
        f"({utente.get_ruolo()})"
    )

    return utente


def schermata_autenticazione(
    utenti: dict,
    config_team: ConfigurazioneTeam,
) -> Utente:
    """
    Schermata iniziale (usata anche per il logout): permette di
    fare login con un utente esistente o registrarne uno nuovo.
    Ritorna l'utente che risulta attivo.
    """

    while True:
        print("\n" + "=" * 55)
        print("      BENVENUTO IN MINI-JIRA TASK MANAGER")
        print("=" * 55)
        print("1. Login")
        print("2. Registrati")

        scelta = leggi_stringa("Seleziona un'opzione: ")

        try:
            if scelta == "1":
                if not utenti:
                    print(
                        "\nNessun utente registrato. "
                        "Registrati prima."
                    )
                    continue

                return login_utente(utenti)

            elif scelta == "2":
                registra_nuovo_utente(utenti, config_team)
                continue

            else:
                print("Opzione non valida. Scegli 1 o 2.")

        except OperazioneAnnullata:
            print("\n[ANNULLATO] Riprova.")

        except JiraException as e:
            print(f"\n[ERRORE]: {e}")



# --------------------------- SELEZIONE PROGETTO E MENU ---------------------------


def seleziona_progetto() -> str:
    """Mostra la lista dei progetti disponibili e ne fa scegliere uno."""

    progetti_disponibili = [
        "ALP - Alpha Project",
        "BET - Beta Project",
        "GAM - Gamma Project",
        "OMG - Omega Project",
    ]

    print("=" * 55)
    print("      CONFIGURAZIONE INIZIALE GESTIONALE JIRA")
    print("=" * 55)
    print("Seleziona il progetto su cui lavorare:\n")

    for idx, progetto in enumerate(progetti_disponibili, start=1):
        print(f"{idx}. {progetto}")

    scelta = leggi_intero(
        "\nSeleziona numero progetto: ",
        min_val=1,
        max_val=len(progetti_disponibili),
    )

    return progetti_disponibili[scelta - 1]


# Permesso richiesto per ogni voce di menu che modifica dati.
# Le voci non presenti qui (es. le visualizzazioni, logout, esci) sono
# sempre visibili a chiunque sia autenticato.
PERMESSO_RICHIESTO_MENU = {
    "2": "CREATE_TICKET",
    "3": "ASSIGN_TICKET",
    "4": "CHANGE_STATUS",
    "5": "COMMENT_TICKET",
    "6": "CREATE_SPRINT",
    "7": "MANAGE_SPRINT",
    "8": "MANAGE_SPRINT",
    "14": "MANAGE_TEAM",
    "15": "VIEW_TICKET",
}

VOCI_MENU = {
    "1": "Visualizza Utenti e Team",
    "2": "Crea Nuovo Ticket",
    "3": "Assegna Ticket",
    "4": "Avanza Stato Ticket",
    "5": "Aggiungi Commento",
    "6": "Crea Nuovo Sprint",
    "7": "Aggiungi Ticket a uno Sprint",
    "8": "Avvia / Chiudi Sprint",
    "9": "Visualizza Ticket",
    "10": "Visualizza Utenti e Carico di Lavoro",
    "11": "Visualizza Sprint",
    "12": "Mostra Report e Statistiche",
    "13": "Logout / Cambia Utente Attivo",
    "14": "Imposta Limite Ticket Team (solo PM)",
    "15": "Visualizza Dettaglio Ticket (Commenti e Storico)",
    "0": "Esci dal Progetto",
}


def mostra_menu(nome_progetto: str, utente_corrente: Utente) -> None:
    """
    Stampa a schermo il menu principale, mostrando solo le voci
    che l'utente attivo puo' effettivamente usare in base al suo ruolo.
    Il controllo vero e vincolante resta comunque lato GestionaleJira
    (verifica_permesso): questo filtro e' solo per non confondere
    l'utente con opzioni che gli verrebbero comunque negate.
    """

    print("\n" + "=" * 55)
    print(f"   MINI-JIRA TASK MANAGER - [{nome_progetto.upper()}]")
    print("=" * 55)

    print(
        f"Utente attivo: {utente_corrente.username} "
        f"({utente_corrente.get_ruolo()})"
    )

    print()

    for numero, etichetta in VOCI_MENU.items():
        permesso = PERMESSO_RICHIESTO_MENU.get(numero)

        if permesso is None or utente_corrente.ha_permesso(permesso):
            print(f"{numero}. {etichetta}")

    print("-" * 55)


def main() -> None:
    """Ciclo principale: autenticazione, poi scelta progetto, poi menu."""

    utenti_globali: dict = {}
    config_team = ConfigurazioneTeam()

    utente_corrente = schermata_autenticazione(utenti_globali, config_team)

    nome_progetto = seleziona_progetto()

    jira = GestionaleJira(
        nome_progetto,
        utenti=utenti_globali,
        config_team=config_team,
    )
    reporter = ReportService(jira)

    while True:
        mostra_menu(nome_progetto, utente_corrente)

        try:
            scelta = leggi_stringa("Seleziona un'opzione: ")

            # 1. VISUALIZZA UTENTI E TEAM
            if scelta == "1":
                utenti = jira.elenca_utenti()

                print(f"\n--- UTENTI E TEAM ({len(utenti)}) ---")

                if not utenti:
                    print(" - Nessun utente registrato.")
                else:
                    for u in utenti:
                        print(
                            f" - {u.username} "
                            f"({u.get_ruolo()})"
                        )

            # 2. CREA TICKET DA TASTIERA
            elif scelta == "2":
                print("\n--- CREAZIONE NUOVO TICKET ---")
                print(
                    "Inserisci 0 in qualsiasi momento per "
                    "tornare al menu principale."
                )

                tipo = leggi_input_o_annulla(
                    "Tipo Ticket (BUG / FEATURE): ",
                    uppercase=True,
                )

                valida_opzione_scelta(
                    tipo,
                    ["BUG", "FEATURE"],
                )

                titolo = leggi_input_o_annulla(
                    "Titolo / Descrizione sintetica: "
                )

                priorita = leggi_input_o_annulla(
                    "Priorita' (BASSA / MEDIA / ALTA): ",
                    uppercase=True,
                )

                valida_opzione_scelta(
                    priorita,
                    ["BASSA", "MEDIA", "ALTA"],
                )

                if tipo == "BUG":
                    sev = leggi_input_o_annulla(
                        "Severita' "
                        "(BLOCKS / CRITICAL / MINOR): ",
                        uppercase=True,
                    )

                    valida_opzione_scelta(
                        sev,
                        ["BLOCKS", "CRITICAL", "MINOR"],
                    )

                    ticket = BugTicket(
                        "",
                        titolo,
                        severita=sev,
                        priorita=priorita,
                    )

                else:
                    sp = leggi_intero(
                        "Story Points "
                        "(0 per annullare, 1-13): ",
                        min_val=0,
                        max_val=13,
                    )

                    if sp == 0:
                        raise OperazioneAnnullata()

                    ticket = FeatureTicket(
                        "",
                        titolo,
                        story_points=sp,
                        priorita=priorita,
                    )

                jira.crea_ticket(
                    ticket,
                    utente_corrente.username,
                )

                print(
                    f"\n[OK] Ticket {ticket.codice} "
                    f"creato con successo!"
                )

            # 3. ASSEGNA TICKET VIA INPUT
            elif scelta == "3":
                print("\n--- ASSEGNAZIONE TICKET ---")
                print(
                    "Inserisci 0 in qualsiasi momento per "
                    "tornare al menu principale."
                )

                print("Ticket in memoria:")

                for t in jira.elenca_ticket():
                    dev = (
                        t.assegnatario.username
                        if t.assegnatario
                        else "Non assegnato"
                    )

                    print(
                        f" - [{t.codice}] "
                        f"{t.titolo} "
                        f"(Assegnato a: {dev})"
                    )

                cod_ticket = leggi_input_o_annulla(
                    "\nInserisci Codice Ticket: ",
                    uppercase=True,
                )

                print("\nSviluppatori registrati:")

                for u in jira.elenca_utenti():
                    if u.get_ruolo() == "DEV":
                        print(
                            f" - Username: {u.username} "
                            f"(Carico: "
                            f"{u.ticket_in_carico}/"
                            f"{u.max_ticket})"
                        )

                dev_user = leggi_input_o_annulla(
                    "Inserisci Username Sviluppatore: "
                )

                jira.assegna_ticket(
                    cod_ticket,
                    dev_user,
                    utente_corrente.username,
                )

            # 4. AVANZA STATO TICKET VIA INPUT
            elif scelta == "4":
                print("\n--- CAMBIO STATO TICKET ---")
                print(
                    "Inserisci 0 in qualsiasi momento per "
                    "tornare al menu principale."
                )

                print("\nTicket in memoria:\n")

                for t in jira.elenca_ticket():

                    dev = (
                        t.assegnatario.username
                        if t.assegnatario
                        else "Non assegnato"
                    )

                    print(
                        f" - [{t.codice}] {t.titolo}\n"
                        f"   (Stato: {t.stato}, "
                        f"Assegnato a: {dev})\n"
                    )

                cod_ticket = leggi_input_o_annulla(
                    "\nCodice Ticket: ",
                    uppercase=True,
                )

                nuovo_stato = leggi_input_o_annulla(
                    "Nuovo Stato "
                    "(IN_PROGRESS / IN_REVIEW / DONE): ",
                    uppercase=True,
                )

                jira.avanza_stato_ticket(
                    cod_ticket,
                    nuovo_stato,
                    autore=utente_corrente.username,
                )

            # 5. AGGIUNGI COMMENTO VIA INPUT
            elif scelta == "5":
                print("\n--- AGGIUNGI COMMENTO ---")
                print(
                    "Inserisci 0 in qualsiasi momento per "
                    "tornare al menu principale."
                )

                print("Ticket in memoria:")

                for t in jira.elenca_ticket():
                    print(
                        f" - [{t.codice}] "
                        f"{t.titolo}"
                    )

                cod_ticket = leggi_input_o_annulla(
                    "\nCodice Ticket: ",
                    uppercase=True,
                )

                testo = leggi_input_o_annulla(
                    "Scrivi il commento: "
                )

                jira.aggiungi_commento_ticket(
                    cod_ticket,
                    utente_corrente.username,
                    testo,
                )

            # 6. CREA SPRINT VIA INPUT
            elif scelta == "6":
                print("\n--- CREAZIONE SPRINT ---")
                print(
                    "Inserisci 0 in qualsiasi momento per "
                    "tornare al menu principale."
                )

                nome_sp = leggi_input_o_annulla(
                    "Nome dello Sprint (es. Sprint 1): "
                )

                obj_sp = leggi_input_o_annulla(
                    "Obiettivo dello Sprint: "
                )

                sprint = Sprint(
                    nome_sp,
                    obj_sp,
                )

                jira.crea_sprint(
                    sprint,
                    utente_corrente.username,
                )

            # 7. AGGIUNGI TICKET A SPRINT
            elif scelta == "7":
                print("\n--- AGGIUNGI TICKET A SPRINT ---")
                print(
                    "Inserisci 0 in qualsiasi momento per "
                    "tornare al menu principale."
                )

                print("Sprint creati:")

                for s in jira.elenca_sprint():
                    print(f" - {s.nome}")

                nome_sp = leggi_input_o_annulla(
                    "\nNome dello Sprint: "
                )

                print("\nTicket disponibili:")

                for t in jira.elenca_ticket():
                    print(
                        f" - [{t.codice}] "
                        f"{t.titolo}"
                    )

                cod_ticket = leggi_input_o_annulla(
                    "Codice Ticket da aggiungere: ",
                    uppercase=True,
                )

                jira.aggiungi_ticket_a_sprint(
                    nome_sp,
                    cod_ticket,
                    utente_corrente.username,
                )

            # 8. AVVIA / CHIUDI SPRINT
            elif scelta == "8":
                print("\n--- AVVIA / CHIUDI SPRINT ---")
                print(
                    "Inserisci 0 in qualsiasi momento per "
                    "tornare al menu principale."
                )

                print("Sprint disponibili:")

                for s in jira.elenca_sprint():
                    if s.attivo:
                        stato = "ATTIVO"
                    else:
                        stato = "CHIUSO / PIANIFICATO"

                    print(
                        f" - {s.nome} [{stato}]"
                    )

                nome_sp = leggi_input_o_annulla(
                    "\nNome dello Sprint: "
                )

                azione = leggi_input_o_annulla(
                    "Azione (AVVIA / CHIUDI): ",
                    uppercase=True,
                )

                valida_opzione_scelta(
                    azione,
                    ["AVVIA", "CHIUDI"],
                )

                if azione == "AVVIA":
                    jira.avvia_sprint(nome_sp, utente_corrente.username)
                else:
                    jira.chiudi_sprint(nome_sp, utente_corrente.username)

            # 9. VISUALIZZA TICKET IN RAM
            elif scelta == "9":
                tickets = jira.elenca_ticket()

                print(
                    f"\n--- ELENCO TICKET "
                    f"IN MEMORIA ({len(tickets)}) ---"
                )

                if not tickets:
                    print(
                        "Nessun ticket ancora registrato."
                    )

                for t in tickets:
                    print(t)

                    print(
                        f"   L Complessita' calcolata: "
                        f"{t.calcola_complessita()}"
                    )

            # 10. VISUALIZZA TEAM E CARICO DI LAVORO
            elif scelta == "10":
                utenti = jira.elenca_utenti()

                print(
                    f"\n--- UTENTI E CARICO DI LAVORO "
                    f"({len(utenti)}) ---"
                )

                if not utenti:
                    print(
                        "Nessun utente ancora registrato."
                    )

                for u in utenti:
                    print(u)

            # 11. VISUALIZZA SPRINT IN RAM
            elif scelta == "11":
                sprint_list = jira.elenca_sprint()

                print(
                    f"\n--- SPRINT "
                    f"({len(sprint_list)}) ---"
                )

                if not sprint_list:
                    print(
                        "Nessuno Sprint ancora creato."
                    )

                for s in sprint_list:
                    print(s)

                    for t in s.elenca_ticket():
                        print(
                            f"   L {t.codice} - "
                            f"{t.titolo}"
                        )

            # 12. MOSTRA STATISTICHE
            elif scelta == "12":
                stats = reporter.calcola_statistiche()

                print(
                    "\n--- STATISTICHE PROGETTO ---"
                )

                for k, v in stats.items():
                    print(f"{k}: {v}")

            # 13. LOGOUT / CAMBIO UTENTE
            elif scelta == "13":
                print("\n--- LOGOUT ---")

                utente_corrente = schermata_autenticazione(
                    utenti_globali,
                    config_team,
                )

            # 14. IMPOSTA LIMITE TICKET TEAM (SOLO PM)
            elif scelta == "14":
                print("\n--- LIMITE TICKET TEAM ---")

                print(
                    f"Limite attuale: {jira.limite_ticket_dev} "
                    f"ticket per DEV."
                )

                nuovo_limite = leggi_intero(
                    "Nuovo limite (0 per annullare): ",
                    min_val=0,
                )

                if nuovo_limite == 0:
                    raise OperazioneAnnullata()

                jira.imposta_limite_ticket_team(
                    nuovo_limite,
                    utente_corrente.username,
                )

                print(
                    f"\n[OK] Limite ticket team aggiornato a "
                    f"{nuovo_limite} per tutti i DEV."
                )

            # 15. DETTAGLIO TICKET (COMMENTI E STORICO)
            elif scelta == "15":
                print("\n--- DETTAGLIO TICKET ---")

                print("Ticket in memoria:")

                for t in jira.elenca_ticket():
                    print(
                        f" - [{t.codice}] "
                        f"{t.titolo}"
                    )

                cod_ticket = leggi_input_o_annulla(
                    "\nCodice Ticket: ",
                    uppercase=True,
                )

                ticket = jira.cerca_ticket_per_codice(cod_ticket)

                print(f"\n{ticket}")
                print(
                    f"Complessita': "
                    f"{ticket.calcola_complessita()}"
                )

                print("\nCommenti:")

                if not ticket.commenti:
                    print(" - Nessun commento presente.")
                else:
                    for c in ticket.commenti:
                        print(f" - {c}")

                print("\nStorico:")

                for riga in ticket.storico:
                    print(f" - {riga}")

            # 0. ESCI
            elif scelta == "0":
                print(
                    f"\nChiusura del sistema Jira "
                    f"per '{nome_progetto}'. "
                    f"Arrivederci!"
                )
                break

            else:
                print(
                    "Opzione non riconosciuta. "
                    "Inserisci un numero da 0 a 15."
                )

        except OperazioneAnnullata:
            print(
                "\n[ANNULLATO] "
                "Ritorno al menu principale."
            )

        except JiraException as e:
            print(
                f"\n[ERRORE REGOLA DI BUSINESS]: {e}"
            )

            jira.registra_errore(
                f"Regola di business violata: {e}"
            )

        except Exception as e:
            print(
                f"\n[ERRORE NON PREVISTO]: {e}"
            )

            jira.registra_errore(
                f"Errore non previsto: {e}"
            )

        else:
            if scelta in [
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "14",
            ]:
                print(
                    "\n[OK] Operazione inserita "
                    "ed eseguita con successo!"
                )

        finally:
            print("--- Operazione conclusa ---")


if __name__ == "__main__":
    main()