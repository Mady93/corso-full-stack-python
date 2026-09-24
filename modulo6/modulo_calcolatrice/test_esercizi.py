import calcolatrice
import utility_casuali


print("Attività 1")

print(calcolatrice.somma(10, 5))
print(calcolatrice.sottrai(10, 5))
print(calcolatrice.moltiplica(10, 5))
print(calcolatrice.dividi(10, 5))


print("\nAttività 2")

exec(open("main_calcolatrice.py").read())


print("\nAttività 3")

exec(open("casuale_base.py").read())


print("\nAttività 4")

print(utility_casuali.lancia_dado())

nomi = ["Anna", "Luca", "Marco", "Sara"]
print(utility_casuali.estrai_nome(nomi))

print(utility_casuali.genera_password(10))


print("\nAttività 5")

exec(open("gioco_casuale.py").read())


print("\nAttività 6")

print(calcolatrice.potenza(2, 3))
print(calcolatrice.resto(10, 3))
print(calcolatrice.radice_quadrata(9))


print("\nAttività 7")

exec(open("progetto_completo/main.py").read())