import mpmath as mp
import numpy as np
import matplotlib.pyplot as plt

mp.mp.dps = 30  # set precision

def compute_sums(zeros, x_vals):
    """zeros: list of complex numbers (non-trivial zeros)
    x_vals: list of positive real numbers
    Returns S1, S2 arrays where
        S1[i] = sum over zeros of x^rho / rho
        S2[i] = sum over zeros of x^{1-rho} / (1-rho)
    """
    S1 = np.zeros(len(x_vals), dtype=complex)
    S2 = np.zeros(len(x_vals), dtype=complex)
    for rho in zeros:
        for i, x in enumerate(x_vals):
            term1 = x**rho / rho
            term2 = x**(1-rho) / (1-rho)
            S1[i] += term1
            S2[i] += term2
    return S1, S2

# Get first N zeros (positive gamma) using mpmath.zetazero
N = 5000  # number of zeros with positive imaginary part
print(f"Computing first {N} zeros of zeta(s)...")
gamma_vals = []
for n in range(1, N+1):
    g = mp.zetazero(n).imag
    gamma_vals.append(g)
# Build full zero list: each gamma gives rho = 0.5 + i*gamma and its conjugate
zeros = []
for g in gamma_vals:
    zeros.append(mp.mpc(0.5, g))
    zeros.append(mp.mpc(0.5, -g))
print(f"Total zeros in list: {len(zeros)}")

# Define x values to test
x_vals = [10**k for k in range(1, 6)]  # 10^1 to 10^5
print("x values:", x_vals)

# Compute sums for actual zeros
S1, S2 = compute_sums(zeros, x_vals)
diff = np.abs(S1 - S2)
print("\nDiscrepancy for actual zeros (should be small):")
for x, d in zip(x_vals, diff):
    print(f"  x = {x:.1e}: |S1 - S2| = {d:.2e}")

# Now inject an off-line zero and its required friends to see effect
# Choose an off-line zero: beta = 0.6, gamma = first gamma ~14.1347
beta_off = 0.6
gamma_off = gamma_vals[0]  # ~14.1347
rho_off = mp.mpc(beta_off, gamma_off)
# Its friends needed for the xi function to be entire? For sum test we just add this zero and its conjugate?
# But to maintain the set closed under rho -> 1-rho and conjugation, we should add the quadruplet:
# rho, 1-rho, conjugate rho, conjugate(1-rho)
zeros_injected = zeros.copy()
quad = [
    rho_off,
    mp.mpc(1-rho_off.real, -rho_off.imag),  # 1 - rho
    mp.mpc(rho_off.real, -rho_off.imag),    # conjugate
    mp.mpc(1-rho_off.real, rho_off.imag)    # 1 - conjugate rho
]
zeros_injected.extend(quad)
print(f"\nInjected off-line zero rho = {rho_off}")
print(f"Added its quadruplet, total zeros now: {len(zeros_injected)}")

# Compute sums with injected zeros
S1_inj, S2_inj = compute_sums(zeros_injected, x_vals)
diff_inj = np.abs(S1_inj - S2_inj)
print("\nDiscrepancy with injected off-line zero:")
for x, d in zip(x_vals, diff_inj):
    print(f"  x = {x:.1e}: |S1 - S2| = {d:.2e}")

# Plot
plt.figure(figsize=(10,6))
plt.semilogy(x_vals, diff, 'bo-', label='Actual zeros')
plt.semilogy(x_vals, diff_inj, 'rs--', label='With off-line zero')
plt.xlabel('x')
plt.ylabel('|S1 - S2|')
plt.title('Discrepancy between sums over zeros and over 1-rho')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('discrepancy_plot.png', dpi=150)
print("\nSaved discrepancy_plot.png")