import mpmath as mp
import numpy as np
import matplotlib.pyplot as plt

mp.mp.dps = 30

def term_offline(rho, x):
    # rho is complex
    return x**rho / rho - x**(1-rho) / (1-rho)

def discrepancy_offline(beta, gamma_val, x_vals):
    rho = mp.mpc(beta, gamma_val)
    quad = [
        rho,
        mp.mpc(1-rho.real, -rho.imag),   # 1 - rho
        mp.mpc(rho.real, -rho.imag),     # conjugate
        mp.mpc(1-rho.real, rho.imag)     # 1 - conjugate rho
    ]
    S1 = np.zeros(len(x_vals), dtype=complex)
    S2 = np.zeros(len(x_vals), dtype=complex)
    for r in quad:
        for i, x in enumerate(x_vals):
            term = x**r / r
            S1[i] += term
            term2 = x**(1-r) / (1-r)
            S2[i] += term2
    return np.abs(S1 - S2)

gamma0 = mp.zetazero(1).imag
print(f"gamma0 = {gamma0}")

beta_vals = [0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0]
x_vals = [10, 100, 1000, 10000, 100000]

print("Discrepancy from off-line quadruplet only:")
print("beta\\x", end="")
for x in x_vals:
    print(f"\t{x:.0e}", end="")
print()
for beta in beta_vals:
    diff = discrepancy_offline(beta, gamma0, x_vals)
    print(f"{beta:.2f}\t", end="")
    for d in diff:
        print(f"{float(d):.2e}\t", end="")
    print()