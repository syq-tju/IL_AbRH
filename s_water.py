import os
from ctREFPROP.ctREFPROP import REFPROPFunctionLibrary

def initialize_refprop():
    """初始化 REFPROP 库并设置水作为工作流体"""
    RP = REFPROPFunctionLibrary(os.environ['RPPREFIX'])
    RP.SETPATHdll(os.environ['RPPREFIX'])

    r = RP.SETUPdll(1, "WATER.FLD", "HMX.BNC", "DEF")
    if r.ierr != 0:
        raise ValueError(f"Error setting up fluid: {r.herr}")
    return RP

def calculate_entropy_tp(RP, temperature, pressure):
    """计算给定温度和压力下的水的熵值"""
    result = RP.TPFLSHdll(temperature + 273.15, pressure, [1.0])
    if result.ierr != 0:
        raise ValueError(f"Error in TP flash calculation: {result.herr}")
    return result.s / 18.01528  # kJ/(kg·K)

def calculate_entropy_tx(RP, temperature, quality):
    """计算给定温度和干度下的水的熵值"""
    result = RP.TQFLSHdll(temperature + 273.15, quality, [1.0], 1)  # 添加 kq=1
    if result.ierr != 0:
        raise ValueError(f"Error in TQ flash calculation: {result.herr}")
    return result.s / 18.01528  # kJ/(kg·K)

def main():
    RP = initialize_refprop()

    # 1. 根据温度和压力计算熵值
    temperature = 50  # °C
    pressure = 101.325  # kPa
    entropy_tp = calculate_entropy_tp(RP, temperature, pressure)
    print(f"At T={temperature}°C and P={pressure} kPa:")
    print(f"  Entropy: {entropy_tp:.4f} kJ/(kg·K)")

    # 2. 根据温度和干度计算熵值
    temperature = 100  # °C
    quality = 0.5  # 50% 干度
    entropy_tx = calculate_entropy_tx(RP, temperature, quality)
    print(f"\nAt T={temperature}°C and quality={quality}:")
    print(f"  Entropy: {entropy_tx:.4f} kJ/(kg·K)")

if __name__ == '__main__':
    main()
