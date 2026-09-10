import mpmath as mp
import numpy as np
import matplotlib.pyplot as plt

mp.mp.dps = 30

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

# Precompute many zeros for both functions
print("Computing many zeros...")
# Zeta zeros up to height ~100 (first 30 zeros)
zeta_zeros_all = []
for n in range(1, 31):
    gamma = mp.zetazero(n).imag
    zeta_zeros_all.append(gamma)
    zeta_zeros_all.append(-gamma)
zeta_zeros_all = sorted(zeta_zeros_all)

# L(s, chi_{-4}) zeros via approximate method up to similar height
chi_zeros_raw = find_zeros(Z_chi_minus4, 0, 80, step=0.2)
refined = []
for z in chi_zeros_raw:
    refined.extend(find_zeros(Z_chi_minus4, z-0.5, z+0.5, step=0.01))
chi_zeros_all = []
for z in refined:
    if not any(abs(z - uz) < 0.1 for uz in chi_zeros_all):
        chi_zeros_all.append(z)
chi_zeros_all = sorted(chi_zeros_all)
# Keep both positive and negative (the find_zeros already gives both sides? Actually it gives positive t; we'll mirror)
chi_zeros_all = chi_zeros_all + [-z for z in chi_zeros_all]
chi_zeros_all = sorted(chi_zeros_all)

def participation_ratio(F):
    """Participation ratio = (trace)^2 / trace(F^2) for PSD matrix."""
    # F*F is PSD Hermitian
    FtF = F.conj().T @ F
    # Ensure real symmetric by taking real part (imag should be ~0)
    FtF_real = np.real(FtF)
    evals = np.linalg.eigvalsh(FtF_real)  # eigenvalues of real symmetric matrix
    # Participation ratio = (sum evals)^2 / sum(evals^2)
    sum_evals = np.sum(evals)
    sum_sq = np.sum(evals**2)
    if sum_sq == 0:
        return 0
    return (sum_evals * sum_evals) / sum_sq

def spectral_entropy(F):
    """Von Neumann entropy of the normalized density matrix rho = F*F / trace(F*F)."""
    FtF = F.conj().T @ F
    FtF_real = np.real(FtF)
    evals = np.linalg.eigvalsh(FtF_real)
    trace = np.sum(evals)
    if trace == 0:
        return 0
    probs = evals / trace
    # Remove zeros to avoid log(0)
    probs = probs[probs > 1e-12]
    return -np.sum(probs * np.log(probs))

def analyze(zeros_list, label, max_N=30):
    Ns = list(range(2, max_N+1, 2))  # use even numbers to keep symmetry
    prs = []
    ents = []
    for N in Ns:
        zeros = zeros_list[:N]
        # Build F with M test points (say M=12)
        M = 12
        x_vals = [10**i for i in np.linspace(1.0, 3.0, M)]
        F = np.zeros((M, N), dtype=complex)
        for k, x in enumerate(x_vals):
            for n, gamma in enumerate(zeros):
                rho = mp.mpc(0.5, gamma)
                x_rho = x ** rho
                F[k, n] = -x_rho / rho
        pr = participation_ratio(F)
        ent = spectral_entropy(F)
        prs.append(pr)
        ents.append(ent)
        if N % 6 == 0:
            print(f"{label}: N={N:2d}, PR={pr:.2f}, entropy={ent:.2f}")
    return Ns, prs, ents

print("\nComputing participation ratio and spectral entropy...")
Ns_zeta, prs_zeta, ents_zeta = analyze(zeta_zeros_all, "Zeta", max_N=28)
Ns_chi, prs_chi, ents_chi = analyze(chi_zeros_all, "L(s,chi_{-4})", max_N=28)

# Plot participation ratio
plt.figure(figsize=(12,5))
plt.subplot(1,2,1)
plt.plot(Ns_zeta, prs_zeta, 'bo-', label=r'$\zeta(s)$')
plt.plot(Ns_chi, prs_chi, 'rs--', label=r'$L(s,\chi_{-4})$')
plt.xlabel('Number of zero pairs N (using ±γ)')
plt.ylabel('Participation ratio')
plt.title('Participation ratio of F*F vs. number of zeros')
plt.legend()
plt.grid(True, alpha=0.3)

# Plot spectral entropy
plt.subplot(1,2,2)
plt.plot(Ns_zeta, ents_zeta, 'bo-', label=r'$\zeta(s)$')
plt.plot(Ns_chi, ents_chi, 'rs--', label=r'$L(s,\chi_{-4})$')
plt.xlabel('Number of zero pairs N (using ±γ)')
plt.ylabel('Spectral entropy (nats)')
plt.title('Spectral entropy of F*F vs. number of zeros')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('participation_ratio.png', dpi=150)
print("Saved participation_ratio.png")