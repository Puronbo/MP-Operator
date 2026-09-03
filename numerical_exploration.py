#!/usr/bin/env python3
"""
Numerical exploration of threshold behavior in Millennium Prize Problems
Using user-provided number sets and timestamp
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

def ns_model(permutation, timestamp):
    """Simplified NS Q_NS model"""
    vorticity_stretch = permutation * (timestamp % 100)
    enstrophy_density = (permutation ** 2) * (timestamp % 50)
    viscosity = 0.01
    q_ns = vorticity_stretch / (viscosity * enstrophy_density + 1)
    return q_ns

def ym_model(permutation, timestamp):
    """Simplified YM Q_YM model"""
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
    """Simplified BSD Q_BSD model"""
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

def main():
    timestamp = 972555980
    permutations = get_valid_permutations()

    print(f"Total valid permutations: {len(permutations)}")
    print(f"Starting permutation (timestamp mod 48 = {timestamp % 48}): {permutations[timestamp % 48]}")
    print()

    # Analyze first 10 permutations in detail
    print("First 10 permutations analysis:")
    print("Perm\tNS_Q\tYM_Q\tBSD_Q\tStable?")
    print("-" * 40)

    for i in range(min(10, len(permutations))):
        p = permutations[i]
        q_ns = ns_model(p, timestamp)
        q_ym = ym_model(p, timestamp)
        bsd_result = bsd_model(p, timestamp)
        print(f"{p}\t{q_ns:.3f}\t{q_ym:.3f}\t{bsd_result['q_bsd']:.3f}\t{bsd_result['is_stable']}")

    print()

    # Threshold crossing statistics
    ns_above_threshold = sum(1 for p in permutations if ns_model(p, timestamp) > 1.0)
    ym_above_threshold = sum(1 for p in permutations if ym_model(p, timestamp) >= 1.0)
    bsd_stable_count = sum(1 for p in permutations if bsd_model(p, timestamp)['is_stable'])

    print(f"Threshold crossing statistics:")
    print(f"NS model: {ns_above_threshold}/{len(permutations)} permutations with Q_NS > 1 ({100*ns_above_threshold/len(permutations):.1f}%)")
    print(f"YM model: {ym_above_threshold}/{len(permutations)} permutations with Q_YM >= 1 ({100*ym_above_threshold/len(permutations):.1f}%)")
    print(f"BSD model: {bsd_stable_count}/{len(permutations)} permutations stable ({100*bsd_stable_count/len(permutations):.1f}%)")

    print()
    # Example detailed calculation for starting permutation
    start_idx = timestamp % 48
    start_perm = permutations[start_idx]
    print(f"Detailed analysis for starting permutation {start_perm}:")
    print(f"  NS Q_NS: {ns_model(start_perm, timestamp):.6f}")
    print(f"  YM Q_YM: {ym_model(start_perm, timestamp):.6f}")
    bsd_det = bsd_model(start_perm, timestamp)
    print(f"  BSD Q_BSD: {bsd_det['q_bsd']:.6f}")
    print(f"  BSD Stable: {bsd_det['is_stable']} (rank={bsd_det['rank']}, L_val={bsd_det['L_val']:.4f}, Sha={bsd_det['Sha']})")

if __name__ == "__main__":
    main()