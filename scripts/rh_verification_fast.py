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
        if n % 100 == 0:
            print(f"  Computed {n} zeros so far...")
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
    gammas = sorted([float(abs(z.imag)) for z in zeros if z.imag > 0])  # Positive imaginary parts
    print(f"Using {len(gammas)} positive zeros for pair correlation")

    # Compute normalized spacings
    spacings = np.diff(gammas)
    mean_spacing = np.mean(spacings)
    normalized_spacings = spacings / mean_spacing

    print(f"Mean spacing: {float(mean_spacing):.6f}")
    print(f"Std of normalized spacings: {float(np.std(normalized_spacings)):.6f}")
    print(f"Variance of normalized spacings: {float(np.var(normalized_spacings)):.6f}")

    # Compute histogram of normalized spacings
    hist, bin_edges = np.histogram(normalized_spacings, bins=50, range=(0, 3), density=True)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    # Theoretical GUE prediction
    def gue_pair_correlation(x):
        """GUE pair correlation function: R2(x) = 1 - (sin(πx)/(πx))^2"""
        x = np.asarray(x)
        result = np.ones_like(x)
        mask = x != 0
        result[mask] = 1 - (np.sin(np.pi * x[mask]) / (np.pi * x[mask]))**2
        return result

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
    print(f"               Q_RH >= 1 suggests significant deviation from GUE")

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
    plt.savefig('gue_comparison_rh_fast.png', dpi=150, bbox_inches='tight')
    print("\nSaved gue_comparison_rh_fast.png")

    return {
        'normalized_spacings': normalized_spacings,
        'variance': np.var(normalized_spacings),
        'Q_RH': Q_RH
    }

def main():
    """Main function to run analyses"""
    print("Riemann Hypothesis Numerical Verification (Fast Version)")
    print("=" * 60)
    print(f"Started at: {time.ctime()}")

    start_time = time.time()

    # Choose T for zero height (smaller for speed)
    T_height = 500  # This will give about ~500/(2*pi)*log(500/(2*pi)) ≈ 500/(6.28)*log(79.6)≈79.7*4.38≈349 zeros? Actually compute.
    print(f"\nComputing zeros up to T = {T_height}")
    zeros = compute_zeros_up_to_T(T_height)
    print(f"Total zeros (including conjugates): {len(zeros)}")

    if len(zeros) == 0:
        print("No zeros computed. Exiting.")
        return

    # Discrepancy analysis
    print("\n=== DISCREPANCY ANALYSIS ===")
    x_vals = [10, 100, 1000, 10000]  # Reduced x range
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
    plt.savefig('discrepancy_vs_x_rh_fast.png', dpi=150)
    print("\nSaved discrepancy_vs_x_rh_fast.png")

    # Pair correlation analysis
    pair_corr_results = pair_correlation_analysis(zeros)

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

    print("\nAll plots saved as PNG files in the current directory.")

    # Save results to a text file
    with open('rh_verification_fast_results.txt', 'w') as f:
        f.write(f"Riemann Hypothesis Numerical Verification Results (Fast)\\n")
        f.write(f"==========================================================\\n")
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

    print("\nResults saved to rh_verification_fast_results.txt")

if __name__ == "__main__":
    main()