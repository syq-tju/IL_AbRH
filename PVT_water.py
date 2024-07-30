import numpy as np
from scipy.optimize import fsolve, root

class Refrigerant:
    def __init__(self, name):
        self.name = name
        self.params = self.get_params()

    def get_params(self):
        if self.name == 'Water':
            return {
                'Tc': 647.096,  # Critical temperature (K)
                'Pc': 22064,    # Critical pressure (kPa)
                'omega': 0.344 
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

    def alpha_function(self, T, Tc, omega):
        Tr = T / Tc
        m = 0.37464 + 1.54226 * omega - 0.26992 * omega**2
        alpha = (1 + m * (1 - Tr**0.5))**2
        if Tr > 1:
            alpha *= np.exp(m * (1 - Tr) * (1 + m * (1 - Tr**0.5)))
        return alpha

    def PengRobinson(self, T, P, s=0):
        Tc, Pc, omega = self.params['Tc'], self.params['Pc'], self.params['omega']
        R = 8.31446261815324

        Tr = T / Tc
        alpha = self.alpha_function(T, Tc, omega)
        a = 0.45724 * (R * Tc)**2 / Pc * alpha
        b = 0.07780 * R * Tc / Pc

        # Calculate A and B directly, without np.clip initially
        A = a * P / (R * T)**2  # Assign A here
        B = b * P / (R * T) - s  # Assign B here

        # Now clip A and B
        A = np.clip(A, -1e6, 1e6) 
        B = np.clip(B, -1e6, 1e6) 
        
        coeffs = [1.0, -1 + B, A - 3 * B**2 - 2 * B, -A * B + B**2 + B**3]
        
        # Use np.roots with try-except for error handling
        try:
            roots = np.roots(coeffs)
            real_roots = roots[np.isreal(roots)]
        except np.linalg.LinAlgError:
            # Handle cases where np.roots fails
            return 1, R * T / P, a, B  # Return Z=1 as a fallback

        if not real_roots.size:
            raise ValueError(f"No real roots found for T={T}, P={P}")

        Z = np.max(real_roots.real)
        V = Z * R * T / P
        return Z, V, a, B 

    def saturation_temperature(self, P):
        def equation(T, B):  # B is passed as an argument
            Z_vapor, V_vapor, _, _ = self.PengRobinson(T, P)
            Z_liquid, V_liquid, _, _ = self.PengRobinson(T, P, s=0.1)

            if Z_vapor - B <= 0 or Z_liquid - B <= 0:
                return np.inf

            fugacity_vapor = P * V_vapor * np.exp(Z_vapor - 1 - np.log(Z_vapor - B))
            fugacity_liquid = P * V_liquid * np.exp(Z_liquid - 1 - np.log(Z_liquid - B))
            return fugacity_vapor - fugacity_liquid

        # Antoine equation for initial guess
        A = 4.05544
        B = 1119.108
        C = -33.937
        T_guess = B / (A - np.log10(P)) - C

        # Calculate B for the initial guess
        _, _, _, B_guess = self.PengRobinson(T_guess, P)

        result = root(lambda T: equation(T, B_guess), T_guess, method='broyden1')
        T_sat = result.x.item()

        # Calculate B for the final T_sat
        _, _, _, B_sat = self.PengRobinson(T_sat, P)

        if equation(T_sat, B_sat) > 1e-6:  
            raise ValueError(f"Unable to find saturation temperature for P={P}")

        return T_sat
    
    # ... (rest of the code remains the same)


    def saturation_pressure(self, T):
        def equation(P):
            try:
                Z_vapor, _ = self.PengRobinson(T, P)
                Z_liquid, _ = self.PengRobinson(T, P)
                return Z_vapor - Z_liquid
            except ValueError:
                return np.inf  # 返回一个大数，表示这个压力不可行

        P_guess = self.params['Pc'] * 0.1
        P_sat = fsolve(equation, P_guess)[0]

        if equation(P_sat) > 1e-6:  # 检查是否真的找到了解
            raise ValueError(f"Unable to find saturation pressure for T={T}")

        return P_sat


if __name__ == "__main__":
    # 创建 R134a 制冷剂对象
    r134a = Refrigerant('R134a')

    # 计算 R134a 在 500 kPa 压力下的饱和温度
    P = 500  # kPa
    T_sat = r134a.saturation_temperature(P)
    print(f"R134a 在 {P} kPa 压力下的饱和温度为: {T_sat:.2f} K")

    # 计算 R134a 在 300 K 温度下的饱和压力
    T = 300  # K
    P_sat = r134a.saturation_pressure(T)
    print(f"R134a 在 {T} K 温度下的饱和压力为: {P_sat:.2f} kPa")