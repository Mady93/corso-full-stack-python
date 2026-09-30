# Backup selettivo del workspace Python

## Avvio
Eseguire i file in quest'ordine, dalla cartella lab_backup:
1. python crea_prova.py   (crea la cartella di prova workspace_prova/, una volta sola)
2. python main.py         (esegue il backup; ripeterlo per le prove: 1° run, 2° run, 3° run)
3. python verifica.py     (controlla che l'ultimo backup combaci con workspace_prova/)

## Struttura
- main.py: menu e interazione (unico file con input/print)
- backup.py: validazione, selezione, copia, rotazione dei backup, spostamento
- crea_prova.py: genera la cartella di prova
- verifica.py: confronta workspace_prova/ con l'ultimo backup (file mancanti, file in più, contenuto diverso)
- workspace_prova/: cartella di prova da copiare
- backup_output/: backup creati dal programma (al massimo 2)
- backup_output/_in_corso/: cartella temporanea usata durante la copia

## Criteri di selezione
Escluse le cartelle __pycache__, .venv, venv, .git, node_modules, .idea,
backup_output e i file .pyc, .tmp, .log.
Tutto il resto viene copiato mantenendo la struttura delle sottocartelle.

## Destinazione
backup_output/backup_AAAA-MM-GG_HH-MM-SS/
Vengono conservati al massimo 2 backup. Prima di copiare il programma controlla quanti ne esistono
e legge la data dal nome della cartella: se ce ne sono già 2, elimina il meno recente e lo sostituisce.
La copia avviene in backup_output/_in_corso/ e viene spostata (shutil.move) nella cartella finale
solo a copia completata, così un'interruzione non danneggia i backup esistenti.
Eliminazione e spostamento sono permessi solo dentro backup_output.

## Percorsi non validi
Controllati prima di copiare: vuoto, inesistente, non cartella,
radice del disco, cartella dentro backup_output, cartella vuota.

## Archivio finale
Non realizzato: la copia resta in cartelle direttamente consultabili.

## Riepilogo
File copiati con dimensione totale, file esclusi, eventuali errori
e elenco dei backup conservati.

## Verifica minima
- Directory iniziale non vuota, più tipi di file, sottocartella: workspace_prova/
- Destinazione assente: primo run (0/2 backup presenti)
- Destinazione già esistente: secondo run (1/2, si aggiunge) e terzo run (2/2, sostituisce il meno recente)
- Percorso non valido: C:\cartella_finta
- Copia (shutil.copy2) e spostamento (shutil.move da _in_corso alla cartella finale)
- Copia corretta: verifica.py stampa "nessuno" su file mancanti, file in più e contenuto diverso