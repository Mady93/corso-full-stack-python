# 🚀 Mini-Jira CLI Task Manager

## 1. Introduzione e obiettivo

**Mini-Jira CLI Task Manager** è un'applicazione da riga di comando che simula la gestione dei task all'interno di un team di sviluppo software.

L'obiettivo principale che mi sono posta è stato quello di **trasformare delle regole di business in vincoli software**.

Quindi non mi sono limitata a memorizzare utenti, ticket e Sprint, ma ho fatto in modo che il programma controllasse automaticamente che le operazioni rispettassero le regole definite.

Ad esempio, un Developer non può avere un numero illimitato di ticket, un ticket non può saltare le fasi del workflow e solo il Developer assegnatario può modificarne lo stato.

---

# 2. Struttura del progetto e programmazione ad oggetti

Ho organizzato il progetto in modo modulare, separando le diverse responsabilità.

Ho quindi:

* **modelli**, per rappresentare gli oggetti principali;
* **servizi**, per gestire la logica applicativa;
* **utilità**, per le funzioni di supporto e la validazione degli input;
* **eccezioni personalizzate**, per rappresentare gli errori di business;
* **CLI**, per l'interazione con l'utente.

Il cuore della logica applicativa è `GestionaleJira`, mentre `main.py` si occupa principalmente di autenticazione, input e menu.

### Programmazione ad oggetti

Per la programmazione ad oggetti ho utilizzato soprattutto **ereditarietà e polimorfismo**.

La classe principale è `Ticket`, che contiene le informazioni comuni, come codice, titolo, priorità, stato, assegnatario, commenti e storico.

Da `Ticket` derivano:

* `BugTicket`, che aggiunge la **severità**;
* `FeatureTicket`, che aggiunge gli **Story Points**.

Il polimorfismo è visibile, ad esempio, nel metodo `calcola_complessita()`.

Il metodo viene definito nella classe base, ma ogni sottoclasse lo implementa in modo diverso: per i bug dipende dalla severità, mentre per le feature dipende dagli Story Points.

Lo stesso principio viene utilizzato anche in `__str__()`, che viene personalizzato dalle sottoclassi.

In questo modo posso lavorare con oggetti `Ticket` mantenendo però il comportamento specifico di ogni tipo di ticket.

### Architettura In-Memory

Il sistema utilizza un'architettura **in-memory**.

Durante l'esecuzione, utenti, ticket e Sprint vengono mantenuti in memoria e non vengono salvati permanentemente su disco.

Ho invece utilizzato `FileLogger` per registrare operazioni ed errori in un file di log.

Quindi il log serve come **tracciamento delle operazioni**, ma non rappresenta la persistenza dei dati dell'applicazione.

---

# 3. Ruoli e controllo dei permessi

Nel sistema ho previsto due ruoli:

* **Project Manager**, o PM;
* **Developer**, o DEV.

I due ruoli hanno permessi differenti.

Il **PM** può creare e assegnare ticket, creare e gestire Sprint e modificare la configurazione del team.

Il **Developer** può visualizzare i ticket, aggiungere commenti e modificare lo stato dei ticket che gli sono stati assegnati.

Un punto importante è che i permessi non vengono controllati solamente dal menu.

Per esempio, per modificare lo stato di un ticket sono necessari il permesso `CHANGE_STATUS` e la condizione di essere **l'assegnatario del ticket**.

Questi controlli vengono effettuati da `GestionaleJira`, quindi la regola viene applicata direttamente nella **business logic**.

---

# 4. Workflow e limite di carico

Uno degli aspetti principali del progetto è la gestione del workflow.

Il ticket segue questa sequenza:

```text
TODO → IN_PROGRESS → IN_REVIEW → DONE
```

La classe `Ticket` impedisce di saltare degli stati e non permette di iniziare il lavoro su un ticket `TODO` se non è stato assegnato.

In questo caso ho quindi due livelli di controllo:

* `GestionaleJira` verifica **chi può effettuare l'operazione**;
* `Ticket` verifica **se la transizione richiesta è valida**.

### Limite di carico

Ho poi introdotto un limite al numero di ticket che ogni Developer può avere contemporaneamente in carico.

Il limite viene gestito tramite `ConfigurazioneTeam` ed è inizialmente impostato a **3 ticket per Developer**.

Il PM può modificarlo e la nuova configurazione viene applicata sia ai Developer già presenti sia a quelli registrati successivamente.

Quando assegno un ticket, `GestionaleJira` controlla il carico dello sviluppatore.

Se il limite è già stato raggiunto, viene sollevata:

```text
LimiteCaricoLavoroSuperatoError
```

In questo modo l'assegnazione viene bloccata automaticamente.

Quando invece un ticket passa a `DONE`, il carico del Developer viene decrementato e si libera nuovamente uno spazio.

### Legge di Little

Il concetto del limite WIP è collegato alla **Legge di Little**:

```text
L = λ × W
```

dove:

1. **`L`** rappresenta il **lavoro in corso**, cioè il **WIP** (*Work In Progress*);
2. **`λ`**, **lambda**, rappresenta il **throughput**, cioè quante attività vengono completate per unità di tempo;
3. **`W`** rappresenta il **tempo medio di permanenza** di un'attività nel sistema.

Nel mio progetto ho utilizzato questo concetto come **motivazione progettuale** per limitare il numero di attività contemporaneamente in carico.

L'obiettivo è mantenere sotto controllo il lavoro in corso ed evitare un accumulo eccessivo di attività.

---

# 5. Gestione degli errori e testing

Per rappresentare le violazioni delle regole di business ho creato una gerarchia di eccezioni che deriva da `JiraException`.

Tra le principali ho:

```text
ValidazioneError
TransizioneStatoNonValidaError
LimiteCaricoLavoroSuperatoError
ElementoNonTrovatoError
StatoSprintError
DuplicatoError
RuoloNonValidoError
TicketNonAssegnatoError
PermessoNegatoError
```

In questo modo ogni tipo di errore rappresenta una situazione specifica.

La CLI intercetta le `JiraException`, mostra un messaggio relativo alla regola violata e registra l'errore nel log.

Quindi un errore previsto dal dominio **non interrompe il programma**, ma viene gestito normalmente.

### Testing

Per verificare il comportamento del sistema ho realizzato **test automatici organizzati per funzionalità**.

Ho testato principalmente:

* `Utente`;
* `Ticket`;
* `BugTicket`;
* `FeatureTicket`;
* `Sprint`;
* `ConfigurazioneTeam`;
* `GestionaleJira`.

I test utilizzano `assert` e controllano anche le eccezioni attese.

Ho verificato sia i casi corretti sia situazioni di errore, come dati non validi, duplicati, permessi insufficienti, assegnazioni non consentite, superamento del limite di carico e transizioni di stato non valide.

In questo modo ho verificato che il sistema non funzionasse soltanto nei casi normali, ma rispettasse effettivamente le principali regole di business.

---

# 6. Conclusione

In conclusione, con **Mini-Jira CLI Task Manager** ho cercato di trasformare delle regole tipiche di un team di sviluppo in **comportamenti concreti del software**.

Per farlo ho utilizzato:

* un'architettura modulare;
* programmazione ad oggetti con ereditarietà e polimorfismo;
* controllo dei permessi;
* workflow obbligatorio;
* limite sul carico di lavoro;
* eccezioni personalizzate;
* validazione degli input;
* logging;
* test automatici;
* un servizio dedicato alle statistiche.

A questo punto mostrerei brevemente il funzionamento direttamente da terminale, concentrandomi su **limite di carico e workflow**.

---

# 🖥️ Demo al terminale

## 1. Limite di carico

Accedo come **PM**, creo quattro ticket e provo ad assegnarli tutti a `pippo`.

Il limite predefinito è 3, quindi dopo le prime tre assegnazioni:

```text
Carico: 3/3
```

Quando provo ad assegnare il quarto ticket, il sistema solleva `LimiteCaricoLavoroSuperatoError`.

La CLI intercetta l'errore e mostra il messaggio relativo alla regola di business.

> "Quindi il sistema impedisce automaticamente di superare il limite di carico."

## 2. Workflow

Effettuo il logout e accedo come `pippo`.

Prendo uno dei ticket assegnati e lo porto avanti:

```text
TODO → IN_PROGRESS → IN_REVIEW → DONE
```

Ad ogni passaggio il sistema controlla che io sia l'assegnatario e che la transizione sia valida.

Quindi, ad esempio, non posso passare direttamente da `TODO` a `DONE`.

## 3. Risultato

Prima di completare il ticket:

```text
Carico: 3/3
```

Dopo averlo portato a `DONE`:

```text
Carico: 2/3
```

Si libera quindi uno spazio e posso nuovamente assegnare un ticket a `pippo`.

> "In questo modo posso vedere concretamente come una regola di business venga trasformata in un comportamento automatico del software."
