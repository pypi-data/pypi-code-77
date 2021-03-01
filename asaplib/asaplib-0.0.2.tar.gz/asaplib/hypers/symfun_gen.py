#!/usr/bin/python
import sys
import argparse
import numpy as np
from asaplib.hypers.univeral_length_scales import uni_length_scales, system_pair_bond_lengths

"""
Automatically generate the hyperparameters of ACSF descriptors for arbitrary elements and combinations.

## Example
The command
gen_universal_soap_hypers.py --Zs 1

generates ACSF for hydrogen
"""

def main(Zs, scalerange, sharpness):

    """
    scalerange: type=float, scale the cutoffs of the SFs.
    sharpness: type=float, sharpness factor for atom_width, default=1.0, 
                larger sharpness means more resolution, and more SFs will be generated.
    rmin: type=float, distance in Angstrom to the first nearest neighbor. 
         Eliminates the symmetry functions that investigate the space between 0 and rmin.
    """
    for Z in Zs:
        if str(Z) not in uni_length_scales:
            raise RuntimeError("key Z {} not present in length_scales table".format(Z))

    shortest_bond, longest_bond = system_pair_bond_lengths(Zs, uni_length_scales)
    cutoff = longest_bond * 1.56 * float(scalerange)
    rmin = shortest_bond
    N = min(int(sharpness*(cutoff-rmin)/0.5), 5)

    index = np.arange(N+1, dtype=float)
    shift_array = cutoff*(1./N)**(index/(len(index)-1)) 
    eta_array = 1./shift_array**2.

    for fel in Zs:
        for sel in Zs:
            print("# symfunctions for type %s 2 %s" %(fel, sel))
            for eta in eta_array:
                if 3*np.sqrt(1/eta) > rmin:
                    print("symfunction_short %s 2 %s %.4f 0.000 %.3f" %(fel, sel, eta, cutoff))
            for i in range(len(shift_array)-1):
                eta = 1./((shift_array[N-i] - shift_array[N-i-1])**2)
                if shift_array[N-i] + 3*np.sqrt(1/eta) > rmin:
                    print("symfunction_short %s 2 %s %.4f %.3f %.3f" %(fel, sel, eta, shift_array[N-i], cutoff))

    eta_array = np.logspace(-3,0,N//2)
    zeta_array = [1.000, 4.000, 16.000]
    for fel in Zs:
        ang_Zs = list(Zs)
        for sel in Zs:
            for tel in ang_Zs:
                print("# symfunctions for type %s 3 %s %s" %(fel, sel, tel))
                for eta in eta_array:
                    for zeta in zeta_array:
                        if 3*np.sqrt(1/eta) > rmin:
                            print("symfunction_short %s 3 %s %s %.4f  1.000 %.3f %.3f" %(fel, sel, tel, eta, zeta, cutoff))
                            print("symfunction_short %s 3 %s %s %.4f -1.000 %.3f %.3f" %(fel, sel, tel, eta, zeta, cutoff))
            ang_Zs.pop(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument("--Zs", nargs="+", type=int, help="atomic numbers to calculate descriptors for", required=True)
    parser.add_argument('-sr', '--scalerange', type = float, default = 1.0, help = 'Scale the length scales.')
    parser.add_argument('-s', '--sharpness', type = float, default = 1.0, help = 'larger means more ACSFs will be selected.')
    args = parser.parse_args()
    main(args.Zs, args.scalerange, args.sharpness)
