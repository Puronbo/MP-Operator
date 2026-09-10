import mpmath as mp
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist

mp.mp.dps = 30

def gue_pair_correlation(x):
    """GUE pair correlation function: R2(x) = 1 - (sin(πx)/(πx))^2"""
    if x == 0:
        return 0  # limit as x->0
    return 1 - (np.sin(np.pi * x) / (np.pi * x))**2

def compute_normalized_spacings(gamma_list):
    """Compute normalized spacings between consecutive zeros"""
    # gamma_list should be sorted positive imaginary parts
    spacings = np.diff(gamma_list)
    mean_spacing = np.mean(spacings)
    normalized_spacings = spacings / mean_spacing
    return normalized_spacings

def compute_pair_correlation(normalized_spacings, bins=50, max_val=5):
    """Compute pair correlation from normalized spacings"""
    # For small systems, we use all pairs
    # For larger systems, we might subsample
    n = len(normalized_spacings)
    if n < 1000:
        # Use all consecutive pairs (not all pairs to avoid O(n^2))
        differences = np.diff(normalized_spacings)
    else:
        # Subsample if too large
        indices = np.random.choice(n, size=min(1000, n), replace=False)
        indices = np.sort(indices)
        differences = np.diff(normalized_spacings[indices])

    # Compute histogram of differences
    hist, bin_edges = np.histogram(np.abs(differences), bins=bins, range=(0, max_val), density=True)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    return bin_centers, hist

def zeta_zeros_to_gamma(N):
    """Get first N zeta zero imaginary parts (positive)"""
    gammas = []
    for n in range(1, N+1):
        g = mp.zetazero(n).imag
        gammas.append(g)
    return sorted(gammas)

def main():
    print("Computing zeta zero statistics and comparing to GUE...")

    # Get zeta zeros
    N_zeros = 1000  # Use first 1000 zeros
    print(f"Computing first {N_zeros} zeta zeros...")
    gammas = zeta_zeros_to_gamma(N_zeros)
    print(f"Got {len(gammas)} zeros")

    # Compute normalized spacings
    print("Computing normalized spacings...")
    normalized_spacings = compute_normalized_spacings(gammas)
    print(f"Mean spacing: {np.mean(np.diff(gammas)):.6f}")
    print(f"Std of normalized spacings: {np.std(normalized_spacings):.6f}")

    # Compute pair correlation from spacings
    print("Computing pair correlation from normalized spacings...")
    bin_centers, pair_corr = compute_pair_correlation(normalized_spacings, bins=30, max_val=3.0)

    # Compute theoretical GUE pair correlation
    gue_vals = gue_pair_correlation(bin_centers)

    # Plot comparison
    plt.figure(figsize=(12, 8))

    plt.subplot(2, 2, 1)
    plt.plot(bin_centers, pair_corr, 'b-', label='Zeta zeros', linewidth=2)
    plt.plot(bin_centers, gue_vals, 'r--', label='GUE prediction', linewidth=2)
    plt.xlabel('Normalized spacing s')
    plt.ylabel('Pair correlation R2(s)')
    plt.title('Pair Correlation: Zeta Zeros vs GUE')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.subplot(2, 2, 2)
    plt.semilogy(bin_centers, np.abs(pair_corr - gue_vals), 'g-', linewidth=2)
    plt.xlabel('Normalized spacing s')
    plt.ylabel('|R2_zeta - R2_GUE| (log scale)')
    plt.title('Absolute Difference')
    plt.grid(True, alpha=0.3)

    # Compute Q_RH as integrated squared difference
    # Q_RH = ∫(R2_zeta(s) - R2_GUE(s))^2 ds / ∫R2_GUE(s)^2 ds
    from scipy.integrate import simpson

    numerator = simpson(np.abs(pair_corr - gue_vals)**2, bin_centers)
    denominator = simpson(gue_vals**2, bin_centers)

    if denominator > 0:
        Q_RH = numerator / denominator
    else:
        Q_RH = 0

    print(f"\nQ_RH (integrated squared difference): {Q_RH:.6f}")
    print(f"Interpretation: Q_RH < 1 suggests agreement with GUE (consistent with RH)")
    print(f"               Q_RH ≥ 1 suggests significant deviation from GUE")

    # Also compute based on variance of normalized spacings
    # For GUE, variance of normalized spacing is 1
    var_spacings = np.var(normalized_spacings)
    Q_RH_var = var_spacings  # Since expected variance is 1

    print(f"\nVariance of normalized spacings: {var_spacings:.6f}")
    print(f"Expected for GUE: 1.0")
    print(f"Q_RH (based on variance): {Q_RH_var:.6f}")

    plt.subplot(2, 2, 3)
    plt.hist(normalized_spacings, bins=30, alpha=0.7, density=True, label='Zeta zeros')
    x_vals = np.linspace(0, 3, 100)
    # GUE spacing distribution (Wigner surmise for GOE/GUE approximate)
    # For GUE, exact is complicated, but we can show Poisson for contrast
    plt.plot(x_vals, np.exp(-x_vals), 'g--', label='Poisson (uncorrelated)', linewidth=2)
    plt.xlabel('Normalized spacing')
    plt.ylabel('Density')
    plt.title('Spacing Distribution')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.subplot(2, 2, 4)
    # Compute the number variance Σ²(L) = <(N(L) - <N(L)>)²>
    # For GUE, Σ²(L) ~ (1/π²)(log(2πL) + γ + 1) + o(1)
    # For Poisson, Σ²(L) = L
    L_vals = np.logspace(-1, 1, 20)  # from 0.1 to 10
    sigma2_zeta = []
    sigma2_gue = []
    sigma2_poisson = []

    for L in L_vals:
        # Count number of spacings in intervals of length L*mean_spacing
        # Actually, better to work directly with the normalized spacings
        # Number variance for point process: variance of number of points in interval of length L
        # For normalized spacings with mean 1, interval of length L contains ~L points on average

        # For simplicity, compute variance of cumulative sum over windows
        cumsum = np.cumsum(normalized_spacings)
        counts = []
        window_size = int(L * len(normalized_spacings) / np.mean(np.diff(gammas)) * np.mean(np.diff(gammas)))  # This is messy

        # Let's do it properly: for normalized spacings with mean 1,
        # the number of points in interval [x, x+L] is approximately L
        # We'll use the fact that for a stationary process,
        # Σ²(L) = L + 2∫₀^L (L-s)[g₂(s)-1]ds where g₂ is pair correlation

        # For now, let's just show what we can compute easily
        pass

    # Instead, let's compute the spectral rigidity or number variance directly from the zeros
    # Number of zeros in interval [0, L] after unfolding
    # Unfolding: ξ_n = n * <d> where <d> is mean spacing
    # Actually, we already normalized so mean spacing = 1
    # So the unfolded zeros are approximately 0, 1, 2, 3, ..., N-1 plus fluctuations
    # The fluctuation is what we want

    # The unfolded zeros should be close to integers if perfectly spaced
    # deviation_n = gamma_n - n * mean_spacing
    # But better: since we normalized spacings to have mean 1,
    # the cumulative sum gives the unfolded zeros
    unfolded = np.cumsum(normalized_spacings)
    # These should be close to 0, 1, 2, 3, ..., N-1
    ideal = np.arange(len(unfolded))
    fluctuations = unfolded - ideal

    # Number variance: for interval of length L, variance of number of points
    # For large L, this relates to the pair correlation

    plt.subplot(2, 2, 4)
    plt.plot(ideal[:50], fluctuations[:50], 'b-', alpha=0.7)
    plt.xlabel('Zero index n')
    plt.ylabel('Fluctuation from uniform spacing')
    plt.title('Unfolding Fluctuations (first 50 zeros)')
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('gue_comparison.png', dpi=150, bbox_inches='tight')
    print("\nSaved gue_comparison.png")

    # Print some statistics
    print(f"\nStatistics of normalized spacings:")
    print(f"  Mean: {np.mean(normalized_spacings):.6f}")
    print(f"  Variance: {np.var(normalized_spacings):.6f}")
    print(f"  Skewness: {np.sqrt(len(normalized_spacings)) * np.mean((normalized_spacings - np.mean(normalized_spacings))**3) / (np.var(normalized_spacings)**1.5):.6f}")
    print(f"  Kurtosis: {len(normalized_spacings) * np.mean((normalized_spacings - np.mean(normalized_spacings))**4) / (np.var(normalized_spacings)**2) - 3:.6f}")

    # For GUE, the variance should approach 1 as N→∞
    print(f"\nDeviation from GUE variance expectation: {abs(np.var(normalized_spacings) - 1):.6f}")

if __name__ == "__main__":
    main()