import mpmath as mp
import numpy as np
import matplotlib.pyplot as plt
import time

# Set high precision
mp.mp.dps = 100
print(f"Using mpmath precision: {mp.mp.dps} decimal places")

def compute_zeros_up_to_T(T):
    """Compute zeta zeros with imaginary part < T"""
    zeros = []
    n = 1
    start_time = time.time()
    while True:
        try:
            g = mp.zetazero(n).imag
        except Exception as e:
            print(f"Error computing zero {n}: {e}")
            break
        if g > T:
            break
        zeros.append(mp.mpc(0.5, g))
        zeros.append(mp.mpc(0.5, -g))
        n += 1
    end_time = time.time()
    print(f"Computed {len(zeros)//2} zero pairs (imaginary part < {T}) in {end_time-start_time:.2f}s")
    return zeros

def chi_minus4(n):
    if n % 2 == 0:
        return 0
    elif n % 4 == 1:
        return 1
    elif n % 4 == 3:
        return -1
    else:
        return 0

def L_chi_minus4(t):
    N = int(np.sqrt(2 * abs(t) / np.pi))
    if N < 1:
        N = 1
    sum1 = mp.mpc(0,0)
    sum2 = mp.mpc(0,0)
    for n in range(1, N+1):
        chi = chi_minus4(n)
        if chi == 0:
            continue
        term1 = chi * (n ** (-0.5 - 1j * t))
        term2 = chi * (n ** (-0.5 + 1j * t))
        sum1 += term1
        sum2 += term2
    epsilon = -1j
    factor = (4 / (2 * np.pi)) ** (-0.5 + 1j * t)
    return sum1 + epsilon * factor * sum2

def theta_chi_minus4(t):
    return - (t/2) * mp.log(mp.pi/4) + mp.im(mp.loggamma(mp.mpc(0.75, 0.5*t)))

def Z_chi_minus4(t):
    return mp.e**(1j * theta_chi_minus4(t)) * L_chi_minus4(t)

def find_zeros(func, t_start, t_end, step=0.1):
    zeros = []
    t_prev = t_start
    f_prev = func(t_prev)
    for t in np.arange(t_start + step, t_end + step, step):
        f_curr = func(t)
        if np.real(f_prev) * np.real(f_curr) <= 0:
            t_zero = t_prev - (t - t_prev) * np.real(f_prev) / (np.real(f_curr) - np.real(f_prev))
            zeros.append(t_zero)
        t_prev = t
        f_prev = f_curr
    return zeros

def zeta_Z(t):
    theta = mp.im(mp.loggamma(mp.mpc(0.25, 0.5*t))) - (t/2)*mp.log(mp.pi)
    return mp.e**(1j * theta) * mp.zeta(0.5 + 1j*t)

# Precompute zeros for zeta
print("Computing zeta zeros...")
T_eigen = 500  # same as before
zeros = compute_zeros_up_to_T(T_eigen)
gamma_vals = sorted([float(abs(z.imag)) for z in zeros if z.imag > 0])  # Positive gammas
print(f"Using {len(gamma_vals)} positive zeros for eigenvector analysis")

# Build F matrix and compute F*F (F^H F)
def build_F_and_FtF(zeros_gamma, M=20):
    """Build F matrix and compute F*F."""
    N = len(zeros_gamma)
    # Test x values: log-spaced from 10^1 to 10^3
    x_vals = [10**i for i in np.linspace(1.0, 3.0, M)]
    F = np.zeros((M, N), dtype=complex)
    for k, x in enumerate(x_vals):
        for n, gamma in enumerate(zeros_gamma):
            rho = mp.mpc(0.5, gamma)
            x_rho = x ** rho
            F[k, n] = -x_rho / rho
    # Compute F*F = F^H F
    FtF = F.conj().T @ F
    return F, FtF, x_vals, zeros_gamma

def analyze_eigenvectors(FtF, label, zeros):
    """Analyze eigenvectors of F*F."""
    # Eigenvalues and eigenvectors
    evals, evecs = np.linalg.eig(FtF)
    # Sort by eigenvalue (descending)
    idx = np.argsort(np.real(evals))[::-1]
    evals = evals[idx]
    evecs = evecs[:, idx]

    # Take real part for plotting (imaginary should be small)
    evals_real = np.real(evals)
    evecs_real = np.real(evecs)

    # Participation ratio
    trace = np.trace(np.real(FtF))
    trace_sq = np.trace(np.real(FtF) @ np.real(FtF))
    pr = (trace * trace) / trace_sq if trace_sq > 0 else 0

    # Plot eigenvalues
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 3, 1)
    plt.semilogy(evals_real, 'bo-')
    plt.xlabel('Eigenvalue index')
    plt.ylabel('Eigenvalue (log scale)')
    plt.title(f'Eigenvalues of F*F ({label})')
    plt.grid(True, alpha=0.3)

    # Plot first few eigenvectors
    plt.subplot(1, 3, 2)
    for i in range(min(5, len(zeros))):
        plt.plot(evecs_real[:, i], label=f'Mode {i+1}')
    plt.xlabel('Zero index')
    plt.ylabel('Eigenvector component')
    plt.title(f'First 5 Eigenvectors ({label})')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Plot last few eigenvectors
    plt.subplot(1, 3, 3)
    for i in range(max(0, len(zeros)-5), len(zeros)):
        plt.plot(evecs_real[:, i], label=f'Mode {i+1}')
    plt.xlabel('Zero index')
    plt.ylabel('Eigenvector component')
    plt.title(f'Last 5 Eigenvectors ({label})')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.suptitle(f'Eigenvector Analysis of F*F for {label} (dps=100)', fontsize=14)
    label_safe = label.lower().replace("(", "").replace(")", "").replace(" ", "_")
    plt.savefig(f'eigenvector_{label_safe}_rh.png', dpi=150)
    plt.close()

    # Also plot eigenvectors against zero index to see if they look sinusoidal
    plt.figure(figsize=(10, 6))
    # Use the zero values as x-axis
    zero_vals = np.array(zeros)
    for i in range(min(3, len(zeros))):
        plt.plot(zero_vals, evecs_real[:, i], 'o-', label=f'Eigenvector {i+1} (eval={evals_real[i]:.2f})')
    plt.xlabel('Zero value γ_n')
    plt.ylabel('Eigenvector component')
    plt.title(f'Eigenvectors vs. Zero Values ({label})')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    label_safe2 = label.lower().replace("(", "").replace(")", "").replace(" ", "_")
    plt.savefig(f'eigenvector_vs_zero_{label_safe2}_rh.png', dpi=150)
    plt.close()

    return {
        'evals': evals,
        'evecs': evecs,
        'evals_real': evals_real,
        'evecs_real': evecs_real,
        'pr': pr,
        'zeros': zeros
    }

# Analyze for zeta
print("\nAnalyzing zeta eigenvectors...")
# Use first 30 zeros for F matrix (to keep size manageable)
N_use = min(30, len(gamma_vals))
F_zeta, FtF_zeta, x_zeta, zeta_zeros = build_F_and_FtF(gamma_vals[:N_use], M=15)
zeta_eigen = analyze_eigenvectors(FtF_zeta, "Zeta", zeta_zeros)

print(f"Zeta: Participation ratio = {zeta_eigen['pr']:.2f}")
print(f"Largest eigenvalue: {np.real(zeta_eigen['evals'][0]):.2f}")
print(f"Smallest eigenvalue: {np.real(zeta_eigen['evals'][-1]):.2f}")
print(f"Condition number: {np.real(zeta_eigen['evals'][0])/np.real(zeta_eigen['evals'][-1]):.2f}")

# Also analyze for a few different x ranges to see how eigenvectors change
print("\nAnalyzing eigenvector stability with different x ranges...")
x_ranges = [
    (1.0, 2.0),   # low x
    (1.0, 3.0),   # medium (our standard)
    (2.0, 4.0),   # high x
]

participation_ratios = []
for i, (x_min, x_max) in enumerate(x_ranges):
    x_vals = [10**j for j in np.linspace(np.log10(x_min), np.log10(x_max), 10)]
    F = np.zeros((len(x_vals), len(zeta_zeros)), dtype=complex)
    for k, x in enumerate(x_vals):
        for n, gamma in enumerate(zeta_zeros):
            rho = mp.mpc(0.5, gamma)
            x_rho = x ** rho
            F[k, n] = -x_rho / rho
    FtF = F.conj().T @ F
    evals, evecs = np.linalg.eig(FtF)
    evals_real = np.real(evals)
    evecs_real = np.real(evecs)

    # Calculate participation ratio for this x range
    trace = np.trace(np.real(FtF))
    trace_sq = np.trace(np.real(FtF) @ np.real(FtF))
    pr = (trace * trace) / trace_sq if trace_sq > 0 else 0
    participation_ratios.append(pr)

    print(f"  x range 10^{x_min:.1f}-10^{x_max:.1f}: PR = {pr:.2f}")

    # Plot eigenvectors vs zero values for this range
    plt.figure(figsize=(10, 6))
    for j in range(min(3, len(zeta_zeros))):
        plt.plot(zeta_zeros, evecs_real[:, j], 'o-', label=f'Eigenvector {j+1}')
    plt.xlabel('Zero value γ_n')
    plt.ylabel('Eigenvector component')
    plt.title(f'Eigenvectors vs. Zero Values (x range: 10^{x_min:.1f} to 10^{x_max:.1f})')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'eigenvector_xrange_{i}_rh.png', dpi=150)
    plt.close()

# Plot participation ratios
plt.figure(figsize=(8, 6))
x_labels = [f'10^{x_min:.1f}-10^{x_max:.1f}' for x_min, x_max in x_ranges]
plt.bar(x_labels, participation_ratios)
plt.xlabel('x range')
plt.ylabel('Participation Ratio')
plt.title('Participation Ratio vs x Range (dps=100)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('participation_ratio_vs_xrange_rh.png', dpi=150)
plt.close()

print("\nEigenvector analysis complete. Plots saved.")