import pandas as pd

# 加载比热系数数据
cp_data = pd.read_csv('IL_Cp.csv')
cp_data.set_index('Ionic liquid', inplace=True)

def calculate_specific_heat(ionic_liquid, temperature):
    """
    根据给定的离子液体名称和温度计算比热。

    Args:
    ionic_liquid (str): 离子液体的名称。
    temperature (float): 温度，单位为K。

    Returns:
    float: 比热，单位为 J/(mol*K)。
    """
    if ionic_liquid in cp_data.index:
        # 获取相应的系数
        C0 = cp_data.loc[ionic_liquid, 'C0']
        C1 = cp_data.loc[ionic_liquid, 'C1']
        C2 = cp_data.loc[ionic_liquid, 'C2']
        
        # 计算比热
        specific_heat = C0 + C1 * temperature + C2 * temperature**2
        return specific_heat
    else:
        raise ValueError("Ionic liquid not found in the database.")

# 示例使用
ionic_liquid = '[hmim][Tf2N]'
temperature = 298.15  # K
cp = calculate_specific_heat(ionic_liquid, temperature)
print(f"The specific heat of {ionic_liquid} at {temperature} K is {cp} J/(mol*K)")
