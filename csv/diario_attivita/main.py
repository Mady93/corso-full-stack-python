# Esercizio 10 - Diario completo
# Realizza un'applicazione da terminale per diario e log attività con
# creazione, consultazione, ricerca, export CSV, import CSV e riepilogo dati.
#
# Questo file contiene solo il menu: la logica sta nel pacchetto moduli/.
# File usati (cartella dati/):
#   diario.txt - voci di diario: data ora | testo
#   attivita.log - log attività: data ora | categoria | descrizione | minuti
#   attivita_export.csv - creato dall'esportazione
#   attivita_esempio.csv - (default) file da cui importare

from moduli import (nuova_voce, nuova_attivita, consulta_diario, 
                    consulta_log, cerca, esporta_csv, importa_csv, riepilogo)

# Ogni voce del menu: tasto - (testo mostrato, funzione da chiamare).
# Per aggiungere una funzione basta aggiungere una riga qui.
VOCI_MENU = {
    "1": ("Nuova voce di diario", nuova_voce),
    "2": ("Nuova attività nel log", nuova_attivita),
    "3": ("Consulta il diario", consulta_diario),
    "4": ("Consulta il log", consulta_log),
    "5": ("Cerca", cerca),
    "6": ("Esporta il log in CSV", esporta_csv),
    "7": ("Importa attività da CSV", importa_csv),
    "8": ("Riepilogo dati", riepilogo),
}


def main():
    while True:
        print("\n=== DIARIO E LOG ATTIVITÀ ===")
        for tasto, (descrizione, _) in VOCI_MENU.items():
            print(f"{tasto}) {descrizione}")
        print("0) Esci")
        scelta = input("Scelta: ").strip()

        if scelta == "0":
            print("Arrivederci!")
            break
        elif scelta in VOCI_MENU:
            # [1] = la funzione, poi () per eseguirla
            VOCI_MENU[scelta][1]()
        else:
            print("Scelta non valida.")


if __name__ == "__main__":
    main()