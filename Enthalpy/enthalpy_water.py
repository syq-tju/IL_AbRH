import os
from ctREFPROP.ctREFPROP import REFPROPFunctionLibrary

def calculate_enthalpy(temperature, pressure):
    """
    计算给定温度和压力下的水的焓值。
    
    Args:
    temperature (float): 温度，单位为开尔文。
    pressure (float): 压力，单位为千帕（kPa）。

    Returns:
    float: 焓值，单位为焦耳每摩尔。
    """
    # 初始化REFPROP库
    RP = REFPROPFunctionLibrary(os.environ['RPPREFIX'])
    RP.SETPATHdll(os.environ['RPPREFIX'])
    
    # 设置流体文件
    r = RP.SETUPdll(1,"WATER.FLD","HMX.BNC","DEF")
    if r.ierr != 0:
        raise ValueError(f"Error setting up fluid: {r.herr}")
    
    # 使用温度和压力进行闪蒸计算
    result = RP.TPFLSHdll(temperature, pressure, [1.0])
    if result.ierr != 0:
        raise ValueError(f"Error in flash calculation: {result.herr}")
    
    # 返回焓值
    return result.h

if __name__ == '__main__':
    # 示例：计算温度为 300 K 和压力为 101.325 kPa 下的丙烷焓值
    temperature = 300  # K
    pressure = 101.325  # kPa
    enthalpy = calculate_enthalpy(temperature, pressure)
    print(f"Enthalpy at T={temperature} K and P={pressure} kPa is {enthalpy} J/mol")
