import numpy as np
import pandas as pd
import enthalpy_IL_function as h_IL

temperature = 25
h = h_IL.enthalpy_IL('[hmim][Tf2N]', temperature)

print("The enthalpy of [hmim][Tf2N] at 25 Celsius is:", h, "kJ/kg")
