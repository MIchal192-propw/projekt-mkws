import cantera as ct
import numpy as np
import matplotlib.pyplot as plt

# === PARAMETRY OGÓLNE ===
compression_ratio = 10.0
T1 = 300.0  # [K] warnki początkowe
P1 = ct.one_atm  # [Pa]  warunki początkowe
phi_range = np.arange(0.5, 1.5, 0.1)  # rozkład pi od 0,5 do 1.5 phi

# === TABLICE WYNIKÓW ===
phis = [] #Wyniki phi zapisuje do tablicy , potrzebne do tabeli na koniec
T3_list = [] #tak samo temperaturę
W_netto_list = []  #tak samo moc

print("\n=== OBIEG OTTO: DANE DLA RÓŻNYCH φ ===")
print(f"{'φ':>5} | {'T3 [K]':>10} | {'W_netto [J/kg]':>16}")
print("-" * 36)

# === PĘTLA PO WARTOŚCIACH phi ===
for phi in phi_range:
    gas = ct.Solution('gri30.yaml')  # gaz że stosujemy mechanizm reakcji grid30.yaml
    gas.set_equivalence_ratio(phi, fuel='H2', oxidizer={'O2': 1.0, 'N2': 3.76})  # ustalamy skład mieszanki , a i tak phi to definuje
    gas.TP = T1, P1

    # Stan 1
    s1 = gas.s   # stan początkowy
    u1 = gas.int_energy_mass

    # Stan 2
    gas.SP = s1, P1 * (compression_ratio ** 1.4)  # reakcja sprężnia mieszanki
    T2 = gas.T
    P2 = gas.P
    u2 = gas.int_energy_mass

    # Stan 3
    gas.TP = T2, P2
    gas.equilibrate('UV')     #reakcja spalania stała objetośc i stała entallpia
    T3 = gas.T
    P3 = gas.P
    u3 = gas.int_energy_mass
    print(gas())  # WYDRUK jak na obrazku działa stan w spalaniu jakieś analizy z tego

    # Stan 4
    s3 = gas.s
    gas.SP = s3, P3 / (compression_ratio ** 1.4)
    T4 = gas.T
    u4 = gas.int_energy_mass

    # Praca netto
    W_netto = (u3 - u4) - (u2 - u1)

    # Zapis do list
    phis.append(phi)
    T3_list.append(T3)
    W_netto_list.append(W_netto)

    # === PRINT do CMD ===
    print(f"{phi:>5.2f} | {T3:>10.2f} | {W_netto:>16.2f}")

# === WYKRESY ===
plt.figure(figsize=(12, 5))

# T3 od phi
plt.subplot(1, 2, 1)
plt.plot(phis, T3_list, marker='o', color='red')
plt.xlabel('Współczynnik ekwiwalentności φ')
plt.ylabel('Temperatura maksymalna T3 [K]')
plt.title('Temperatura spalania T3 vs φ')
plt.grid(True)

# W_netto od phi
plt.subplot(1, 2, 2)
plt.plot(phis, W_netto_list, marker='s', color='blue')
plt.xlabel('Współczynnik ekwiwalentności φ')
plt.ylabel('Praca netto [J/kg]')
plt.title('Praca netto vs φ')
plt.grid(True)


plt.tight_layout()
plt.show(block=False)  # nie blokuje terminala
input("\nNaciśnij Enter, aby zakończyć...")  # czeka na użytkownika




