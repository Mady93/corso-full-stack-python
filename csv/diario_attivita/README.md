# Diario e log attività

Applicazione da terminale per gestire un diario e un registro di attività,
con esportazione e importazione in formato CSV.

## Struttura

```
diario_attivita/
├── main.py                       menu dell'applicazione (esercizio 10)
├── README.md
├── moduli/
│   ├── __init__.py
│   ├── config.py                 percorsi e costanti
│   ├── archivio.py               lettura e scrittura dei file di testo
│   ├── eventi.py                 formato del log (riga <-> evento)
│   ├── diario.py                 nuove voci di diario
│   ├── attivita.py               nuove attività nel log
│   ├── consultazione.py          consultazione e ricerca
│   ├── scambio_csv.py            esportazione e importazione CSV
│   └── riepilogo.py              riepilogo dei dati
├── dati/
│   ├── diario.txt
│   ├── attivita.log
│   ├── attivita_esempio.csv      CSV fornito dal laboratorio
│   └── attivita_export.csv       generato dall'esportazione
└── esercizi/
    ├── salva_voce.py             1  salva una voce di diario
    ├── mostra_voci.py            2  visualizza tutte le voci
    ├── cerca_voci.py             3  cerca testo nel diario
    ├── registra_attivita.py      4  registra un'attività con timestamp
    ├── filtra_log.py             5  filtra gli eventi del log
    ├── esporta_csv.py            6  esporta il log in CSV
    ├── importa_csv.py            7  importa e consulta un CSV
    ├── statistiche_attivita.py   8  statistiche dal CSV
    └── modifica_elimina.py       9  modifica o elimina dati
```

Gli script in `esercizi/` sono indipendenti tra loro e dai moduli.

## Esecuzione

Dalla cartella del progetto:

```
py main.py
py esercizi/salva_voce.py
```

## Formati

- Diario: `2026-09-29 08:00 | testo della voce`
- Log: `2026-09-29 08:15 | studio | Revisione appunti | 45`
- CSV: `id,data_ora,categoria,descrizione,durata_minuti`