# File manager da terminale

Applicazione unica che integra un **file explorer testuale** e un **sistema di backup di cartelle**.
Richiede Python 3.10 o superiore e usa solo la libreria standard (`pathlib`, `os`, `shutil`, `datetime`, `zipfile`).

## Avvio

Dalla cartella del progetto:

    py main.py

## Struttura

```text
file_manager/
├── main.py                 menu principale: coordina explorer e backup
├── README.md               descrizione del progetto e delle scelte progettuali
├── backup/                 contiene i backup creati dal programma
├── test/                   cartella di prova per le dimostrazioni creata dal terminale
│   ├── dati/
│   │   └── dati_prova.csv
│   └── documenti/
│       ├── appunti.txt
│       └── relazione.md
└── moduli/
    ├── __init__.py
    ├── config.py           percorsi predefiniti, inclusa la cartella dei backup
    ├── utilita.py          formattazione di dimensioni e date e funzioni di input
    ├── analisi.py          statistiche ricorsive su una cartella
    ├── explorer.py         esploratore testuale e operazioni sui file
    └── backup.py           creazione, elenco, eliminazione e ripristino dei backup
```

   
## Menu

    FILE MANAGER

    1. Esplora cartella
    2. Analizza cartella
    3. Crea backup
    4. Gestisci backup
    5. Esci

Nell'explorer, `aiuto` mostra tutti i comandi. Gli elementi si scelgono con il numero
dell'elenco o con il nome. Il comando `seleziona` fa diventare la cartella corrente la
sorgente proposta dalla voce 3 (Crea backup).

## Scelte progettuali

- **Percorsi:** tutto il codice usa `pathlib`, quindi i percorsi funzionano su Windows, macOS e Linux.
  `os.walk` è usato solo per attraversare l'albero in modo robusto (non si ferma davanti a
  cartelle illeggibili). Nessun percorso è obbligatorio: la cartella dei backup è proposta
  ma modificabile a ogni operazione.
- **Backup:** l'utente sceglie tra cartella duplicata (`shutil.copytree`) e archivio ZIP
  (`shutil.make_archive`). Il nome `backup_AAAA-MM-GG_HH-MM-SS` contiene data e ora, quindi un
  backup non ne sovrascrive mai un altro. Dopo la creazione il programma confronta file,
  sottocartelle e byte con la sorgente e comunica se coincidono.
- **Destinazione:** se esiste già, i backup presenti non vengono toccati; se non esiste, il
  programma chiede conferma prima di crearla. Una destinazione dentro la sorgente viene
  rifiutata, perché il backup copierebbe sé stesso. Una copia interrotta a metà viene eliminata.
- **Operazioni distruttive:** eliminazione di backup, eliminazione di file, ripristino su una
  cartella non vuota e sovrascrittura di file richiedono una conferma esplicita (`s/n`).
  L'explorer elimina, copia e sposta solo file, non cartelle intere.
- **Ripristino:** la destinazione proposta è una cartella nuova (`ripristino_<nome backup>`),
  così il ripristino non tocca i dati originali a meno che l'utente lo chieda.
- **Errori:** i moduli sollevano `ErroreBackup` con messaggi già leggibili. Percorsi
  inesistenti, file al posto di cartelle, nomi non validi, accessi negati e ZIP danneggiati
  producono un messaggio e non interrompono il programma.
- **Codice:** `main.py` contiene solo il menu; explorer, backup e analisi sono moduli separati.
  Nei moduli la logica è separata dalle domande da terminale.

## Dimostrazione minima

1. `1` → `cartella_prova` → `ls`, `cd documenti`, `su`: esplorazione, file e sottocartelle.
2. `2` → `cartella_prova`: analisi (file, cartelle, spazio, estensioni, profondità).
3. `3` → `cartella_prova` → Invio → `1`: creazione di un backup.
4. `4` → Invio → `1`: elenco dei backup; `2` mostra le informazioni.
5. `1` → `cartella_prova` → `nuovo-file`, `rinomina`, `copia`, `leggi`: operazioni sui file.
6. `1` → `/percorso/inesistente`: gestione di un percorso non valido.

Le operazioni di eliminazione e ripristino vanno provate solo sulla cartella di prova.