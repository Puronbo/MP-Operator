#!/usr/bin/env python3
"""
Compute Q values for each domain using refined models from zero-as-condition analyses.
"""
import itertools

def get_valid_permutations():
    """Generate all valid permutations of {0,1,2,2,6} with no leading zero"""
    digits = [0, 1, 2, 2, 6]
    perms = set()
    for perm in itertools.permutations(digits):
        if perm[0] != 0:  # No leading zero
            num = perm[0]*10000 + perm[1]*1000 + perm[2]*100 + perm[3]*10 + perm[4]
            perms.add(num)
    return sorted(list(perms))

# Refined models per domain
def ns_model(permutation, timestamp):
    """Simplified NS Q_NS model (keeping original)"""
    vorticity_stretch = permutation * (timestamp % 100)
    enstrophy_density = (permutation ** 2) * (timestamp % 50)
    viscosity = 0.01
    q_ns = vorticity_stretch / (viscosity * enstrophy_density + 1)
    return q_ns

def ym_model(permutation, timestamp):
    """Simplified YM Q_YM model (keeping original)"""
    action_term = permutation / 10000.0
    string_term = (permutation % 1000) / 100.0
    mass_gap_term = 1.0 + (permutation % 50) / 100.0
    base = (action_term * string_term) / (mass_gap_term**4 + 1.0)

    instanton_term = (permutation % 7)
    theta_term = (permutation % 13) * 0.1
    gluon_cond_term = (permutation % 23) / 100.0
    monopole_term = (permutation % 19) / 50.0
    dyon_term = (permutation % 11) * 0.01
    spectral_term = (permutation % 9)

    corrections = 1.0 + instanton_term**2 + theta_term**2 + gluon_cond_term + monopole_term + dyon_term**2 + spectral_term
    q_ym = base * corrections
    return q_ym

def bsd_model(permutation, timestamp):
    """Simplified BSD Q_BSD model (keeping original)"""
    L_val = permutation * 0.0001
    L_deriv = (permutation % 97) * 0.00001
    rank = permutation % 3
    Omega = 1.0 + (permutation % 13) / 100.0
    Regulator = 1.0 + (permutation % 17) / 50.0
    Tamagawa = 1.0 + (permutation % 11)
    Sha = permutation % 7
    Tors = (permutation % 5) + 1

    # Stability conditions
    is_stable = (rank == 0) and (L_val != 0)
    is_unstable = (rank > 0) or (L_val == 0)

    # Q_BSD calculation (avoiding division by zero)
    denominator = Omega * Regulator * Tamagawa * Sha / (Tors * Tors)
    if denominator == 0:
        q_bsd = 0.0
    else:
        q_bsd = abs(L_deriv) / denominator

    return {
        'q_bsd': q_bsd,
        'is_stable': is_stable,
        'is_unstable': is_unstable,
        'rank': rank,
        'L_val': L_val,
        'Sha': Sha
    }

def hodge_model(permutation, timestamp):
    """Refined HODGE Q_H model from zero-as-condition analysis"""
    # griffithsSize = first two digits, hodgeSpaceDim = last three digits
    griffithsSize = (permutation // 1000)  # first two digits of 5-digit number
    hodgeSpaceDim = permutation % 1000     # last three digits
    if hodgeSpaceDim == 0:
        # avoid division by zero; if hodgeSpaceDim zero, set to 1
        hodgeSpaceDim = 1
    q_h = griffithsSize / hodgeSpaceDim
    return q_h

def pnp_model(permutation, timestamp):
    """Refined PNP Q_PNP model based on phase transition in random SAT"""
    # Map permutation to clause density alpha in [0,1] range
    # max permutation is 62210, min is 10226? Actually we'll normalize by 100000
    alpha = permutation / 100000.0  # roughly 0.1 to 0.62
    # critical alpha_c for 3-SAT ~ 0.4266? but we'll use 0.5 for simplicity
    alpha_c = 0.5
    q_pnp = alpha / alpha_c
    return q_pnp

def poincare_model(permutation, timestamp):
    """Refined POINCARE Q_P model from zero-as-condition analysis"""
    # Assignment from section 1 of poincare_analysis.txt:
    # entropy = first two digits
    # scalarCurvatureIntegral = next two digits
    # surgCount = last digit
    # minVol = 1, diam = 1, reducedVolume = 1
    entropy = permutation // 1000          # first two digits
    scalarCurvatureIntegral = (permutation // 10) % 100  # next two digits
    surgCount = permutation % 10           # last digit
    minVol = 1.0
    diam = 1.0
    reducedVolume = 1.0

    complexity = scalarCurvatureIntegral + surgCount * 10 + 1.0 / (minVol + 1.0)
    stabilizing = entropy + reducedVolume + 1.0 / (diam + 1.0)
    if stabilizing == 0:
        q_p = 0.0
    else:
        q_p = complexity / stabilizing
    return q_p

def riemann_model(permutation, timestamp):
    """Refined RIEMANN Q_RH model based on deviation from GUE (placeholder)"""
    # Use last digit as proxy for deviation from GUE
    # Q_RH = (deviation) / scale, where deviation in [0,9]
    # Set scale such that Q_RH >=1 when deviation >=5
    deviation = permutation % 10
    q_rh = deviation / 5.0  # 0-9 -> 0-1.8
    return q_rh

def main():
    base_timestamp = 972555980
    permutations = get_valid_permutations()
    print(f"Total valid permutations: {len(permutations)}")

    # We'll vary timestamp by offsets k*1000 for k=-5..5
    offsets = [k * 1000 for k in range(-5, 6)]

    # Prepare results dictionary: domain -> list of percentages stable per offset
    results = {
        'NS': [],
        'YM': [],
        'BSD': [],
        'HODGE': [],
        'PNP': [],
        'POINCARE': [],
        'RIEMANN': []
    }

    for offset in offsets:
        timestamp = base_timestamp + offset
        print(f"\nTimestamp: {timestamp} (offset {offset})")

        # For each domain, compute Q for each permutation and count stable (Q<1)
        stable_counts = {domain: 0 for domain in results}
        for p in permutations:
            q_ns = ns_model(p, timestamp)
            if q_ns < 1.0:
                stable_counts['NS'] += 1

            q_ym = ym_model(p, timestamp)
            if q_ym < 1.0:
                stable_counts['YM'] += 1

            bsd_res = bsd_model(p, timestamp)
            if bsd_res['is_stable']:
                stable_counts['BSD'] += 1

            q_h = hodge_model(p, timestamp)
            if q_h < 1.0:
                stable_counts['HODGE'] += 1

            q_pnp = pnp_model(p, timestamp)
            if q_pnp < 1.0:
                stable_counts['PNP'] += 1

            q_p = poincare_model(p, timestamp)
            if q_p < 1.0:
                stable_counts['POINCARE'] += 1

            q_rh = riemann_model(p, timestamp)
            if q_rh < 1.0:
                stable_counts['RIEMANN'] += 1

        # Compute percentages
        for domain in results:
            pct = stable_counts[domain] / len(permutations) * 100.0
            results[domain].append(pct)
            print(f"{domain}: {stable_counts[domain]}/{len(permutations)} stable ({pct:.1f}%)")

    # Print summary table
    print("\n\n=== Summary Table: Percentage Stable per Domain ===")
    print("Offset\\Domain", end="")
    for domain in results:
        print(f"\t{domain}", end="")
    print()
    for i, offset in enumerate(offsets):
        print(f"{offset}\t", end="")
        for domain in results:
            print(f"{results[domain][i]:.1f}\t", end="")
        print()

    # Also compute at base timestamp (offset 0) for quick reference
    base_idx = offsets.index(0)
    print("\n\n=== Base Timestamp (offset 0) Stability ===")
    for domain in results:
        print(f"{domain}: {results[domain][base_idx]:.1f}% stable")

    # Save to file
    with open('THRESHOLD_VALIDATION.md', 'w') as f:
        f.write('# Threshold Validation Results\n\n')
        f.write('Base timestamp: 972555980\n')
        f.write('Timestamp offsets: k * 1000 for k = -5..5\n\n')
        f.write('## Percentage Stable Predictions (Q < 1 = stable)\n\n')
        f.write('| Offset | NS | YM | BSD | HODGE | PNP | POINCARE | RIEMANN |\n')
        f.write('|--------|----|----|-----|-------|-----|----------|---------|\n')
        for i, offset in enumerate(offsets):
            f.write(f'| {offset} | {results["NS"][i]:.1f} | {results["YM"][i]:.1f} | {results["BSD"][i]:.1f} | '
                    f'{results["HODGE"][i]:.1f} | {results["PNP"][i]:.1f} | {results["POINCARE"][i]:.1f} | '
                    f'{results["RIEMANN"][i]:.1f} |\n')
    print("\\nResults saved to THRESHOLD_VALIDATION.md")

if __name__ == "__main__":
    main()