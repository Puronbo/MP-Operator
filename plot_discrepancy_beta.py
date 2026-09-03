import mpmath as mp
import numpy as np
import matplotlib.pyplot as plt

mp.mp.dps = 30

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
beta_vals = [0.5, 0.6, 0.7, 0.8, 0.9, 0.95]
x_vals = np.logspace(1, 6, 50)  # from 10^1 to 10^6

plt.figure(figsize=(10,6))
for beta in beta_vals:
    disc = discrepancy_offline(beta, gamma0, x_vals)
    plt.loglog(x_vals, disc, label=f'β={beta:.2f}')
plt.xlabel('x')
plt.ylabel('|S1 - S2|')
plt.title('Discrepancy from off-line zero quadruplet (γ = first zero)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('discrepancy_beta_plot.png', dpi=150)
print("Saved discrepancy_beta_plot.png")