# Lab Validatore Email/Password e Analisi Testo

## Avvio
python main.py

## Struttura

- `main.py`: menu e interazione con l'utente (unico file con input/print)
- `validatori.py`: validazione email e password
- `analisi.py`: analisi del testo ed estrazione dati con regex
- `report.py`: batch e generazione del report finale
- `input_prova/`: file di input e output (`emails.txt`, `passwords.txt`, `testo.txt`, `report.txt`)

## Regole email
- Normalizzazione: strip() degli spazi e conversione in minuscolo
- Pattern (re.fullmatch): nome con lettere, numeri e . _ % + -,
  una @, dominio con lettere, numeri e trattini,
  estensione finale di almeno 2 lettere
- Rifiutate: input vuoto, più lunghe di 200 caratteri, formato non valido

## Politica password
- Almeno 8 caratteri
- Almeno una maiuscola, una minuscola, un numero
- Almeno un simbolo tra !@#$%^&*
- Nessuno spazio
- Ogni regola violata produce un messaggio di errore separato

## Analisi testo
Caratteri, parole, frasi, 5 parole più frequenti, parola più lunga.

## Estrazione dati (regex)
Email, telefoni (es. +39 333 1234567), date (gg/mm/aaaa), URL.
Se un tipo di dato non è presente, viene mostrato "assente".

## Casi limite gestiti
Input vuoto, spazi iniziali/finali, maiuscole nelle email,
input troppo lungo, lista batch con righe vuote.

## Modalità batch
Legge un file con un elemento per riga, mostra l'esito di ognuno
e un riepilogo (totale, validi, non validi).

## Report

Il report finale raccoglie i risultati della sessione corrente e mostra:

- numero di email controllate, valide e non valide
- numero di password controllate, valide e non valide
- numero di testi analizzati
- dettagli degli elementi non validi

Il report viene salvato automaticamente in:

`input_prova/report.txt`