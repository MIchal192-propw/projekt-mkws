import cantera as ct
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# === PARAMETRY OGÓLNE ===
compression_ratio = 10.0
T1 = 300.0  # [K]
P1 = ct.one_atm  # [Pa]
phi_range = np.arange(0.5, 1.5, 0.1)  # zakres współczynnika φ

# === TABLICE WYNIKÓW ===
phis = []
T3_list = []
W_netto_list = []
NO2_moles = []
N2O_moles = []

print("\n=== OBIEG DIESLA: DANE DLA RÓŻNYCH φ ===")
print(f"{'φ':>5} | {'T3 [K]':>10} | {'W_netto [J/kg]':>16} | {'NO2 [mol]':>10} | {'N2O [mol]':>10}")
print("-" * 66)

# === PĘTLA PO WARTOŚCIACH φ ===
for phi in phi_range:
    gas = ct.Solution('gri30.yaml')
    gas.set_equivalence_ratio(phi, fuel='H2', oxidizer={'O2': 1.0, 'N2': 3.76})
    gas.TP = T1, P1

    # Stan 1
    s1 = gas.s
    u1 = gas.int_energy_mass

    # === WYŚWIETL SKŁAD PO SPALANIU ===
    print("\nSkład mieszaniny po spalaniu (φ = {:.2f}):".format(phi))
    print(gas())  # pokazuje T, P, i skład molowy

    # Stan 2 – sprężanie adiabatyczne
    gas.SP = s1, P1 * (compression_ratio ** 1.4)
    u2 = gas.int_energy_mass

    # === WYŚWIETL SKŁAD PO SPALANIU ===
    print("\nSkład mieszaniny po spalaniu (φ = {:.2f}):".format(phi))
    print(gas())  # pokazuje T, P, i skład molowy

    # Stan 3 – spalanie przy stałym ciśnieniu
    gas.HP = gas.enthalpy_mass, gas.P
    gas.equilibrate('HP')
    T3 = gas.T
    u3 = gas.int_energy_mass

    # === WYŚWIETL SKŁAD PO SPALANIU ===
    print("\nSkład mieszaniny po spalaniu (φ = {:.2f}):".format(phi))
    print(gas())  # pokazuje T, P, i skład molowy

    # Ilości molowe zanieczyszczeń
    no2 = gas.X[gas.species_index('NO2')]
    n2o = gas.X[gas.species_index('N2O')]

    # Stan 4 – rozprężanie adiabatyczne
    gas.SP = gas.s, gas.P / (compression_ratio ** 1.4)
    u4 = gas.int_energy_mass

    # === WYŚWIETL SKŁAD PO SPALANIU ===
    print("\nSkład mieszaniny po spalaniu (φ = {:.2f}):".format(phi))
    print(gas())  # pokazuje T, P, i skład molowy

    # Praca netto
    W_netto = (u3 - u4) - (u2 - u1)

    # Zapis wyników
    phis.append(phi)
    T3_list.append(T3)
    W_netto_list.append(W_netto)
    NO2_moles.append(no2)
    N2O_moles.append(n2o)

    # PRINT
    print(f"{phi:>5.2f} | {T3:>10.2f} | {W_netto:>16.2f} | {no2:>10.3e} | {n2o:>10.3e}")

# === WYKRESY ===
plt.figure(figsize=(14, 6))

# Temperatura
plt.subplot(2, 2, 1)
plt.plot(phis, T3_list, marker='o', color='green')
plt.xlabel('Współczynnik ekwiwalentności φ')
plt.ylabel('Temperatura maksymalna T3 [K]')
plt.title('Temperatura spalania T3 vs φ (Diesel)')
plt.grid(True)
plt.ticklabel_format(style='plain', axis='y')

# Praca netto
plt.subplot(2, 2, 2)
plt.plot(phis, W_netto_list, marker='s', color='orange')
plt.xlabel('Współczynnik ekwiwalentności φ')
plt.ylabel('Praca netto [J/kg]')
plt.title('Praca netto vs φ (Diesel)')
plt.grid(True)
plt.ticklabel_format(style='plain', axis='y')

# NO2
plt.subplot(2, 2, 3)
plt.plot(phis, NO2_moles, marker='^', color='red')
plt.xlabel('Współczynnik ekwiwalentności φ')
plt.ylabel('Ilość NO₂ [mol]')
plt.title('Powstawanie NO₂ vs φ')
plt.grid(True)

# N2O
plt.subplot(2, 2, 4)
plt.plot(phis, N2O_moles, marker='v', color='blue')
plt.xlabel('Współczynnik ekwiwalentności φ')
plt.ylabel('Ilość N₂O [mol]')
plt.title('Powstawanie N₂O vs φ')
plt.grid(True)

plt.tight_layout()
plt.show(block=False)
input("\nNaciśnij Enter, aby zakończyć...")
