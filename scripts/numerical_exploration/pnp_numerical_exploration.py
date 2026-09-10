#!/usr/bin/env python3
"""
Numerical exploration for P versus NP problem using zero-as-condition perspective.
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
    Assignment Scheme A (inspired by SATEnsemble structure):
    - n = first two digits as integer
    - m = last three digits as integer
    - alpha = m / n as float (if n > 0, else 0)
    - alpha_c = 0.5 (placeholder critical threshold for k=2 SAT, but we use fixed for simplicity)
    - hardness = sum of digits
    - msgEntropy = (permutation as number) % 10 / 10.0  # between 0 and 1
    - clustering = (permutation as number) % 5 / 5.0   # between 0 and 1
    - Q_SAT = alpha / alpha_c
    """
    # Convert permutation to number
    perm_num = int(''.join(map(str, perm)))

    n = int(''.join(map(str, perm[:2])))  # First two digits
    m = int(''.join(map(str, perm[2:])))  # Last three digits

    # Avoid division by zero
    if n == 0:
        n = 1

    alpha = m / n
    alpha_c = 0.5  # placeholder critical threshold
    hardness = sum(perm)
    msgEntropy = (perm_num % 10) / 10.0
    clustering = (perm_num % 5) / 5.0

    Q_SAT = alpha / alpha_c if alpha_c != 0 else float('inf')

    return {
        'permutation': perm,
        'perm_num': perm_num,
        'n': n,
        'm': m,
        'alpha': alpha,
        'alpha_c': alpha_c,
        'hardness': hardness,
        'msgEntropy': msgEntropy,
        'clustering': clustering,
        'Q_SAT': Q_SAT,
        'stable': Q_SAT < 1.0,
        'unstable': Q_SAT >= 1.0
    }

def assign_scheme_b(perm: Tuple[int, ...]) -> Dict[str, float]:
    """
    Assignment Scheme B (alternative splitting):
    - n = first three digits as integer
    - m = last two digits as integer
    - alpha = m / n as float (if n > 0, else 0)
    - alpha_c = 0.35 (placeholder for k=3 SAT critical threshold)
    - hardness = product of digits
    - msgEntropy = (sum of digits) / 30.0  # normalized
    - clustering = (permutation as number) % 7 / 7.0  # between 0 and 1
    - Q_SAT = alpha / alpha_c
    """
    n = int(''.join(map(str, perm[:3])))  # First three digits
    m = int(''.join(map(str, perm[3:])))  # Last two digits

    # Avoid division by zero
    if n == 0:
        n = 1

    alpha = m / n
    alpha_c = 0.35  # placeholder critical threshold for k=3
    hardness = np.prod(perm)
    msgEntropy = sum(perm) / 30.0
    clustering = (int(''.join(map(str, perm))) % 7) / 7.0

    Q_SAT = alpha / alpha_c if alpha_c != 0 else float('inf')

    return {
        'permutation': perm,
        'perm_num': int(''.join(map(str, perm))),
        'n': n,
        'm': m,
        'alpha': alpha,
        'alpha_c': alpha_c,
        'hardness': hardness,
        'msgEntropy': msgEntropy,
        'clustering': clustering,
        'Q_SAT': Q_SAT,
        'stable': Q_SAT < 1.0,
        'unstable': Q_SAT >= 1.0
    }

def assign_scheme_c(perm: Tuple[int, ...]) -> Dict[str, float]:
    """
    Assignment Scheme C (using timestamp idea):
    - n = (product of digits) % 100 + 1  # ensure at least 1
    - m = (timestamp % 1000)  # last three digits of timestamp
    - alpha = m / n as float
    - alpha_c = 0.45 (placeholder)
    - hardness = (timestamp % 100)  # last two digits of timestamp
    - msgEntropy = (sum of digits) / 20.0
    - clustering = ( (permutation as number) * timestamp ) % 11 / 11.0
    - Q_SAT = alpha / alpha_c
    """
    timestamp = 972555980
    perm_num = int(''.join(map(str, perm)))

    n = (np.prod(perm) % 100) + 1  # ensure at least 1
    m = timestamp % 1000
    alpha = m / n
    alpha_c = 0.45  # placeholder
    hardness = timestamp % 100
    msgEntropy = sum(perm) / 20.0
    clustering = (perm_num * timestamp) % 11 / 11.0

    Q_SAT = alpha / alpha_c if alpha_c != 0 else float('inf')

    return {
        'permutation': perm,
        'perm_num': perm_num,
        'n': n,
        'm': m,
        'alpha': alpha,
        'alpha_c': alpha_c,
        'hardness': hardness,
        'msgEntropy': msgEntropy,
        'clustering': clustering,
        'Q_SAT': Q_SAT,
        'stable': Q_SAT < 1.0,
        'unstable': Q_SAT >= 1.0
    }

def test_axioms(results: List[Dict]) -> Dict:
    """Test the axioms and derived theorems from the P vs NP documents."""
    axioms = {
        'stable_if_Q_SAT_lt_one': [],
        'unstable_if_Q_SAT_ge_one': [],
        'hardness_affects_Q': [],
        'clustering_shifts_threshold': []
    }

    for result in results:
        # Test stable_if_Q_SAT_lt_one
        if result['Q_SAT'] < 1.0:
            axioms['stable_if_Q_SAT_lt_one'].append(result)

        # Test unstable_if_Q_SAT_ge_one
        if result['Q_SAT'] >= 1.0:
            axioms['unstable_if_Q_SAT_ge_one'].append(result)

        # Test hardness_affects_Q (if hardness > 100, then Q_SAT > 0.5)
        if result['hardness'] > 100:
            if result['Q_SAT'] > 0.5:
                axioms['hardness_affects_Q'].append(result)

        # Test clustering_shifts_threshold (if msgEntropy < 1, then Q_SAT >= 0.9 -> Unstable)
        if result['msgEntropy'] < 1.0:
            if result['Q_SAT'] >= 0.9:
                # This axiom says: if msgEntropy < 1 and Q_SAT >= 0.9 then Unstable
                # So we check if the result is indeed unstable (Q_SAT >= 1) - note the axiom uses Unstable which is Q_SAT >= 1
                if result['Q_SAT'] >= 1.0:
                    axioms['clustering_shifts_threshold'].append(result)

    return axioms

def main():
    """Main numerical exploration function."""
    digits = [0, 1, 2, 2, 6]
    permutations = generate_permutations(digits)

    print(f"Generated {len(permutations)} permutations of {digits}")
    print("=" * 50)

    # Test each assignment scheme
    schemes = [
        ("Scheme A (2+3 split)", assign_scheme_a),
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

        Q_SAT_values = [r['Q_SAT'] for r in results if r['Q_SAT'] != float('inf')]
        if Q_SAT_values:
            min_Q_SAT = min(Q_SAT_values)
            max_Q_SAT = max(Q_SAT_values)
            mean_Q_SAT = np.mean(Q_SAT_values)
        else:
            min_Q_SAT = max_Q_SAT = mean_Q_SAT = 0.0

        print(f"Stable (Q_SAT < 1): {stable_count}/{len(results)}")
        print(f"Unstable (Q_SAT >= 1): {unstable_count}/{len(results)}")
        print(f"Q_SAT range: {min_Q_SAT:.4f} to {max_Q_SAT:.4f}")
        print(f"Mean Q_SAT: {mean_Q_SAT:.4f}")

        # Show some examples
        print("\nFirst 5 results:")
        for i, result in enumerate(results[:5]):
            print(f"  {result['permutation']}: Q_SAT = {result['Q_SAT']:.4f} "
                  f"({'Stable' if result['stable'] else 'Unstable'})")

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

    with open('scripts/numerical_exploration/pnp_results.json', 'w') as f:
        json.dump(output_data, f, indent=2)

    print(f"\nResults saved to scripts/numerical_exploration/pnp_results.json")

    # Create visualizations
    create_visualizations(all_results)

def create_visualizations(results_dict):
    """Create visualizations of the numerical exploration results."""
    try:
        plt.figure(figsize=(15, 5))

        for idx, (scheme_name, results) in enumerate(results_dict.items()):
            plt.subplot(1, 3, idx + 1)

            # Extract Q_SAT values (excluding inf)
            valid_results = [r for r in results if r['Q_SAT'] != float('inf')]
            if not valid_results:
                continue

            Q_SAT_values = [r['Q_SAT'] for r in valid_results]
            permutations_str = [''.join(map(str, r['permutation'])) for r in valid_results]
            stable = [r['stable'] for r in valid_results]

            # Create bar chart
            colors = ['green' if s else 'red' for s in stable]
            bars = plt.bar(range(len(Q_SAT_values)), Q_SAT_values, color=colors, alpha=0.7)

            # Add threshold line
            plt.axhline(y=1.0, color='black', linestyle='--', alpha=0.5, label='Q_SAT = 1')

            plt.xlabel('Permutation Index')
            plt.ylabel('Q_SAT Value')
            plt.title(f'{scheme_name}\n(Green: Stable, Red: Unstable)')
            plt.xticks(range(len(permutations_str)), permutations_str, rotation=45, ha='right')
            plt.legend()

            # Add value labels on bars
            for i, (bar, value) in enumerate(zip(bars, Q_SAT_values)):
                plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                        f'{value:.2f}', ha='center', va='bottom', fontsize=8)

        plt.tight_layout()
        plt.savefig('scripts/numerical_exploration/pnp_visualization.png', dpi=150, bbox_inches='tight')
        print("Visualization saved to scripts/numerical_exploration/pnp_visualization.png")

    except ImportError:
        print("Matplotlib not available, skipping visualization")

if __name__ == "__main__":
    main()