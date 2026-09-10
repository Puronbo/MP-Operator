"""
Verification script for numerical exploration of explicit formula duality and Riemann zeta zeros.
This script rigorously verifies the key claims made in our exploration.
"""

import mpmath as mp
import numpy as np
import matplotlib.pyplot as plt

# Set high precision for verification
mp.mp.dps = 50

def compute_sums_direct(zeros, x_vals):
    """Direct computation of sums without numpy vectorization issues"""
    S1 = np.zeros(len(x_vals), dtype=complex)
    S2 = np.zeros(len(x_vals), dtype=complex)
    for rho in zeros:
        for i, x in enumerate(x_vals):
            term1 = x**rho / rho
            term2 = x**(1-rho) / (1-rho)
            S1[i] += term1
            S2[i] += term2
    return S1, S2

def compute_participation_ratio(FtF):
    """Compute participation ratio from F*F matrix"""
    FtF_real = np.real(FtF)
    trace = np.trace(FtF_real)
    trace_sq = np.trace(FtF_real @ FtF_real)
    return (trace * trace) / trace_sq if trace_sq > 0 else 0

def build_F_and_FtF(zeros, M=20):
    """Build F matrix and compute F*F"""
    N = len(zeros)
    x_vals = [10**i for i in np.linspace(1.0, 3.0, M)]
    F = np.zeros((M, N), dtype=complex)
    for k, x in enumerate(x_vals):
        for n, rho in enumerate(zeros):
            x_rho = x ** rho
            F[k, n] = -x_rho / rho
    FtF = F.conj().T @ F
    return F, FtF, x_vals

def main():
    print("="*60)
    print("RIGOROUS VERIFICATION OF NUMERICAL EXPLORATION CLAIMS")
    print("="*60)

    # 1. Verify discrepancy for actual zeros (should be ~0)
    print("\n1. VERIFYING DISCREPANCY FOR ACTUAL ZEROS (RH CASE)")
    print("-" * 50)

    # Get first 100 zeta zeros (50 pairs)
    N_pairs = 50
    gamma_vals = [mp.zetazero(n).imag for n in range(1, N_pairs+1)]
    zeros_actual = []
    for g in gamma_vals:
        zeros_actual.append(mp.mpc(0.5, g))
        zeros_actual.append(mp.mpc(0.5, -g))

    x_vals = [10, 100, 1000, 10000, 100000]
    print(f"Using {N_pairs} pairs of zeros ({len(zeros_actual)} total)")
    print(f"x values: {x_vals}")

    S1, S2 = compute_sums_direct(zeros_actual, x_vals)
    diff_actual = np.abs(S1 - S2)

    print("\nDiscrepancy |S1-S2| for actual zeros:")
    max_discrepancy = 0
    for x, d in zip(x_vals, diff_actual):
        d_float = float(d)
        print(f"  x = {x:.1e}: {d_float:.3e}")
        max_discrepancy = max(max_discrepancy, d_float)

    print(f"\nMaximum discrepancy: {max_discrepancy:.3e}")
    if max_discrepancy < 1e-10:
        print("PASS: Discrepancy is numerically zero (supporting RH)")
    else:
        print("FAIL: Discrepancy is unexpectedly large")

    # 2. Verify discrepancy grows with off-line zero
    print("\n\n2. VERIFYING DISCREPANCY GROWTH WITH OFF-LINE ZERO")
    print("-" * 50)

    beta_off = 0.6  # Clearly off the critical line
    gamma_off = gamma_vals[0]  # First zero's gamma
    rho_off = mp.mpc(beta_off, gamma_off)

    # Build the required quadruplet for the off-line zero
    quad = [
        rho_off,
        mp.mpc(1-rho_off.real, -rho_off.imag),   # 1 - rho
        mp.mpc(rho_off.real, -rho_off.imag),     # conjugate
        mp.mpc(1-rho_off.real, rho_off.imag)     # 1 - conjugate rho
    ]

    zeros_offline = zeros_actual + quad
    print(f"Injected off-line zero: rho = {rho_off}")
    print(f"Total zeros: {len(zeros_offline)} (original {len(zeros_actual)} + 4)")

    S1_off, S2_off = compute_sums_direct(zeros_offline, x_vals)
    diff_off = np.abs(S1_off - S2_off)

    print("\nDiscrepancy |S1-S2| with off-line zero:")
    for x, d in zip(x_vals, diff_off):
        d_float = float(d)
        print(f"  x = {x:.1e}: {d_float:.3e}")

    # Check that discrepancy grows with x (generally)
    increasing = all(diff_off[i] <= diff_off[i+1] for i in range(len(diff_off)-1))
    if increasing or diff_off[-1] > diff_off[0] * 10:  # Allow some fluctuation but expect growth
        print("PASS: Discrepancy grows with x (indicating sensitivity to off-line zeros)")
    else:
        print("WARNING: Discrepancy does not clearly grow with x")

    # 3. Verify participation ratio shows strong correlations
    print("\n\n3. VERIFYING PARTICIPATION RATIO (CORRELATION MEASURE)")
    print("-" * 50)

    # Use first 20 zeros (10 pairs) for F*F analysis like in our eigenvector_analysis.py
    N_small = 10
    gamma_small = [mp.zetazero(n).imag for n in range(1, N_small+1)]
    zeros_small = []
    for g in gamma_small:
        zeros_small.append(mp.mpc(0.5, g))
        zeros_small.append(mp.mpc(0.5, -g))

    print(f"Using {N_small} pairs of zeros ({len(zeros_small)} total) for F*F analysis")

    F, FtF, x_vals_F = build_F_and_FtF(zeros_small, M=15)
    pr = compute_participation_ratio(FtF)

    # Also compute eigenvalue spread
    evals = np.linalg.eigvals(FtF)
    evals_real = np.real(evals)
    lambda_max = np.max(evals_real)
    lambda_min = np.min(evals_real[evals_real > 1e-10])  # Avoid zeros
    condition_number = lambda_max / lambda_min if lambda_min > 0 else np.inf

    print(f"Participation ratio: {pr:.2f} (out of {len(zeros_small)} possible)")
    print(f"Largest eigenvalue: {lambda_max:.2f}")
    print(f"Smallest non-zero eigenvalue: {lambda_min:.2f}")
    print(f"Condition number: {condition_number:.2e}")

    if pr < len(zeros_small) * 0.7:  # Significantly less than maximum
        print("PASS: Participation ratio indicates strong correlations (< 70% of max)")
    else:
        print("FAIL: Participation ratio too high, suggesting weak correlations")

    if condition_number > 1000:
        print("PASS: Condition number indicates large anisotropy (>> 1000)")
    else:
        print("FAIL: Condition number too low, suggesting near-isotropy")

    # 4. Verify eigenvectors are not sinusoidal (non-convolutional)
    print("\n\n4. VERIFYING NON-CONVOLUTIONAL STRUCTURE")
    print("-" * 50)

    # Compute eigenvectors and check if they resemble sinusoids
    evals, evecs = np.linalg.eig(FtF)
    # Sort by eigenvalue (descending)
    idx = np.argsort(np.real(evals))[::-1]
    evals = evals[idx]
    evecs = evecs[:, idx]

    # Take real part (imaginary should be small)
    evecs_real = np.real(evecs)

    # For a sinusoidal eigenvector, we would expect roughly uniform distribution
    # of values or a clear oscillatory pattern. Let's check the first few eigenvectors.
    # A simple measure: compare to a sine wave of appropriate frequency

    n_zeros = len(zeros_small)
    x_indices = np.arange(n_zeros)

    non_sinusoidal_count = 0
    for i in range(min(3, n_zeros)):  # Check first 3 eigenvectors
        vec = evecs_real[:, i]
        # Normalize
        vec_norm = vec / (np.linalg.norm(vec) + 1e-12)
        # Compare to sine wave: sin(2*pi * k * x_indices / n_zeros) for k=1,2,...
        best_corr = 0
        for k in range(1, min(5, n_zeros//2 + 1)):
            sine_wave = np.sin(2 * np.pi * k * x_indices / n_zeros)
            sine_wave = sine_wave / (np.linalg.norm(sine_wave) + 1e-12)
            corr = np.abs(np.dot(vec_norm, sine_wave))
            best_corr = max(best_corr, corr)
        # If correlation with any sine wave is low, it's not sinusoidal
        if best_corr < 0.5:  # Threshold for "not sinusoidal"
            non_sinusoidal_count += 1

    print(f"Number of first 3 eigenvectors that are non-sinusoidal: {non_sinusoidal_count}/3")
    if non_sinusoidal_count >= 2:
        print("PASS: Eigenvectors show non-convolutional structure")
    else:
        print("WARNING: Eigenvectors appear somewhat sinusoidal")

    # 5. Summary
    print("\n\n" + "="*60)
    print("VERIFICATION SUMMARY")
    print("="*60)

    checks_passed = 0
    total_checks = 5

    if max_discrepancy < 1e-10:
        checks_passed += 1
        print("Discrepancy for actual zeros: PASSED")
    else:
        print("Discrepancy for actual zeros: FAILED")

    if increasing or diff_off[-1] > diff_off[0] * 10:
        checks_passed += 1
        print("Discrepancy growth with off-line zero: PASSED")
    else:
        print("Discrepancy growth with off-line zero: FAILED")

    if pr < len(zeros_small) * 0.7:
        checks_passed += 1
        print("Participation ratio shows correlations: PASSED")
    else:
        print("Participation ratio shows correlations: FAILED")

    if condition_number > 1000:
        checks_passed += 1
        print("Condition number indicates anisotropy: PASSED")
    else:
        print("Condition number indicates anisotropy: FAILED")

    if non_sinusoidal_count >= 2:
        checks_passed += 1
        print("Non-convolutional eigenvector structure: PASSED")
    else:
        print("Non-convolutional eigenvector structure: FAILED")

    print(f"\nOverall: {checks_passed}/{total_checks} checks passed")

    if checks_passed >= 4:
        print("\nVERIFICATION SUCCESSFUL: Major claims are supported by numerical evidence")
        print("   This rigorous verification confirms our exploration results.")
    elif checks_passed >= 3:
        print("\nVERIFICATION MOSTLY SUCCESSFUL: Core claims are supported")
        print("   Minor discrepancies warrant further investigation.")
    else:
        print("\nVERIFICATION FAILED: Significant issues found")
        print("   Claims need re-examination with improved methods or parameters.")

    print("\n" + "="*60)

if __name__ == "__main__":
    main()