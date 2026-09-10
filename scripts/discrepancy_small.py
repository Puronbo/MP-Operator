import mpmath as mp
import numpy as np
import matplotlib.pyplot as plt

mp.mp.dps = 30

def compute_sums(zeros, x_vals):
    S1 = np.zeros_like(x_vals, dtype=complex)
    S2 = np.zeros_like(x_vals, dtype=complex)
    for rho in zeros:
        # Avoid division by zero (should not happen)
        # Use numpy vectorization
        x_arr = np.array(x_vals, dtype=object)  # object to allow mpmath power?
        # Better compute in loop
        pass
    # We'll do simple loops for clarity
    S1 = [0+0j]*len(x_vals)
    S2 = [0+0j]*len(x_vals)
    for rho in zeros:
        for i, x in enumerate(x_vals):
            term1 = x**rho / rho
            term2 = x**(1-rho) / (1-rho)
            S1[i] += term1
            S2[i] += term2
    return np.array(S1), np.array(S2)

# Get first N zeros
N = 500
print(f"Computing first {N} zeros...")
gamma_vals = [mp.zetazero(n).imag for n in range(1, N+1)]
zeros = []
for g in gamma_vals:
    zeros.append(mp.mpc(0.5, g))
    zeros.append(mp.mpc(0.5, -g))
print(f"Total zeros: {len(zeros)}")

x_vals = [10**k for k in range(1, 6)]  # 10 to 100000
print("x values:", x_vals)

S1, S2 = compute_sums(zeros, x_vals)
diff = np.abs(S1 - S2)
print("\nDiscrepancy actual zeros:")
for x, d in zip(x_vals, diff):
    print(f"  x={x:.1e}: {float(d):.2e}")

# Inject off-line zero
beta_off = 0.6
gamma_off = gamma_vals[0]
rho_off = mp.mpc(beta_off, gamma_off)
quad = [
    rho_off,
    mp.mpc(1-rho_off.real, -rho_off.imag),
    mp.mpc(rho_off.real, -rho_off.imag),
    mp.mpc(1-rho_off.real, rho_off.imag)
]
zeros_inj = zeros + quad
print(f"\nInjected rho={rho_off}")
S1_inj, S2_inj = compute_sums(zeros_inj, x_vals)
diff_inj = np.abs(S1_inj - S2_inj)
print("Discrepancy with injected:")
for x, d in zip(x_vals, diff_inj):
    print(f"  x={x:.1e}: {float(d):.2e}")

# Plot
plt.figure()
plt.semilogy(x_vals, diff, 'bo-', label='Actual')
plt.semilogy(x_vals, diff_inj, 'rs--', label='Injected')
plt.xlabel('x')
plt.ylabel('|S1-S2|')
plt.title('Discrepancy')
plt.legend()
plt.grid()
plt.savefig('discrepancy_small.png')
print("Saved plot")