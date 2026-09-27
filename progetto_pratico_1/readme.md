# 🚀 Mini-Jira CLI Task Manager

[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Repo](https://img.shields.io/badge/repo-GitHub-181717?logo=github)](https://github.com/Mady93/corso-full-stack-python)
[![Last Commit](https://img.shields.io/github/last-commit/Mady93/corso-full-stack-python)](https://github.com/Mady93/corso-full-stack-python/commits/main)

**Mini-Jira CLI Task Manager** è un'applicazione da riga di comando per la gestione di progetti e attività di un team di sviluppo: utenti, ticket, assegnazioni, sprint, avanzamento degli stati, commenti, carichi di lavoro e statistiche, il tutto tramite un'interfaccia CLI semplice e strutturata.

> 📁 Questo progetto fa parte di [`corso-full-stack-python`](https://github.com/Mady93/corso-full-stack-python), il repository che raccoglie tutti gli esercizi del corso. Mini-Jira si trova nella cartella [`progetto_pratico_1`](https://github.com/Mady93/corso-full-stack-python/tree/main/progetto_pratico_1); questo README descrive solo quella parte del repo.

---

## Indice

- [Quick Start](#quick-start)
- [Cosa risolve](#cosa-risolve)
  - [1. Limite al carico di lavoro](#1-limite-al-carico-di-lavoro)
  - [2. Flusso di lavoro controllato](#2-flusso-di-lavoro-controllato)
  - [3. Due tipi di Ticket](#3-due-tipi-di-ticket)
  - [4. Gestione degli Sprint](#4-gestione-degli-sprint)
  - [5. Permessi e ruoli](#5-permessi-e-ruoli)
- [Architettura Tecnica](#architettura-tecnica)
- [Struttura del Codice: chi fa cosa](#struttura-del-codice-chi-fa-cosa)
- [Autenticazione e permessi](#autenticazione-e-permessi)
- [Testing](#testing)
- [Gestione dei dati](#gestione-dei-dati)
- [Note e limitazioni note](#note-e-limitazioni-note)
- [Conclusione](#conclusione)

---

## Quick Start

```bash
# Clona il repository
git clone https://github.com/Mady93/corso-full-stack-python.git
cd corso-full-stack-python/progetto_pratico_1

# Nessuna dipendenza esterna: solo Python standard library
python3 main.py
```

**Requisiti:** Python 3.10+ (il codice usa type hints con l'operatore `|`, es. `list[str] | None`, sintassi introdotta in 3.10). Sviluppato e testato su Python 3.14.7.

> 💡 Su Windows, se `python3` non è riconosciuto, usa `python` al suo posto (`python main.py`).

Per lanciare i test:

```bash
python3 tests/esegui_test.py
```

---

## Cosa risolve

### 1. Limite al carico di lavoro

Il sistema permette al Project Manager di impostare un **limite massimo di ticket assegnabili a ciascun Developer**.

Il limite è gestito centralmente tramite `ConfigurazioneTeam` (valore predefinito: 3 ticket per Developer) ed è applicato a tutti i Developer del progetto.

Un Developer può accettare un nuovo ticket solo se il proprio carico di lavoro è inferiore al limite configurato.

L'obiettivo è evitare un'eccessiva quantità di attività contemporaneamente in carico alla stessa persona e ridurre il fenomeno del *context switching*.

> 📐 **Legge di Little:** `L = λ × W` — il tempo medio di completamento di un ticket (W) è proporzionale al lavoro in corso (L); a parità di throughput (λ), limitare il WIP è ciò che tiene bassi i tempi di consegna.

### 2. Flusso di lavoro controllato

Ogni ticket segue un flusso di stati predefinito:

```text
TODO → IN_PROGRESS → IN_REVIEW → DONE
```

| Stato | Descrizione |
|---|---|
| `TODO` | Stato iniziale di ogni ticket |
| `IN_PROGRESS` | Lavorazione in corso |
| `IN_REVIEW` | In revisione |
| `DONE` | Completato; decrementa automaticamente il carico del Developer. `DONE → DONE` è tollerato |

Ogni cambio di stato è permesso solo all'assegnatario del ticket: il controllo (in `GestionaleJira.avanza_stato_ticket`) confronta l'autore dell'operazione con `ticket.assegnatario` prima di ogni transizione, non solo per alcuni stati.

Non è possibile saltare stati, né farli avanzare se non si è l'assegnatario del ticket.

### 3. Due tipi di Ticket

Entrambe le specializzazioni derivano dalla classe base `Ticket` e implementano il proprio `calcola_complessita()`:

| Tipo | Attributo distintivo | Priorità di default | Complessità |
|---|---|---|---|
| 🐛 `BugTicket` | `severita` (`BLOCKS`, `CRITICAL`, `MINOR`) | `ALTA` | "URGENTE" se `BLOCKS`/`CRITICAL`, altrimenti "Bugfix Standard" |
| ✨ `FeatureTicket` | `story_points` | `MEDIA` | "Alta Complessità" da 8 SP in su, "Media/Bassa" sotto |

### 4. Gestione degli Sprint

Gli Sprint permettono di raggruppare ticket con un obiettivo comune. È possibile:

- creare uno Sprint;
- aggiungere ticket (confronto per **codice**, non per identità dell'oggetto);
- avviare uno Sprint;
- chiudere uno Sprint;
- impedire che lo stesso ticket venga inserito in più Sprint contemporaneamente;
- impedire operazioni non valide sul ciclo di vita dello Sprint (doppio avvio, chiusura di uno Sprint non attivo).

### 5. Permessi e ruoli

Il sistema distingue due ruoli — 👨‍💻 **DEV** e 👔 **PM** — ognuno con un insieme di permessi che determina quali operazioni può effettuare (dettagli nella tabella in [Autenticazione e permessi](#autenticazione-e-permessi)).

---

## Architettura Tecnica

### ⚡ Architettura In-Memory

Lo stato principale dell'applicazione viene mantenuto interamente in memoria (RAM). `GestionaleJira` conserva in memoria utenti, ticket, sprint e configurazione del team.

Non viene utilizzato un database e non viene effettuato il salvataggio permanente dello stato: alla chiusura del programma, utenti, ticket e sprint vengono persi. L'unico dato scritto su disco è il log delle operazioni.

### 🛡️ Validazione e gestione degli errori

Gli input da tastiera vengono controllati tramite `leggi_stringa()`, `leggi_intero()` e `valida_opzione_scelta()` (in `utilita/validazioni.py`), che sollevano `ValidazioneError` in caso di input non valido.

Gli errori di business derivano tutti da `JiraException`, il che permette a `main.py` di distinguerli con un unico `except` dai bug veri e propri. Esempio concreto: `DuplicatoError` sostituisce un vecchio `ValueError` generico che, essendo builtin e non un `JiraException`, finiva erroneamente nel ramo "errore non previsto".

### 🧩 Struttura modulare

```text
modelli/
    ├── utente.py
    ├── ticket.py
    ├── sprint.py
    └── configurazione_team.py

servizi/
    ├── gestionale_jira.py
    ├── report_service.py
    └── logger.py

utilita/
    └── validazioni.py

eccezioni/
    └── eccezioni_custom.py

tests/
    ├── test_utente.py
    ├── test_ticket.py
    ├── test_sprint.py
    ├── test_configurazione_team.py
    ├── test_gestionale.py
    └── esegui_test.py

main.py
```

---

## Struttura del Codice: chi fa cosa

### 👤 modelli/utente.py — Gli utenti del sistema

Una singola classe `Utente` (username, email, ruolo, permessi, limite ticket, carico attuale, dipartimento). Non esistono classi separate `Sviluppatore`/`ProjectManager`: il comportamento dipende dal ruolo assegnato all'oggetto. Gestisce il proprio carico con `puo_accettare_ticket()`, `incrementa_ticket()`, `decrementa_ticket()`, `impostare_limite_ticket()`.

### 🎫 modelli/ticket.py — Il lavoro da svolgere

`Ticket` è la classe base (codice auto-generato `TCK-XXXX`, titolo, priorità, stato, assegnatario, commenti, storico). `avanza_stato()` gestisce le transizioni e registra lo storico. `BugTicket` e `FeatureTicket` ereditano da `Ticket` (vedi tabella sopra).

### 🏃 modelli/sprint.py — La gestione degli Sprint

`Sprint` (nome, obiettivo, stato `attivo`, lista ticket). La gestione delle relazioni tra Sprint, ticket e utenti (es. impedire che un ticket sia in due Sprint diversi) è coordinata dal `GestionaleJira`.

### ⚙️ modelli/configurazione_team.py — Configurazione del team

`ConfigurazioneTeam.limite_ticket_dev` (default 3). Creata **prima** della scelta del progetto, durante login/registrazione, e passata poi al `GestionaleJira`.

### 🧠 servizi/gestionale_jira.py — Il gestore del progetto

Componente centrale: mantiene in memoria utenti, ticket, sprint, configurazione e logger; coordina ogni operazione che coinvolge più entità (creazione, assegnazione, cambio stato, commenti, Sprint, verifica permessi, ricerca/elenco).

### 📊 servizi/report_service.py — Report e statistiche

`ReportService` è di sola lettura: calcola totale ticket, conteggi per stato e percentuale di completamento globale.

### 📝 servizi/logger.py — Il registro delle operazioni

`FileLogger` scrive su `logs/app_jira.log`, con percorso calcolato in base alla posizione di `servizi/logger.py` (non alla cartella di lancio), creando la cartella `logs/` automaticamente. È l'unico componente che scrive su file.

### 🧪 utilita/validazioni.py — Validazione degli input

Funzioni generiche, senza conoscenza specifica di ticket/utenti/Sprint; sollevano `ValidazioneError`.

### ⚠️ eccezioni/eccezioni_custom.py — Le eccezioni del sistema

| Eccezione | Quando viene sollevata |
|---|---|
| `JiraException` | Classe base; usata anche **direttamente** in `main.py` per errori di autenticazione (username duplicato in registrazione, utente non trovato o email non corrispondente al login) |
| `ValidazioneError` | Dati non validi: sia input da tastiera, sia valori passati ai costruttori dei modelli (es. username/email vuoti, limite ticket negativo) |
| `DuplicatoError` | Username, codice ticket o nome Sprint già esistente; ticket già assegnato; ticket già presente in un altro Sprint |
| `ElementoNonTrovatoError` | Utente, ticket o Sprint cercato non esiste |
| `RuoloNonValidoError` | Ruolo non ammesso, o operazione che richiede un ruolo diverso |
| `PermessoNegatoError` | L'utente non possiede il permesso richiesto |
| `LimiteCaricoLavoroSuperatoError` | Il Developer ha già raggiunto il limite di ticket assegnabili |
| `TicketNonAssegnatoError` | Si tenta di far avanzare un ticket senza assegnatario |
| `TransizioneStatoNonValidaError` | Si tenta un salto di stato non consentito |
| `StatoSprintError` | Operazione non valida sul ciclo di vita dello Sprint |

Tutte derivano da `JiraException`, per una gestione uniforme in `main.py`.

### 🖥️ main.py — L'interfaccia CLI

Gestisce registrazione/login, selezione del progetto (4 opzioni predefinite: Alpha, Beta, Gamma, Omega — non è previsto un nome libero), menu principale filtrato per permessi (`PERMESSO_RICHIESTO_MENU`), raccolta input (con `0` per annullare in ogni momento) e gestione errori. Non contiene logica di dominio: chiama solo modelli e servizi.

---

## Autenticazione e permessi

La registrazione richiede ruolo, username univoco, email e — solo per i PM — dipartimento. I permessi vengono assegnati automaticamente in base al ruolo.

| Permesso | 👨‍💻 DEV | 👔 PM |
|---|:---:|:---:|
| `VIEW_TICKET` | ✅ | ✅ |
| `COMMENT_TICKET` | ✅ | ✅ |
| `CHANGE_STATUS` | ✅ | ❌ |
| `CREATE_TICKET` | ❌ | ✅ |
| `ASSIGN_TICKET` | ❌ | ✅ |
| `CREATE_SPRINT` | ❌ | ✅ |
| `MANAGE_SPRINT` | ❌ | ✅ |
| `MANAGE_TEAM` | ❌ | ✅ |

Da notare: il PM **non** ha `CHANGE_STATUS` — l'avanzamento dello stato resta una responsabilità esclusiva del Developer assegnatario, verificata dal `GestionaleJira` confrontando l'autore dell'operazione con l'assegnatario del ticket.

---

## Testing

Suite di test organizzata per modulo, senza `unittest`: ogni funzione `test_*` viene eseguita ed esaminata con `assert`. `tests/esegui_test.py` lancia tutti i moduli e stampa un riepilogo.

I test coprono Utente, Ticket, BugTicket, FeatureTicket, Sprint, ConfigurazioneTeam e GestionaleJira, inclusi i casi di errore: dati non validi, elementi inesistenti, duplicati, permessi insufficienti, assegnazione a un PM, superamento del limite di carico, transizioni di stato non consentite, operazioni non valide sugli Sprint.

---

## Gestione dei dati

| Componente | Storage |
|---|---|
| Utenti | RAM |
| Ticket | RAM |
| Sprint | RAM |
| Configurazione | RAM |
| Log operazioni | `logs/app_jira.log` (disco) |

Alla chiusura dell'applicazione, lo stato del progetto non viene mantenuto: solo il log resta su disco.

---

## Conclusione

Mini-Jira CLI Task Manager organizza il lavoro di un team di sviluppo attraverso una gestione strutturata di utenti e permessi, ticket e assegnazioni, flusso degli stati, Sprint, statistiche, commenti e storico, limiti di carico del team e gestione controllata degli errori.

La struttura modulare separa modelli, servizi, utilità ed interfaccia CLI, rendendo il progetto più semplice da testare, comprendere e modificare.

---

## 📖 Come visualizzare questo README

Questo documento è scritto in **Markdown**. Per visualizzarlo correttamente:

### ✅ Visual Studio Code

1. Apri questo file in VS Code.
2. Premi `Ctrl + Shift + V` su Windows/Linux oppure `Cmd + Shift + V` su macOS.
3. Si aprirà l'anteprima con la formattazione corretta.

**Non è necessaria alcuna installazione** — VS Code dispone già di un'anteprima Markdown integrata.