import pandas as pd
# Define the function to calculate enthalpy of an ionic liquid at a given temperature
def enthalpy_IL(ionic_liquid, temperature, file_path='IL_Cp_with_Molar_Mass.csv'):
    """
    Calculates the enthalpy of an ionic liquid at a given temperature.

    Args:
        ionic_liquid (str): The name of the ionic liquid.
        temperature (float): The temperature in Celsius.
        file_path (str, optional): The path to the CSV file containing ionic liquid data. Defaults to 'IL_Cp_with_Molar_Mass.csv'.

    Returns:
        float: The enthalpy of the ionic liquid in kJ/kg.

    Raises:
        ValueError: If the ionic liquid is not found in the database or the molar mass is not available.
    """
    # Read the CSV file
    df_updated = pd.read_csv(file_path)

    # Filter the DataFrame to the row where the `Ionic liquid` column matches the input `ionic_liquid`
    filtered_row = df_updated[df_updated['Ionic liquid'] == ionic_liquid]
    if filtered_row.empty:
        raise ValueError(f"Ionic liquid '{ionic_liquid}' not found in the database.")

    # Get the molar mass from the `Molar Mass (g/mol)` column of `filtered_row`
    molar_mass_str = filtered_row['Molar Mass (g/mol)'].values[0]
    if molar_mass_str == 'NA':
        raise ValueError(f"Molar mass for '{ionic_liquid}' is not available.")

    # Convert the `Molar Mass (g/mol)` from a string to a float
    molar_mass = float(molar_mass_str)

    # Convert temperature from Celsius to Kelvin
    temperature = temperature + 273.15

    # Convert H_ref from kJ/kg to J/mol
    H_ref = 200 * molar_mass

    # Calculate the enthalpy
    enthalpy_J_mol =filtered_row['C0'] * (temperature - 298.15) + 0.5 * filtered_row['C1'] * (
                temperature ** 2 - 298.15 ** 2
        ) + (1 / 3) * filtered_row['C2'] * (temperature ** 3 - 298.15 ** 3)
    
    # Convert enthalpy from J/mol to kJ/kg
    enthalpy_kJ_kg = enthalpy_J_mol / 1000 / (molar_mass / 1000)

    return enthalpy_kJ_kg

# Call the function with the ionic liquid name and temperature
enthalpy = enthalpy_IL('[hmim][Tf2N]', 100)

# Print the result
print("The enthalpy of [hmim][Tf2N] at 298.15 Celsius is:", enthalpy, "kJ/kg")
