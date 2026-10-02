# Rubrica contatti (Python + MySQL)

Applicazione da terminale per gestire una rubrica persistente in MySQL.

## Installazione

1. Installa Python, MySQL Server e le librerie:

   ```bash
   py -m pip install mysql-connector-python python-dotenv
   ```

2. Crea nella radice del progetto un file `.env` (non va su Git):

   ```env
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=root
   DB_PASSWORD=la_tua_password
   DB_NAME=
   ```

3. Non serve creare il database a mano: l'applicazione crea automaticamente database, tabelle e categorie predefinite al primo avvio (lo script SQL utilizzato è `schema.sql`).

## Utilizzo (dalla radice del progetto)

```bash
py -m rubrica_db_lab.main
```

Menu: nuovo contatto, elenco, dettaglio, ricerca (più criteri insieme), modifica, elimina (con conferma), categorie, esporta CSV, importa CSV.

## CSV

**Colonne:**

```text
nome;cognome;telefono;email;note;categorie
```

Le categorie sono separate dal carattere `|`.

Esempio:

```text
Amici|Lavoro
```

Il separatore delle colonne può essere:

* `;`
* `,`

Durante l'importazione:

* i contatti già presenti vengono saltati;
* le righe non valide vengono saltate;
* al termine viene mostrato un riepilogo con il numero di righe lette, importate, duplicate e non valide.

## Test

I test sono realizzati tramite uno script Python che:

1. crea un database di test;
2. inserisce automaticamente dei dati;
3. esegue automaticamente ricerche, modifiche, eliminazioni ed operazioni di export/import;
4. controlla automaticamente i risultati;
5. stampa `OK` o `KO` per ogni verifica;
6. alla fine elimina il database di test.

Per eseguire i test:

```bash
py -m rubrica_db_lab.test_rubrica
```

I test utilizzano un database separato (`rubrica_test`), che viene eliminato automaticamente al termine dell'esecuzione.
