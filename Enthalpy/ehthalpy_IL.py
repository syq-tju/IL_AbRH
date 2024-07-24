import pandas as pd
import numpy as np

# Install tabulate if not already installed
try:
    import tabulate
except ModuleNotFoundError:
    import subprocess
    subprocess.check_call(['pip', 'install', 'tabulate'])
    import tabulate

# Define a function to calculate enthalpy at a given temperature T
def enthalpy_cal(T, C0, C1, C2, H_ref=200):
  """
  This function calculates the enthalpy of a substance at a given temperature T, based on its heat capacity parameters and a reference enthalpy.

  Args:
      T (float): The temperature in Kelvin at which to calculate the enthalpy.
      C0 (float): The constant term in the heat capacity equation.
      C1 (float): The coefficient of the linear term in the heat capacity equation.
      C2 (float): The coefficient of the quadratic term in the heat capacity equation.
      H_ref (float, optional): The reference enthalpy at 298.15 K in kJ/kg. Defaults to 200.

  Returns:
      float: The enthalpy of the substance at temperature T in kJ/kg.
  """
  T_ref = 298.15  # Reference temperature in Kelvin

  # Calculate the change in enthalpy due to the temperature difference
  delta_H = C0 * (T - T_ref) + 0.5 * C1 * (T**2 - T_ref**2) + (1 / 3) * C2 * (T**3 - T_ref**3)

  # Calculate the total enthalpy by adding the reference enthalpy
  H = delta_H + H_ref

  return H

# Function to calculate enthalpy from CSV data
def calculate_enthalpy_from_csv(file_path):
    """
    Calculates enthalpy values for ionic liquids from a CSV file containing heat capacity parameters and molar masses.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: A DataFrame containing enthalpy values (in kJ/kg) for each ionic liquid at different temperatures.
    """
    # Read the CSV file
    df_updated = pd.read_csv(file_path)

    # Create a Series of temperatures and convert to NumPy array
    T = pd.Series(np.arange(298.15, 373.15, 1))
    T_array = T.to_numpy()

    # Create an empty DataFrame to store enthalpy values
    enthalpy_df = pd.DataFrame(index=T)

    # Iterate through each row
    for index, row in df_updated.iterrows():
        # Get molar mass, skip if 'NA'
        molar_mass_str = row['Molar Mass (g/mol)']
        if molar_mass_str == 'NA':
            continue
        molar_mass = float(molar_mass_str)

        # Convert H_ref from kJ/kg to J/mol
        H_ref = 200 * molar_mass

        # Calculate the change in enthalpy using array operations
        delta_H_array = row['C0'] * (T_array - 298.15) + 0.5 * row['C1'] * (
                T_array ** 2 - 298.15 ** 2
        ) + (1 / 3) * row['C2'] * (T_array ** 3 - 298.15 ** 3)

        # Calculate the total enthalpy by adding H_ref
        H_array = delta_H_array  + H_ref 

        # Convert to Pandas Series
        enthalpy_values_J_mol = pd.Series(H_array, index=T)

        # Convert enthalpy values from J/mol to kJ/kg and store in the DataFrame
        enthalpy_df[row['Ionic liquid']] = enthalpy_values_J_mol 

        # Convert Cp parameters from J/mol/K to kJ/mol/K
        df_updated.loc[index, ['C0', 'C1', 'C2']] /= 1000

    return df_updated[['Ionic liquid', 'C0', 'C1', 'C2']], enthalpy_df /1000

# Call the function with the CSV file path
cp_result_df, enthalpy_result_df = calculate_enthalpy_from_csv('IL_Cp_with_Molar_Mass.csv')

# Print the results
print("Cp in kJ/(mol*K)")
print(cp_result_df.head().to_markdown(index=False, numalign="left", stralign="left"))

print("\nenthalpy in kJ/mol")
print(enthalpy_result_df.head().to_markdown(numalign="left", stralign="left"))
