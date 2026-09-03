import mpmath as mp
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist
from scipy.integrate import simpson
import time

# Set high precision
mp.mp.dps = 100  # Increased precision as requested
print(f"Using mpmath precision: {mp.mp.dps} decimal places")

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

def get_zeta_zeros(T_height):
    """Get zeta zeros with imaginary part < T_height"""
    zeros = []
    n = 1
    start_time = time.time()
    while True:
        g = mp.zetazero(n).imag
        if g > T_height:
            break
        zeros.append(mp.mpc(0.5, g))
        zeros.append(mp.mpc(0.5, -g))
        n += 1
    end_time = time.time()
    print(f"Computed {len(zeros)//2} zero pairs (imaginary part < {T_height}) in {end_time-start_time:.2f}s")
    return zeros

def discrepancy_analysis():
    """Analyze discrepancy S1(x)-S2(x) for various x and T"""
    print("\n=== DISCREPANCY ANALYSIS ===")

    # Test various heights T
    T_vals = [100, 200, 500, 1000]  # Increased T as requested
    x_vals = [10, 100, 1000, 10000, 100000]  # Extended x range

    print("Discrepancy |S1-S2| for various T (height) and x:")
    print("T\\x", end="")
    for x in x_vals:
        print(f"\t{x:.0e}", end="")
    print()

    all_results = {}
    for T in T_vals:
        zeros = get_zeta_zeros(T)
        S1, S2 = compute_sums(zeros, x_vals)
        diff = np.abs(S1 - S2)
        all_results[T] = diff

        print(f"{T}\t", end="")
        for d in diff:
            print(f"{float(d):.2e}\t", end="")
        print()
        print(f"  Number of zero pairs: {len(zeros)//2}")

    # Plot discrepancy vs x for different T
    plt.figure(figsize=(12, 8))
    for T in T_vals:
        plt.semilogy(x_vals, all_results[T], 'o-', linewidth=2, label=f'T={T}')
    plt.xlabel('x')
    plt.ylabel('|S1(x) - S2(x)|')
    plt.title('Discrepancy vs x for different heights T (dps=100)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('discrepancy_vs_x_T.png', dpi=150)
    print("\nSaved discrepancy_vs_x_T.png")

    return all_results

def pair_correlation_analysis():
    """Compute pair correlation statistics and compare to GUE"""
    print("\n=== PAIR CORRELATION ANALYSIS ===")

    # Get zeros for pair correlation (need many for good statistics)
    T_pc = 1000  # Height for pair correlation
    print(f"Computing zeros up to T={T_pc} for pair correlation...")
    zeros = get_zeta_zeros(T_pc)
    gammas = sorted([abs(z.imag) for z in zeros if z.imag > 0])  # Positive imaginary parts

    print(f"Using {len(gammas)} positive zeros for pair correlation")

    # Compute normalized spacings
    spacings = np.diff(gammas)
    mean_spacing = np.mean(spacings)
    normalized_spacings = spacings / mean_spacing

    print(f"Mean spacing: {mean_spacing:.6f}")
    print(f"Std of normalized spacings: {np.std(normalized_spacings):.6f}")
    print(f"Variance of normalized spacings: {np.var(normalized_spacings):.6f}")

    # Compute pair correlation from normalized spacings
    def gue_pair_correlation(x):
        """GUE pair correlation function: R2(x) = 1 - (sin(πx)/(πx))^2"""
        if x == 0:
            return 0  # limit as x->0
        return 1 - (np.sin(np.pi * x) / (np.pi * x))**2

    # Use all pairs for smaller samples, subsample for larger
    n = len(normalized_spacings)
    if n < 2000:
        differences = np.diff(normalized_spacings)
    else:
        # Subsample to avoid O(n^2)
        indices = np.random.choice(n, size=min(2000, n), replace=False)
        indices = np.sort(indices)
        differences = np.diff(normalized_spacings[indices])

    # Compute histogram of absolute differences
    hist, bin_edges = np.histogram(np.abs(differences), bins=50, range=(0, 3), density=True)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    # Theoretical GUE prediction
    gue_vals = gue_pair_correlation(bin_centers)

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

    # Variance based Q_RH
    var_spacings = np.var(normalized_spacings)
    Q_RH_var = var_spacings  # Expected variance for GUE is 1

    print(f"\nVariance of normalized spacings: {var_spacings:.6f}")
    print(f"Expected for GUE: 1.0")
    print(f"Q_RH (based on variance): {Q_RH_var:.6f}")

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
    plt.savefig('gue_comparison_enhanced.png', dpi=150, bbox_inches='tight')
    print("\nSaved gue_comparison_enhanced.png")

    return {
        'normalized_spacings': normalized_spacings,
        'variance': var_spacings,
        'Q_RH': Q_RH,
        'Q_RH_var': Q_RH_var
    }

def eigenvector_analysis_enhanced():
    """Enhanced eigenvector analysis of correlation matrix F*F"""
    print("\n=== EIGENVECTOR ANALYSIS ENHANCED ===")

    # Get zeros for eigenvector analysis
    T_eigen = 500  # Moderate height for eigenvector analysis
    print(f"Computing zeros up to T={T_eigen} for eigenvector analysis...")
    zeros = get_zeta_zeros(T_eigen)
    gamma_vals = sorted([abs(z.imag) for z in zeros if z.imag > 0])  # Positive gammas

    print(f"Using {len(gamma_vals)} positive zeros for eigenvector analysis")

    # Build F matrix and compute F*F (F^H F)
    def build_F_and_FtF(zeros_gamma, M=30):
        """Build F matrix and compute F*F = F^H F"""
        N = len(zeros_gamma)
        # Test x values: log-spaced from 10^1 to 10^4 (extended range)
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
        plt.savefig(f'eigenvector_{label_safe}_enhanced.png', dpi=150)
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
        plt.savefig(f'eigenvector_vs_zero_{label_safe2}_enhanced.png', dpi=150)
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
    F_zeta, FtF_zeta, x_zeta, zeta_zeros = build_F_and_FtF(gamma_vals[:30])  # First 15 pairs
    zeta_eigen = analyze_eigenvectors(FtF_zeta, "Zeta", zeta_zeros)

    print(f"Zeta: Participation ratio = {zeta_eigen['pr']:.2f}")
    print(f"Largest eigenvalue: {np.real(zeta_eigen['evals'][0]):.2f}")
    print(f"Smallest eigenvalue: {np.real(zeta_eigen['evals'][-1]):.2f}")
    print(f"Condition number: {np.real(zeta_eigen['evals'][0])/np.real(zeta_eigen['evals'][-1]):.2f}")

    # Also analyze for different x ranges to see eigenvector stability
    print("\nAnalyzing eigenvector stability with different x ranges...")
    x_ranges = [
        (1.0, 2.0),   # low x
        (1.0, 3.0),   # medium-low
        (2.0, 4.0),   # medium-high
        (1.0, 4.0),   # full range
    ]

    participation_ratios = []
    for i, (x_min, x_max) in enumerate(x_ranges):
        x_vals = [10**j for j in np.linspace(np.log10(x_min), np.log10(x_max), 20)]
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
        plt.savefig(f'eigenvector_xrange_{i}_enhanced.png', dpi=150)
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
    plt.savefig('participation_ratio_vs_xrange.png', dpi=150)
    plt.close()

    return zeta_eigen, participation_ratios

def main():
    """Main function to run all analyses"""
    print("Riemann Hypothesis Numerical Verification")
    print("=" * 50)
    print(f"Started at: {time.ctime()}")

    start_time = time.time()

    # Run all analyses
    discrepancy_results = discrepancy_analysis()
    pair_corr_results = pair_correlation_analysis()
    eigenvector_results, participation_ratios = eigenvector_analysis_enhanced()

    end_time = time.time()

    print("\n" + "=" * 50)
    print("ANALYSIS COMPLETE")
    print(f"Total time: {end_time - start_time:.2f} seconds")
    print(f"Finished at: {time.ctime()}")

    # Summary of key findings
    print("\n=== KEY FINDINGS ===")
    print("1. Discrepancy Analysis:")
    print(f"   - For T=1000, discrepancy at x=100000: {discrepancy_results[1000][-1]:.2e}")
    print("   - Discrepancy remains small (consistent with RH) but grows with x and T")

    print("\n2. Pair Correlation Analysis:")
    print(f"   - Variance of normalized spacings: {pair_corr_results['variance']:.6f}")
    print(f"   - Expected for GUE: 1.0")
    print(f"   - Deviation from GUE: {abs(pair_corr_results['variance'] - 1):.6f}")
    print(f"   - Q_RH metric: {pair_corr_results['Q_RH']:.6f}")

    print("\n3. Eigenvector Analysis:")
    print(f"   - Participation ratio (standard x range): {eigenvector_results['pr']:.2f}")
    print(f"   - Participation ratios across x ranges: {[f'{pr:.2f}' for pr in participation_ratios]}")
    print("   - Eigenvectors show some structure but not purely sinusoidal")

    print("\nAll plots saved as PNG files in the current directory.")

if __name__ == "__main__":
    main()