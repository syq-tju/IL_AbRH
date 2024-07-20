import os, numpy as np
from ctREFPROP.ctREFPROP import REFPROPFunctionLibrary

def NBP():
    RP = REFPROPFunctionLibrary(os.environ['RPPREFIX'])
    print(RP.RPVersion())
    RP.SETPATHdll(os.environ['RPPREFIX'])
    r = RP.SETUPdll(1,"PROPANE.FLD","HMX.BNC","DEF")
    assert(r.ierr == 0)
    print(RP.PQFLSHdll(101.325, 0, [1.0], 0))

if __name__=='__main__':
    # Print the version of REFPROP in use and the NBP
    NBP()