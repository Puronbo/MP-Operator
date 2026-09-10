import mpmath as mp
import numpy as np
import matplotlib.pyplot as plt

mp.mp.dps = 30

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

def discrepancy_for_beta(beta, gamma_val, N_pairs=10):
    # Build zeros: first N_pairs of actual zeros (on critical line) plus off-line zero and its friends
    zeros = []
    # actual zeros (first N_pairs pairs)
    for n in range(1, N_pairs+1):
        g = mp.zetazero(n).imag
        zeros.append(mp.mpc(0.5, g))
        zeros.append(mp.mpc(0.5, -g))
    # off-line zero and its quadruplet
    rho_off = mp.mpc(beta, gamma_val)
    quad = [
        rho_off,
        mp.mpc(1-rho_off.real, -rho_off.imag),   # 1 - rho
        mp.mpc(rho_off.real, -rho_off.imag),     # conjugate
        mp.mpc(1-rho_off.real, rho_off.imag)     # 1 - conjugate rho
    ]
    zeros.extend(quad)
    return zeros

# Fix gamma to first zero's gamma
gamma0 = mp.zetazero(1).imag
print(f"Using gamma0 = {gamma0}")

beta_vals = [0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0]
x_vals = [10, 100, 1000, 10000, 100000]

print("Discrepancy |S1-S2| for various beta (off-line) and x")
print("beta\\x", end="")
for x in x_vals:
    print(f"\t{x:.0e}", end="")
print()
for beta in beta_vals:
    zeros = discrepancy_for_beta(beta, gamma0, N_pairs=10)
    S1, S2 = compute_sums(zeros, x_vals)
    diff = np.abs(S1 - S2)
    print(f"{beta:.2f}\t", end="")
    for d in diff:
        print(f"{float(d):.2e}\t", end="")
    print()
    # Also print number of zeros
    print(f"  Number of zeros total: {len(zeros)}")