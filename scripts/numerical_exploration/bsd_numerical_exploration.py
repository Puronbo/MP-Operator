#!/usr/bin/env python3
"""
Numerical exploration for Birch and Swinnerton-Dyer conjecture using zero-as-condition perspective.
Based on the plans in Hodge_Zero_As_Condition_Next_Steps/, Hodge_Analysis/, etc.
"""

import itertools
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict
import json

def generate_permutations(digits: List[int]) -> List[Tuple[int, ...]]:
    """Generate all unique permutations of the digits, excluding those with leading zero."""
    perms = set(itertools.permutations(digits))
    # Filter out permutations that start with 0
    valid_perms = [p for p in perms if p[0] != 0]
    return sorted(valid_perms)

def assign_scheme_a(perm: Tuple[int, ...]) -> Dict[str, float]:
    """
    Assignment Scheme A (inspired by BSD structure):
    - Based on the Birch and Swinnerton-Dyer conjecture which relates
      the rank of an elliptic curve to the order of vanishing of its L-function
    - We'll create a Q_BSD parameter that measures deviation from critical behavior

    Scheme A:
    - N = first two digits as integer (conductor-like parameter)
    - r = (third digit) * (fourth digit) - (fifth digit)  # rank-like parameter
    - L0 = sum of digits / 10.0  # L-function value at s=1 (normalized)
    - Q_BSD = |(r / (N * L0)) - 1| if N > 0 and L0 > 0 else 1.0
    """
    # Convert permutation to number
    perm_num = int(''.join(map(str, perm)))

    N = int(''.join(map(str, perm[:2])))  # First two digits
    r = perm[2] * perm[3] - perm[4]       # Third * fourth - fifth
    L0 = sum(perm) / 10.0

    # Compute Q_BSD analogous to previous Q parameters
    if N > 0 and L0 > 0:
        normalizedValue = r / (N * L0)
        Q_BSD = abs(normalizedValue - 1.0)
    else:
        Q_BSD = 1.0  # Default to critical point when undefined

    return {
        'permutation': perm,
        'perm_num': perm_num,
        'N': N,
        'r': r,
        'L0': L0,
        'normalizedValue': r / (N * L0) if N > 0 and L0 > 0 else 0.0,
        'Q_BSD': Q_BSD,
        'rankDeficit': Q_BSD > 1.0,   # Q_BSD > 1 -> rank deficit (like undershooting)
        'rankExcess': Q_BSD < 1.0,    # Q_BSD < 1 -> rank excess (like overshooting)
        'criticalPoint': abs(Q_BSD - 1.0) < 0.001,  # Approximately Q_BSD = 1
        'stable': Q_BSD < 1.0,        # Stable when not exceeding rank bounds
        'unstable': Q_BSD >= 1.0      # Unstable when at or exceeding critical threshold
    }

def assign_scheme_b(perm: Tuple[int, ...]) -> Dict[str, float]:
    """
    Assignment Scheme B (alternative splitting with rank focus):
    - N = first three digits as integer
    - r = last two digits as integer
    - L0 = (product of digits) / 100.0
    - Q_BSD = |(r / (N * L0)) - 1| if N > 0 and L0 > 0 else 1.0
    """
    N = int(''.join(map(str, perm[:3])))  # First three digits
    r = int(''.join(map(str, perm[3:])))  # Last two digits
    L0 = np.prod(perm) / 100.0

    # Compute Q_BSD
    if N > 0 and L0 > 0:
        normalizedValue = r / (N * L0)
        Q_BSD = abs(normalizedValue - 1.0)
    else:
        Q_BSD = 1.0  # Default to critical point when undefined

    return {
        'permutation': perm,
        'perm_num': int(''.join(map(str, perm))),
        'N': N,
        'r': r,
        'L0': L0,
        'normalizedValue': r / (N * L0) if N > 0 and L0 > 0 else 0.0,
        'Q_BSD': Q_BSD,
        'rankDeficit': Q_BSD > 1.0,
        'rankExcess': Q_BSD < 1.0,
        'criticalPoint': abs(Q_BSD - 1.0) < 0.001,
        'stable': Q_BSD < 1.0,
        'unstable': Q_BSD >= 1.0
    }

def assign_scheme_c(perm: Tuple[int, ...]) -> Dict[str, float]:
    """
    Assignment Scheme C (using timestamp idea with BSD connection):
    - N = (product of digits) % 1000
    - r = (timestamp % 100)  # last two digits of timestamp
    - L0 = (sum of digits) / 10.0
    - Q_BSD = |(r / (N * L0)) - 1| if N > 0 and L0 > 0 else 1.0
    """
    timestamp = 972555980
    perm_num = int(''.join(map(str, perm)))

    N = np.prod(perm) % 1000
    r = timestamp % 100
    L0 = sum(perm) / 10.0

    # Compute Q_BSD
    if N > 0 and L0 > 0:
        normalizedValue = r / (N * L0)
        Q_BSD = abs(normalizedValue - 1.0)
    else:
        Q_BSD = 1.0  # Default to critical point when undefined

    return {
        'permutation': perm,
        'perm_num': perm_num,
        'N': N,
        'r': r,
        'L0': L0,
        'normalizedValue': r / (N * L0) if N > 0 and L0 > 0 else 0.0,
        'Q_BSD': Q_BSD,
        'rankDeficit': Q_BSD > 1.0,
        'rankExcess': Q_BSD < 1.0,
        'criticalPoint': abs(Q_BSD - 1.0) < 0.001,
        'stable': Q_BSD < 1.0,
        'unstable': Q_BSD >= 1.0
    }

def test_axioms(results: List[Dict]) -> Dict:
    """Test the axioms and derived theorems from BSD conjecture documents."""
    axioms = {
        'stable_if_Q_BSD_lt_one': [],
        'unstable_if_Q_BSD_ge_one': [],
        'criticalPoint_balance': [],  # At critical point (analytic rank = algebraic rank)
        'rank_consistency': []        # Rank properties are consistent
    }

    for result in results:
        # Test stable_if_Q_BSD_lt_one
        if result['Q_BSD'] < 1.0:
            axioms['stable_if_Q_BSD_lt_one'].append(result)

        # Test unstable_if_Q_BSD_ge_one
        if result['Q_BSD'] >= 1.0:
            axioms['unstable_if_Q_BSD_ge_one'].append(result)

        # Test criticalPoint_balance (at Q_BSD ≈ 1, we should have balance)
        if abs(result['Q_BSD'] - 1.0) < 0.1:  # Near critical point
            # At critical point: not in rank deficit AND not in rank excess
            if not result['rankDeficit'] and not result['rankExcess']:
                axioms['criticalPoint_balance'].append(result)

        # Test rank_consistency (rank properties should be mutually exclusive)
        if result['rankDeficit'] and result['rankExcess']:
            # This should never happen - a point can't have both deficit and excess
            pass  # Intentionally empty - we want 0 cases here
        else:
            axioms['rank_consistency'].append(result)

    return axioms

def main():
    """Main numerical exploration function."""
    digits = [0, 1, 2, 2, 6]
    permutations = generate_permutations(digits)

    print(f"Generated {len(permutations)} permutations of {digits}")
    print("=" * 50)

    # Test each assignment scheme
    schemes = [
        ("Scheme A (inspired by BSD structure)", assign_scheme_a),
        ("Scheme B (3+2 split)", assign_scheme_b),
        ("Scheme C (timestamp-based)", assign_scheme_c)
    ]

    all_results = {}

    for scheme_name, scheme_func in schemes:
        print(f"\n{scheme_name}:")
        print("-" * 30)

        results = [scheme_func(p) for p in permutations]
        all_results[scheme_name] = results

        # Summary statistics
        stable_count = sum(1 for r in results if r['stable'])
        unstable_count = len(results) - stable_count
        critical_count = sum(1 for r in results if r['criticalPoint'])
        deficit_count = sum(1 for r in results if r['rankDeficit'])
        excess_count = sum(1 for r in results if r['rankExcess'])

        Q_BSD_values = [r['Q_BSD'] for r in results]
        if Q_BSD_values:
            min_Q_BSD = min(Q_BSD_values)
            max_Q_BSD = max(Q_BSD_values)
            mean_Q_BSD = np.mean(Q_BSD_values)
        else:
            min_Q_BSD = max_Q_BSD = mean_Q_BSD = 0.0

        print(f"Stable (Q_BSD < 1): {stable_count}/{len(results)}")
        print(f"Unstable (Q_BSD >= 1): {unstable_count}/{len(results)}")
        print(f"Critical points (Q_BSD ~ 1): {critical_count}/{len(results)}")
        print(f"Rank deficit (Q_BSD > 1): {deficit_count}/{len(results)}")
        print(f"Rank excess (Q_BSD < 1): {excess_count}/{len(results)}")
        print(f"Q_BSD range: {min_Q_BSD:.4f} to {max_Q_BSD:.4f}")
        print(f"Mean Q_BSD: {mean_Q_BSD:.4f}")

        # Show some examples
        print("\nFirst 5 results:")
        for i, result in enumerate(results[:5]):
            rank_status = ""
            if result['criticalPoint']:
                rank_status = " [Critical]"
            elif result['rankDeficit']:
                rank_status = " [Deficit]"
            elif result['rankExcess']:
                rank_status = " [Excess]"
            print(f"  {result['permutation']}: Q_BSD = {result['Q_BSD']:.4f}{rank_status}")

    # Test axioms
    print("\n" + "=" * 50)
    print("AXIOM TESTING:")
    print("=" * 50)

    for scheme_name, results in all_results.items():
        print(f"\n{scheme_name}:")
        axioms = test_axioms(results)

        for axiom_name, supporting_results in axioms.items():
            print(f"  {axiom_name}: {len(supporting_results)} supporting cases")

    # Save results to JSON for further analysis
    output_data = {
        'digits': digits,
        'timestamp': 972555980,
        'schemes': {}
    }

    for scheme_name, results in all_results.items():
        # Convert numpy types and booleans in each result
        converted_results = []
        for result in results:
            converted_result = {}
            for key, value in result.items():
                if isinstance(value, np.integer):
                    converted_result[key] = int(value)
                elif isinstance(value, np.floating):
                    converted_result[key] = float(value)
                elif isinstance(value, np.bool_):
                    converted_result[key] = bool(value)
                elif isinstance(value, bool):
                    converted_result[key] = value
                else:
                    converted_result[key] = value
            converted_results.append(converted_result)
        output_data['schemes'][scheme_name] = converted_results

    with open('scripts/numerical_exploration/bsd_results.json', 'w') as f:
        json.dump(output_data, f, indent=2)

    print(f"\nResults saved to scripts/numerical_exploration/bsd_results.json")

    # Create visualizations
    create_visualizations(all_results)

def create_visualizations(results_dict):
    """Create visualizations of the numerical exploration results."""
    try:
        plt.figure(figsize=(15, 5))

        for idx, (scheme_name, results) in enumerate(results_dict.items()):
            plt.subplot(1, 3, idx + 1)

            # Extract Q_BSD values
            Q_BSD_values = [r['Q_BSD'] for r in results]
            permutations_str = [''.join(map(str, r['permutation'])) for r in results]
            stable = [r['stable'] for r in results]
            critical = [r['criticalPoint'] for r in results]
            deficit = [r['rankDeficit'] for r in results]
            excess = [r['rankExcess'] for r in results]

            # Create color scheme: blue for stable/excess, red for unstable/deficit, green for critical
            colors = []
            for i in range(len(results)):
                if critical[i]:
                    colors.append('green')      # Critical point
                elif deficit[i]:
                    colors.append('red')        # Rank deficit (unstable)
                else:  # excess[i] and stable[i]
                    colors.append('blue')       # Rank excess (stable)

            # Create bar chart
            bars = plt.bar(range(len(Q_BSD_values)), Q_BSD_values, color=colors, alpha=0.7)

            # Add threshold lines
            plt.axhline(y=1.0, color='black', linestyle='--', alpha=0.5, label='Q_BSD = 1 (Critical)')
            plt.axhline(y=0.0, color='gray', linestyle='-', alpha=0.3, label='Q_BSD = 0')

            plt.xlabel('Permutation Index')
            plt.ylabel('Q_BSD Value')
            plt.title(f'{scheme_name}\n(Green: Critical, Red: Deficit/Unstable, Blue: Excess/Stable)')
            plt.xticks(range(len(permutations_str)), permutations_str, rotation=45, ha='right')
            plt.legend()

            # Add value labels on bars
            for i, (bar, value) in enumerate(zip(bars, Q_BSD_values)):
                plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                        f'{value:.2f}', ha='center', va='bottom', fontsize=8)

        plt.tight_layout()
        plt.savefig('scripts/numerical_exploration/bsd_visualization.png', dpi=150, bbox_inches='tight')
        print("Visualization saved to scripts/numerical_exploration/bsd_visualization.png")

    except ImportError:
        print("Matplotlib not available, skipping visualization")

if __name__ == "__main__":
    main()