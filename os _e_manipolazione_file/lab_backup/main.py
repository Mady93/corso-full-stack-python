"""Interfaccia da terminale del backup selettivo (unico file con input e print)."""

import os

from backup import (BASE_DIR, MAX_BACKUP, TEMP_DIR, Riepilogo, valida_origine, nuovo_nome_backup,
                    elenca_backup, backup_da_eliminare, elimina_backup, pulisci_temp,
                    pubblica_backup, copia_selettiva)

# Cartella copiata se l'utente preme solo Invio
ORIGINE_DEFAULT: str = os.path.join(BASE_DIR, "workspace_prova")


def chiedi_origine() -> str:
    """Chiede la cartella da copiare; senza risposta usa quella di prova."""
    # strip() toglie gli spazi, strip('"') toglie le virgolette che Windows aggiunge con "Copia come percorso"
    raw = input(f"Cartella da copiare [{ORIGINE_DEFAULT}]: ").strip().strip('"')
    return os.path.abspath(raw) if raw else ORIGINE_DEFAULT


def stampa_riepilogo(riepilogo: Riepilogo, destinazione: str) -> None:
    """Stampa l'esito del backup: copiati, esclusi, errori e backup conservati."""
    print("\n=== RIEPILOGO BACKUP ===")
    print(f"Destinazione: {destinazione}")
    print(f"File copiati: {len(riepilogo['copiati'])} ({riepilogo['byte'] / 1024:.1f} KB)")
    for f in riepilogo["copiati"]:
        print(f"  ✔ {f}")
    print(f"Esclusi: {len(riepilogo['esclusi'])}")
    for f in riepilogo["esclusi"]:
        print(f"  – {f}")
    if riepilogo["errori"]:
        print(f"Errori: {len(riepilogo['errori'])}")
        for e in riepilogo["errori"]:
            print(f"  ✘ {e}")
    presenti = elenca_backup()
    print(f"Backup conservati ({len(presenti)}/{MAX_BACKUP}):")
    for p in presenti:
        print(f"  • {os.path.basename(p)}")


def esegui_backup() -> None:
    """Flusso completo: origine, validazione, copia in temp, sostituzione del meno recente, spostamento."""
    origine = chiedi_origine()
    ok, msg = valida_origine(origine)
    if not ok:
        print("✘", msg)
        return

    # Se un backup precedente è stato interrotto, tolgo il residuo
    pulisci_temp()
    print(f"Backup già presenti: {len(elenca_backup())}/{MAX_BACKUP}")

    # Copio prima in una cartella temporanea: se qualcosa va storto i vecchi backup restano intatti
    riepilogo = copia_selettiva(origine, TEMP_DIR)

    # Se ho già MAX_BACKUP copie elimino la meno recente (la data è nel nome della cartella)
    for vecchio in backup_da_eliminare():
        print(f"Sostituisco il backup meno recente: {os.path.basename(vecchio)}")
        elimina_backup(vecchio)

    # Sposto la copia completata dalla cartella temporanea alla destinazione finale
    destinazione = pubblica_backup(TEMP_DIR, nuovo_nome_backup())
    stampa_riepilogo(riepilogo, destinazione)


def main() -> None:
    """Menu principale."""
    while True:
        print("\n1) Esegui backup")
        print("0) Esci")
        scelta = input("> ").strip()
        if scelta == "0":
            break
        if scelta == "1":
            esegui_backup()
        else:
            print("Scelta non valida")


if __name__ == "__main__":
    main()