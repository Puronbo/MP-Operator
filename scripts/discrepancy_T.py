import mpmath as mp
import numpy as np
import matplotlib.pyplot as plt

mp.mp.dps = 50

def compute_sums(zeros, x_vals):
    S1 = np.zeros(len(x_vals), dtype=complex)
    S2 = np.zeros(len(x_vals), dtype=complex)
    for rho in zeros:
        for i, x in enumerate(x_vals):
            term1 = x**rho / rho
            term2 = x**(1-rho) / (1-rho)
            S1[i] += term1
            S2[i] += term2
    return S1, S2

def discrepancy_for_T(T):
    # compute first N zeros such that gamma < T
    zeros = []
    n = 1
    while True:
        g = mp.zetazero(n).imag
        if g > T:
            break
        zeros.append(mp.mpc(0.5, g))
        zeros.append(mp.mpc(0.5, -g))
        n += 1
    return zeros

x_vals = [10, 100, 1000, 10000]
T_vals = [10, 20, 50, 100, 200, 500]

print("Discrepancy |S1-S2| for various T (height of zeros) and x")
print("T\\x", end="")
for x in x_vals:
    print(f"\t{x:.0e}", end="")
print()
for T in T_vals:
    zeros = discrepancy_for_T(T)
    print(f"{T}\t", end="")
    S1, S2 = compute_sums(zeros, x_vals)
    diff = np.abs(S1 - S2)
    for d in diff:
        print(f"{float(d):.2e}\t", end="")
    print()
    print(f"  Number of zeros pairs: {len(zeros)//2}")