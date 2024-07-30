import numpy as np
from scipy.optimize import brentq

class Refrigerant:
    def __init__(self, name):
        self.name = name
        self.params = self.get_params()

    def get_params(self):
        if self.name == 'Water':
            return {
                'Tc': 647.096,  # Critical temperature (K)
                'Pc': 22064,    # Critical pressure (kPa)
                'omega': 0.344  # Acentric factor
            }
        elif self.name == 'R134a':
            return {
                'Tc': 374.21,
                'Pc': 4059.4,
                'omega': 0.326
            }
        elif self.name == 'R1234yf':
            return {
                'Tc': 367.85,
                'Pc': 3381.5,
                'omega': 0.339
            }
        else:
            raise ValueError("Unsupported refrigerant")

    def alpha_function(self, T):
        Tc, omega = self.params['Tc'], self.params['omega']
        Tr = T / Tc
        k = 0.37464 + 1.54226 * omega - 0.26992 * omega**2
        return (1 + k * (1 - np.sqrt(Tr)))**2

    def PengRobinson(self, T, P):
        Tc, Pc = self.params['Tc'], self.params['Pc']
        R = 8.31446261815324  # Universal gas constant in J/(mol·K)

        a = 0.45724 * R**2 * Tc**2 / Pc
        b = 0.07780 * R * Tc / Pc
        
        alpha = self.alpha_function(T)
        
        A = alpha * a * P / (R * T)**2
        B = b * P / (R * T)

        coeffs = [1, B - 1, A - 3*B**2 - 2*B, -A*B + B**2 + B**3]
        roots = np.roots(coeffs)
        real_roots = roots[np.isreal(roots)].real
        
        if len(real_roots) < 2:
            raise ValueError(f"Less than 2 real roots found for T={T}, P={P}")

        Z_vapor = np.max(real_roots)
        Z_liquid = np.min(real_roots)

        return Z_vapor, Z_liquid, A, B

    def fugacity_coefficient(self, Z, A, B):
        return np.exp(Z - 1 - np.log(Z - B) - A / (2 * np.sqrt(2) * B) * np.log((Z + (1 + np.sqrt(2)) * B) / (Z + (1 - np.sqrt(2)) * B)))

    def saturation_temperature(self, P):
        def equation(T):
            try:
                Z_vapor, Z_liquid, A, B = self.PengRobinson(T, P)
                f_vapor = self.fugacity_coefficient(Z_vapor, A, B)
                f_liquid = self.fugacity_coefficient(Z_liquid, A, B)
                result = f_vapor - f_liquid
                #print(f"Debug: T={T:.2f}, f_vapor={f_vapor:.6e}, f_liquid={f_liquid:.6e}, diff={result:.6e}")
                return result
            except ValueError as e:
                print(f"Error in equation: {e}")
                return np.nan

        Tc, Pc = self.params['Tc'], self.params['Pc']
        T_low = max(0.2 * Tc, 200)  # Lower bound: 20% of critical temp or 200K, whichever is higher
        T_high = min(0.9 * Tc, Tc - 10)  # Upper bound: 99% of critical temp or just below Tc

        print(f"Searching for saturation temperature between {T_low:.2f}K and {T_high:.2f}K")

        # Check boundary conditions
        f_low = equation(T_low)
        f_high = equation(T_high)
        if np.isnan(f_low) or np.isnan(f_high) or f_low * f_high > 0:
            print(f"Unable to find saturation temperature for P = {P} kPa")
            return np.nan

        try:
            T_sat = brentq(equation, T_low, T_high, rtol=1e-6, maxiter=1000)
            return T_sat
        except ValueError as e:
            print(f"Error finding saturation temperature for P = {P} kPa: {e}")
            return np.nan

def print_results(refrigerant, pressures):
    print(f"\nResults for {refrigerant.name}:")
    for P in pressures:
        T_sat = refrigerant.saturation_temperature(P)
        if not np.isnan(T_sat):
            print(f"{refrigerant.name} at {P} kPa has a saturation temperature of {T_sat:.2f} K")
        else:
            print(f"Could not calculate saturation temperature for {refrigerant.name} at {P} kPa")
    print()

if __name__ == "__main__":
    pressures = [100, 150, 200, 250, 300]  # kPa

    water = Refrigerant('Water')
    print_results(water, pressures)

    r134a = Refrigerant('R134a')
    print_results(r134a, pressures)