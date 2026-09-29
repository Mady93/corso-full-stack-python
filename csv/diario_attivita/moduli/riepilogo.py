# Riepilogo dei dati di diario e log.

from .archivio import leggi_righe
from .config import FILE_DIARIO
from .eventi import leggi_log


def riepilogo():
    voci = leggi_righe(FILE_DIARIO)
    eventi = leggi_log()
    print("\n=== RIEPILOGO ===")
    print(f"Voci di diario   : {len(voci)}")
    print(f"Attività nel log : {len(eventi)}")
    if not eventi:
        return

    totale = sum(e["durata"] for e in eventi)
    print(f"Tempo totale     : {totale // 60} h {totale % 60:02d} min ({totale} min)")
    print(f"Durata media     : {totale / len(eventi):.1f} min")

    per_categoria = {}
    for e in eventi:
        per_categoria[e["categoria"]] = per_categoria.get(e["categoria"], 0) + e["durata"]
    print("\nMinuti per categoria:")
    for categoria, minuti in sorted(per_categoria.items(), key=lambda x: x[1], reverse=True):
        print(f"  {categoria:<10} {minuti:>4} min")