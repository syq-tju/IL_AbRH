import pandas as pd

# Load the CSV file
file_path = 'NRTL_para2.csv'
nrtl_data = pd.read_csv(file_path)

# Display the first few rows to understand its structure
print(nrtl_data.head())


import numpy as np

def calculate_activity_coefficients(pair_name, x, T=298.15):
    # Find the row corresponding to the given pair name
    pair_data = nrtl_data[nrtl_data['Working pairs'] == pair_name].iloc[0]
    
    # Extract NRTL parameters
    tau_0_12 = pair_data['tau_0_12']
    tau_1_12 = pair_data['tau_1_12']
    tau_0_21 = pair_data['tau_0_21']
    tau_1_21 = pair_data['tau_1_21']
    alpha = pair_data['alpha']
    
    # Example compositions
    x1 = x
    x2 = 1 - x
    
    # Calculate tau12 and tau21
    tau12 = tau_0_12 + tau_1_12 / (T)
    tau21 = tau_0_21 + tau_1_21 / (T)    
    
    # Calculate G12 and G21
    G12 = np.exp(-alpha * tau12)
    G21 = np.exp(-alpha * tau21)

    
    # Calculate ln_gamma1 and ln_gamma2
    ln_gamma1 = x2**2 * (tau21 * (G21 / (x1 + x2 * G21))**2 + tau12 * G12 / ((x2 + x1 * G12)**2))
    ln_gamma2 = x1**2 * (tau12 * (G12 / (x2 + x1 * G12))**2 + tau21 * G21 / ((x1 + x2 * G21)**2))
    
    # Calculate gamma1 and gamma2
    gamma1 = np.exp(ln_gamma1)
    gamma2 = np.exp(ln_gamma2)
    
    return gamma1, gamma2

# Example usage
pair_name = 'H2O [dmim][DMP]'
x = 0.5
gamma1, gamma2 = calculate_activity_coefficients(pair_name, x)
print(gamma1, gamma2)
