"""
Lab: Sistema Gestione Flotta Veicoli
OOP -- Classi, Ereditarietà, super(), Override, Polimorfismo

Nessun try/except/raise: ogni operazione rischiosa passa per un metodo
factory (`crea()`) o restituisce True/False/None, e il codice controlla
semplicemente il risultato con un `if`.

STRUTTURA DEL PROGETTO
----------------------
polymorphism/
├── main_vehicle_fleet.py
└── vehicle_fleet_management/
    ├── __init__.py
    ├── elettrica.py
    ├── gestione_flotta.py
    ├── noleggio.py
    ├── suv.py
    ├── utilitaria.py
    ├── validazioni.py
    └── veicolo.py


GERARCHIA DELLE CLASSI
----------------------
Veicolo
├── Utilitaria
├── Suv
└── Elettrica



RELAZIONI TRA LE CLASSI
-----------------------
GestioneFlotta
├── contiene → Veicolo
│   └── gestisce la lista dei veicoli registrati
├── contiene → Noleggio
│   └── gestisce la lista dei noleggi attivi
└── utilizza → validazioni.py
    └── valida i chilometri percorsi alla restituzione

Noleggio
├── associazione → Veicolo
│   └── mantiene un riferimento al veicolo noleggiato
└── utilizza → validazioni.py
    └── valida i dati del noleggio

Veicolo
└── utilizza → validazioni.py
    └── valida i dati comuni del veicolo

Utilitaria
└── eredita → Veicolo
    └── esegue l'override di calcola_preventivo() e descrivi()

Suv
├── eredita → Veicolo
├── utilizza → validazioni.py
│   └── valida i dati specifici della trazione integrale
└── esegue l'override di calcola_preventivo() e descrivi()

Elettrica
├── eredita → Veicolo
├── utilizza → validazioni.py
│   └── valida autonomia e tempo di ricarica
└── esegue l'override di calcola_preventivo() e descrivi()



DIPENDENZE TRA I FILE
---------------------
main_vehicle_fleet.py
    ├── importa Veicolo
    ├── importa Utilitaria
    ├── importa Suv
    ├── importa Elettrica
    ├── importa Noleggio
    └── importa GestioneFlotta

veicolo.py
    └── utilizza validazioni.py

utilitaria.py
    └── eredita da veicolo.py

suv.py
    ├── eredita da veicolo.py
    └── utilizza validazioni.py

elettrica.py
    ├── eredita da veicolo.py
    └── utilizza validazioni.py

noleggio.py
    ├── utilizza Veicolo
    └── utilizza validazioni.py

gestione_flotta.py
    ├── utilizza Veicolo
    ├── utilizza Noleggio
    └── utilizza validazioni.py

validazioni.py
    └── fornisce funzioni di validazione riutilizzabili
        dalle altre classi
"""

##### SISTEMA GESTIONE FLOTTA VEICOLI #####

# Veicolo è la classe base e da essa derivano Utilitaria, Suv ed Elettrica,
# che ereditano le caratteristiche comuni e personalizzano alcuni comportamenti.
#
# Noleggio rappresenta un noleggio associato a un veicolo, mentre GestioneFlotta
# gestisce i veicoli registrati, i noleggi, le restituzioni, la disponibilità
# e la manutenzione.
#
# Le funzioni di validazione controllano che i dati inseriti siano corretti.
#
# Nel main creo i veicoli tramite i metodi factory, li registro nella flotta,
# calcolo i preventivi, effettuo e restituisco i noleggi e verifico i vari
# controlli e casi di errore.
#
# Il progetto utilizza classi, ereditarietà, super(), override e polimorfismo.
#
# L'incapsulamento degli attributi è realizzato tramite @property e setter,
# che permettono di controllare l'accesso e la modifica dei dati interni
# degli oggetti.

from vehicle_fleet_management.elettrica import Elettrica
from vehicle_fleet_management.gestione_flotta import GestioneFlotta
from vehicle_fleet_management.noleggio import Noleggio
from vehicle_fleet_management.suv import Suv
from vehicle_fleet_management.utilitaria import Utilitaria
from vehicle_fleet_management.veicolo import Veicolo


def main() -> None:
    """Create fleet objects and demonstrate every operation and check."""

    # 1. PARCO VEICOLI -- creo tre tipologie diverse, tramite crea()
    flotta = GestioneFlotta()

    city_car = Utilitaria.crea("ab123cd", "Fiat", "Panda", 4, 12_000, 35.0)
    suv = Suv.crea("ef456gh", "Jeep", "Compass", 5, 8_000, 55.0, True)
    ev = Elettrica.crea(
        "il789mn",
        "Tesla",
        "Model 3",
        5,
        5_000,
        60.0,
        500,
        0.5,
    )

    # 2. Registrazione in flotta
    flotta.registra_veicolo(city_car)
    flotta.registra_veicolo(suv)
    flotta.registra_veicolo(ev)

    print()
    print("----- FLEET VEHICLES (polymorphism: same method, different output) -----")

    for v in flotta.veicoli:
        print(v.descrivi())

    print()

    # 3. Consultazione disponibilità
    print("----- AVAILABLE VEHICLES -----")

    for v in flotta.veicoli_disponibili():
        print(v.descrivi())

    print()

    # 4. Preventivi su misura
    print("----- RENTAL QUOTES (3 days and 10 days) -----")

    for v in flotta.veicoli:
        p3 = v.calcola_preventivo(3)
        p10 = v.calcola_preventivo(10)

        print(f"{v.targa}: 3 days = €{p3:.2f} | 10 days = €{p10:.2f}")

    print()

    # calcola_preventivo(): giorni non validi direttamente sul veicolo
    print("----- CALCULATE_QUOTE: INVALID DAYS -----")

    city_car.calcola_preventivo(0)
    city_car.calcola_preventivo("tre")

    print()

    # 5. Noleggio: caso di successo
    print("----- RENTAL -----")

    noleggio1 = flotta.noleggia("AB123CD", 3)

    if noleggio1 is not None:
        print(noleggio1.descrivi())

    print()

    # 6. noleggia(): copro i possibili rami
    print("----- RENTAL: BUSINESS CHECKS -----")

    # A) targa inesistente
    flotta.noleggia("ZZ000ZZ", 3)

    # B) veicolo già in noleggio
    flotta.noleggia("AB123CD", 2)

    # C) targa di tipo errato
    flotta.noleggia(12345, 3)

    # D) giorni non validi
    flotta.noleggia("IL789MN", 0)

    # E) giorni di tipo errato
    flotta.noleggia("IL789MN", "tre")

    # Simulo che il SUV abbia superato la soglia di manutenzione
    suv.km_totali += 15_000

    # F) veicolo che necessita manutenzione
    flotta.noleggia("EF456GH", 3)

    print()

    # 7. Manutenzione
    print("----- MAINTENANCE -----")

    # A) targa inesistente
    flotta.effettua_manutenzione("ZZ000ZZ")

    # B) manutenzione corretta
    eseguita = flotta.effettua_manutenzione("EF456GH")
    print(f"SUV maintenance completed: {eseguita}")

    # C) dopo la manutenzione il noleggio riesce
    noleggio2 = flotta.noleggia("EF456GH", 8)

    if noleggio2 is not None:
        print(noleggio2.descrivi())

    # D) veicolo attualmente in noleggio
    flotta.effettua_manutenzione("EF456GH")

    print()

    # 8. Restituzione
    print("----- RETURN -----")

    # km_percorsi non validi
    flotta.restituisci("EF456GH", km_percorsi=-50)
    flotta.restituisci("EF456GH", km_percorsi="tanti")

    # restituzione corretta
    restituito = flotta.restituisci("AB123CD", km_percorsi=250)

    if restituito is not None:
        print(
            f"Returned: {restituito.descrivi()} - "
            f"distance travelled: {restituito.km_percorsi} km"
        )

    # restituzione senza noleggio attivo
    flotta.restituisci("IL789MN")

    print()

    # 9. Veicoli da revisionare
    print("----- VEHICLES REQUIRING MAINTENANCE -----")

    # Forzo il superamento della soglia sulla city car
    city_car.km_totali += city_car.SOGLIA_KM_MANUTENZIONE

    veicoli_revisionare = flotta.veicoli_da_revisionare()

    for v in veicoli_revisionare:
        print(v.descrivi())

    # Dopo la manutenzione la lista torna vuota
    flotta.effettua_manutenzione("AB123CD")

    if not flotta.veicoli_da_revisionare():
        print("No vehicles currently require maintenance")

    print()

    # 10. VALUE CHECKS: testo_valido()
    print("----- VALUE CHECKS: testo_valido() -----")

    # targa non stringa
    Veicolo.crea(123, "Fiat", "500", 4, 0, 30.0)

    # targa vuota
    Veicolo.crea("", "Fiat", "500", 4, 0, 30.0)

    # marca vuota
    Utilitaria.crea("op321qr", "", "500", 4, 0, 30.0)

    # modello vuoto
    Suv.crea("st654uv", "Jeep", "", 5, 0, 50.0, True)

    print()

    # 11. VALUE CHECKS: intero_positivo()
    print("----- VALUE CHECKS: intero_positivo() -----")

    # posti non intero
    Utilitaria.crea(
        "wx987yz",
        "Fiat",
        "500",
        "quattro",
        0,
        30.0,
    )

    # posti è un bool (trappola)
    Utilitaria.crea(
        "wx987yz",
        "Fiat",
        "500",
        True,
        0,
        30.0,
    )

    # posti = 0
    Utilitaria.crea(
        "wx987yz",
        "Fiat",
        "500",
        0,
        0,
        30.0,
    )

    # autonomia negativa
    Elettrica.crea(
        "aa111bb",
        "Tesla",
        "Model Y",
        5,
        0,
        60.0,
        -10,
        0.5,
    )

    print()

    # 12. VALUE CHECKS: intero_non_negativo()
    print("----- VALUE CHECKS: intero_non_negativo() -----")

    # km_totali negativo
    Utilitaria.crea(
        "cc222dd",
        "Fiat",
        "500",
        4,
        -100,
        30.0,
    )

    # km_totali tipo errato
    Utilitaria.crea(
        "dd222ee",
        "Fiat",
        "500",
        4,
        "dodicimila",
        30.0,
    )

    print()

    # 13. VALUE CHECKS: numero_positivo()
    print("----- VALUE CHECKS: numero_positivo() -----")

    # tariffa non numero
    Utilitaria.crea(
        "ee333ff",
        "Fiat",
        "500",
        4,
        0,
        "trenta",
    )

    # tariffa negativa
    Utilitaria.crea(
        "ee333ff",
        "Fiat",
        "500",
        4,
        0,
        -30.0,
    )

    # ricarica negativa
    Elettrica.crea(
        "gg444hh",
        "Tesla",
        "Model Y",
        5,
        0,
        60.0,
        400,
        -1.0,
    )

    print()

    # 14. VALUE CHECKS: booleano_valido()
    print("----- VALUE CHECKS: booleano_valido() -----")

    # trazione non booleana
    Suv.crea(
        "ii555jj",
        "Jeep",
        "Renegade",
        5,
        0,
        45.0,
        "si",
    )

    print()

    # 15. Noleggio.crea(): controlli
    print("----- Noleggio.crea() CHECKS -----")

    # veicolo errato
    Noleggio.crea("non è un veicolo", 3, 100.0)

    # giorni tipo errato
    Noleggio.crea(city_car, "tre", 100.0)

    # preventivo tipo errato
    Noleggio.crea(city_car, 3, "cento")

    # giorni booleano
    Noleggio.crea(city_car, True, 100.0)

    # giorni <= 0
    Noleggio.crea(city_car, 0, 100.0)

    # preventivo booleano
    Noleggio.crea(city_car, 3, True)

    # preventivo <= 0
    Noleggio.crea(city_car, 3, 0)

    print()

    # 16. GestioneFlotta: controlli
    print("----- GESTIONEFLOTTA CHECKS -----")

    # tipo non valido
    flotta.registra_veicolo("non è un veicolo")

    # creo un veicolo non valido -> None
    veicolo_fallito = Utilitaria.crea(
        "",
        "Fiat",
        "500",
        4,
        0,
        30.0,
    )

    # None viene bloccato comunque
    flotta.registra_veicolo(veicolo_fallito)

    # creo un veicolo con targa già registrata
    duplicato = Utilitaria.crea(
        "AB123CD",
        "Fiat",
        "Punto",
        4,
        0,
        28.0,
    )

    # targa duplicata
    flotta.registra_veicolo(duplicato)

    print()

    # 17. Stato finale della flotta
    print("----- FLEET STATUS -----")
    print(flotta.stato_flotta())


if __name__ == "__main__":
    main()