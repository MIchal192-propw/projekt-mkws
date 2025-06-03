# Cantera tutorial

import cantera as ct
import numpy as np

gas1 = ct.Solution('gri30.yaml')     #pliki do mechanizmu reakcji w pythonie

# print(gas1())

gas1.X = 'CH4:1, O2:2, N2:7.52'

gas1.TP = 500, 101325

# print(gas1.P)
# print(gas1.T)
# print(gas1.X)

phiList = [0.2, 0.3, 0.4, 0.5, 0.7, 0.8, 0.9, 1.0]  # fi dla paru przypadków i można by w pętli liczyć

tList = [300, 400, 500, 600]

# for phi in phiList:
# 	gas1 = ct.Solution('gri30.yaml')
# 	gas1.X = 'CH4:1, O2:2, N2:7.52'

# 	gas1.TP = 300, 101325

# 	gas1.X = {'CH4':1, 'O2':2/phi, 'N2':2*3.76/phi}  #pętla dla stanu równowagi
# 	#gas1.TPX = 1200, 101325, 'CH4:1, O2:2, N2:7.52'
# 	gas1.equilibrate('HP') # UV
# 	print(gas1())


gas1.equilibrate('HP')  #Oblicza stan równowagi chemicznej mieszaniny przy stałej entalpii (H) i ciśnieniu (P), co odpowiada procesowi adiabatycznemu przy stałym ciśnieniu

print(gas1())   #wyświelta szczególowe dane o temperaturz i entalipi itp

print(gas1.X)   #wypliuj liczbę moli
print(gas1.Y)   #wypluj skład masowy










