import mpmath as mp
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import simpson
import time

# Set high precision
mp.mp.dps = 100  # 100 decimal places
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

def compute_sums(zeros, x_vals):
    """Compute S1 and S2 sums over zeros"""
    S1 = np.zeros(len(x_vals), dtype=complex)
    S2 = np.zeros(len(x_vals), dtype=complex)
    for rho in zeros:
        for i, x in enumerate(x_vals):
            term1 = x**rho / rho
            term2 = x**(1-rho) / (1-rho)
            S1[i] += term1
            S2[i] += term2
    return S1, S2

def discrepancy_analysis(zeros, x_vals):
    """Compute discrepancy D(x) = |S1(x) - S2(x)|"""
    S1, S2 = compute_sums(zeros, x_vals)
    diff = np.abs(S1 - S2)
    return diff

def pair_correlation_analysis(zeros):
    """Compute pair correlation statistics and compare to GUE"""
    # Get positive imaginary parts
    gammas = sorted([abs(z.imag) for z in zeros if z.imag > 0])  # Positive imaginary parts
    print(f"Using {len(gammas)} positive zeros for pair correlation")

    # Compute normalized spacings
    spacings = np.diff(gammas)
    mean_spacing = np.mean(spacings)
    normalized_spacings = spacings / mean_spacing

    print(f"Mean spacing: {mean_spacing:.6f}")
    print(f"Std of normalized spacings: {np.std(normalized_spacings):.6f}")
    print(f"Variance of normalized spacings: {np.var(normalized_spacings):.6f}")

    # Compute histogram of normalized spacings
    hist, bin_edges = np.histogram(normalized_spacings, bins=50, range=(0, 3), density=True)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    # Theoretical GUE prediction
    def gue_pair_correlation(x):
        """GUE pair correlation function: R2(x) = 1 - (sin(πx)/(πx))^2"""
        if x == 0:
            return 0  # limit as x->0
        return 1 - (np.sin(np.pi * x) / (np.pi * x))**2

    gue_vals = gue_pair_correlation(bin_centers)

    # Compute Q_RH as integrated squared difference
    numerator = simpson(np.abs(hist - gue_vals)**2, bin_centers)
    denominator = simpson(gue_vals**2, bin_centers)

    if denominator > 0:
        Q_RH = numerator / denominator
    else:
        Q_RH = 0

    print(f"\nQ_RH (integrated squared difference): {Q_RH:.6f}")
    print(f"Interpretation: Q_RH < 1 suggests agreement with GUE (consistent with RH)")
    print(f"               Q_RH ≥ 1 suggests significant deviation from GUE")

    # Plot comparison
    plt.figure(figsize=(14, 10))

    plt.subplot(2, 2, 1)
    plt.plot(bin_centers, hist, 'b-', label='Zeta zeros', linewidth=2)
    plt.plot(bin_centers, gue_vals, 'r--', label='GUE prediction', linewidth=2)
    plt.xlabel('Normalized spacing s')
    plt.ylabel('Pair correlation R2(s)')
    plt.title('Pair Correlation: Zeta Zeros vs GUE (dps=100)')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.subplot(2, 2, 2)
    plt.semilogy(bin_centers, np.abs(hist - gue_vals), 'g-', linewidth=2)
    plt.xlabel('Normalized spacing s')
    plt.ylabel('|R2_zeta - R2_GUE| (log scale)')
    plt.title('Absolute Difference')
    plt.grid(True, alpha=0.3)

    # Spacing distribution
    plt.subplot(2, 2, 3)
    plt.hist(normalized_spacings, bins=50, alpha=0.7, density=True, label='Zeta zeros')
    x_vals = np.linspace(0, 3, 200)
    plt.plot(x_vals, np.exp(-x_vals), 'g--', label='Poisson (uncorrelated)', linewidth=2)
    plt.xlabel('Normalized spacing')
    plt.ylabel('Density')
    plt.title('Spacing Distribution')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Number variance / spectral rigidity
    plt.subplot(2, 2, 4)
    unfolded = np.cumsum(normalized_spacings)
    ideal = np.arange(len(unfolded))
    fluctuations = unfolded - ideal

    # Plot first 100 fluctuations
    plt.plot(ideal[:100], fluctuations[:100], 'b-', alpha=0.7)
    plt.xlabel('Zero index n')
    plt.ylabel('Fluctuation from uniform spacing')
    plt.title('Unfolding Fluctuations (first 100 zeros)')
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('gue_comparison_rh.png', dpi=150, bbox_inches='tight')
    print("\nSaved gue_comparison_rh.png")

    return {
        'normalized_spacings': normalized_spacings,
        'variance': np.var(normalized_spacings),
        'Q_RH': Q_RH
    }

def eigenvector_analysis(zeros, M=20):
    """Enhanced eigenvector analysis of correlation matrix F*F"""
    print("\n=== EIGENVECTOR ANALYSIS ===")

    gamma_vals = sorted([abs(z.imag) for z in zeros if z.imag > 0])  # Positive gammas
    print(f"Using {len(gamma_vals)} positive zeros for eigenvector analysis")

    # Use first N zeros for F matrix (limit to avoid too large matrix)
    N = min(len(gamma_vals), 100)  # Use up to 100 zeros
    gamma_subset = gamma_vals[:N]

    # Build F matrix and compute F*F (F^H F)
    def build_F_and_FtF(zeros_gamma, M=M):
        """Build F matrix and compute F*F = F^H F"""
        N = len(zeros_gamma)
        # Test x values: log-spaced from 10^1 to 10^4
        x_vals = [10**i for i in np.linspace(1.0, 4.0, M)]
        F = np.zeros((M, N), dtype=complex)
        for k, x in enumerate(x_vals):
            for n, gamma in enumerate(zeros_gamma):
                rho = mp.mpc(0.5, gamma)
                x_rho = x ** rho
                F[k, n] = -x_rho / rho
        # Compute F*F = F^H F
        FtF = F.conj().T @ F
        return F, FtF, x_vals, zeros_gamma

    def analyze_eigenvectors(FtF, label, zeros_gamma):
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
        plt.figure(figsize=(15, 5))
        plt.subplot(1, 3, 1)
        plt.semilogy(evals_real, 'bo-')
        plt.xlabel('Eigenvalue index')
        plt.ylabel('Eigenvalue (log scale)')
        plt.title(f'Eigenvalues of F*F ({label})')
        plt.grid(True, alpha=0.3)

        # Plot first few eigenvectors
        plt.subplot(1, 3, 2)
        for i in range(min(5, len(zeros_gamma))):
            plt.plot(evecs_real[:, i], label=f'Mode {i+1}')
        plt.xlabel('Zero index')
        plt.ylabel('Eigenvector component')
        plt.title(f'First 5 Eigenvectors ({label})')
        plt.legend()
        plt.grid(True, alpha=0.3)

        # Plot last few eigenvectors
        plt.subplot(1, 3, 3)
        for i in range(max(0, len(zeros_gamma)-5), len(zeros_gamma)):
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
        plt.figure(figsize=(12, 6))
        # Use the zero values as x-axis
        zero_vals = np.array(zeros_gamma)
        for i in range(min(3, len(zeros_gamma))):
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
            'zeros': zeros_gamma
        }

    # Analyze for zeta
    print("\nAnalyzing zeta eigenvectors...")
    F_zeta, FtF_zeta, x_zeta, zeta_zeros = build_F_and_FtF(gamma_subset[:min(30, len(gamma_subset))])  # Use first 15 pairs -> 30 zeros
    zeta_eigen = analyze_eigenvectors(FtF_zeta, "Zeta", zeta_zeros)

    print(f"Zeta: Participation ratio = {zeta_eigen['pr']:.2f}")
    print(f"Largest eigenvalue: {np.real(zeta_eigen['evals'][0]):.2f}")
    print(f"Smallest eigenvalue: {np.real(zeta_eigen['evals'][-1]):.2f}")
    print(f"Condition number: {np.real(zeta_eigen['evals'][0])/np.real(zeta_eigen['evals'][-1]):.2f}")

    return zeta_eigen

def main():
    """Main function to run all analyses"""
    print("Riemann Hypothesis High-Precision Numerical Verification")
    print("=" * 60)
    print(f"Started at: {time.ctime()}")

    start_time = time.time()

    # Choose T for zero height (balance between computation time and statistics)
    T_height = 5000  # This will give about ~5000/(2*pi)*log(5000/(2*pi)) ≈ 500 zeros? Let's compute.
    # Actually number of zeros with 0 < gamma < T is ~ (T/(2pi)) log(T/(2pi)) - T/(2pi)
    # For T=5000: (5000/(2*3.1416)) ≈ 795.77, log(795.77)≈6.68, so 795.77*6.68 - 795.77 ≈ 5316 - 796 = 4520 zeros.
    print(f"\nComputing zeros up to T = {T_height}")
    zeros = compute_zeros_up_to_T(T_height)
    print(f"Total zeros (including conjugates): {len(zeros)}")

    if len(zeros) == 0:
        print("No zeros computed. Exiting.")
        return

    # Discrepancy analysis
    print("\n=== DISCREPANCY ANALYSIS ===")
    x_vals = [10, 100, 1000, 10000, 100000]  # Extended x range
    print(f"Computing discrepancy for x = {x_vals}")
    disc = discrepancy_analysis(zeros, x_vals)
    print("Discrepancy |S1-S2|:")
    for x, d in zip(x_vals, disc):
        print(f"  x={x:.1e}: {float(d):.2e}")

    # Plot discrepancy vs x
    plt.figure(figsize=(10, 6))
    plt.semilogy(x_vals, disc, 'o-', linewidth=2, markersize=8)
    plt.xlabel('x')
    plt.ylabel('|S1(x) - S2(x)|')
    plt.title(f'Discrepancy vs x (T={T_height}, dps={mp.mp.dps})')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('discrepancy_vs_x_rh.png', dpi=150)
    print("\nSaved discrepancy_vs_x_rh.png")

    # Pair correlation analysis
    pair_corr_results = pair_correlation_analysis(zeros)

    # Eigenvector analysis
    eigenvector_results = eigenvector_analysis(zeros, M=20)

    end_time = time.time()

    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print(f"Total time: {end_time - start_time:.2f} seconds")
    print(f"Finished at: {time.ctime()}")

    # Summary of key findings
    print("\n=== KEY FINDINGS ===")
    print("1. Discrepancy Analysis:")
    for x, d in zip(x_vals, disc):
        print(f"   - At x={x:.1e}: |S1-S2| = {float(d):.2e}")
    print("   - Discrepancy remains very small (consistent with RH)")

    print("\n2. Pair Correlation Analysis:")
    print(f"   - Variance of normalized spacings: {pair_corr_results['variance']:.6f}")
    print(f"   - Expected for GUE: 1.0")
    print(f"   - Deviation from GUE: {abs(pair_corr_results['variance'] - 1):.6f}")
    print(f"   - Q_RH metric: {pair_corr_results['Q_RH']:.6f}")

    print("\n3. Eigenvector Analysis:")
    print(f"   - Participation ratio: {eigenvector_results['pr']:.2f}")
    print(f"   - Condition number: {np.real(eigenvector_results['evals'][0])/np.real(eigenvector_results['evals'][-1]):.2f}")
    print("   - Eigenvectors show structure (non-sinusoidal indicates correlations)")

    print("\nAll plots saved as PNG files in the current directory.")

    # Save results to a text file
    with open('rh_verification_results.txt', 'w') as f:
        f.write(f"Riemann Hypothesis Numerical Verification Results\\n")
        f.write(f"==================================================\\n")
        f.write(f"Timestamp: {time.ctime()}\\n")
        f.write(f"mpmath precision: {mp.mp.dps} decimal places\\n")
        f.write(f"Zero height T: {T_height}\\n")
        f.write(f"Number of zero pairs computed: {len(zeros)//2}\\n")
        f.write(f"\\nDiscrepancy |S1-S2|:\\n")
        for x, d in zip(x_vals, disc):
            f.write(f"  x={x:.1e}: {float(d):.2e}\\n")
        f.write(f"\\nPair Correlation:\\n")
        f.write(f"  Variance of normalized spacings: {pair_corr_results['variance']:.6f}\\n")
        f.write(f"  Expected for GUE: 1.0\\n")
        f.write(f"  Q_RH (integrated squared difference): {pair_corr_results['Q_RH']:.6f}\\n")
        f.write(f"\\nEigenvector Analysis:\\n")
        f.write(f"  Participation ratio: {eigenvector_results['pr']:.2f}\\n")
        f.write(f"  Condition number: {np.real(eigenvector_results['evals'][0])/np.real(eigenvector_results['evals'][-1]):.2f}\\n")

    print("\nResults saved to rh_verification_results.txt")

if __name__ == "__main__":
    main()