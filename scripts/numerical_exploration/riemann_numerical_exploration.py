#!/usr/bin/env python3
"""
Numerical exploration for Riemann Hypothesis using zero-as-condition perspective.
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
    Assignment Scheme A (inspired by RHData structure):
    - N = first two digits as integer
    - pairCorrSum = (third digit) * (fourth digit) - (fifth digit)
    - logDensity = sum of digits / 10.0
    - primeSum = (permutation as number) % 100
    - operatorTrace = (permutation as number) % 10 - 5  # centered around zero
    - higherCorr = 0.0
    - electricDensity = 0.0
    - magneticDensity = 0.0
    - varianceOfNormalizedGaps = (pairCorrSum / (logDensity * N)) if N > 0 and logDensity > 0 else 0.0
    """
    # Convert permutation to number
    perm_num = int(''.join(map(str, perm)))

    N = int(''.join(map(str, perm[:2])))  # First two digits
    pairCorrSum = perm[2] * perm[3] - perm[4]  # Third * fourth - fifth
    logDensity = sum(perm) / 10.0
    primeSum = perm_num % 100
    operatorTrace = (perm_num % 10) - 5
    higherCorr = 0.0
    electricDensity = 0.0
    magneticDensity = 0.0

    # Compute varianceOfNormalizedGaps from pairCorrSum, logDensity, and N
    if N > 0 and logDensity > 0:
        varianceOfNormalizedGaps = pairCorrSum / (logDensity * N)
    else:
        varianceOfNormalizedGaps = 0.0

    Q_RH = abs(varianceOfNormalizedGaps - 1.0)

    return {
        'permutation': perm,
        'perm_num': perm_num,
        'N': N,
        'pairCorrSum': pairCorrSum,
        'logDensity': logDensity,
        'primeSum': primeSum,
        'operatorTrace': operatorTrace,
        'higherCorr': higherCorr,
        'electricDensity': electricDensity,
        'magneticDensity': magneticDensity,
        'varianceOfNormalizedGaps': varianceOfNormalizedGaps,
        'Q_RH': Q_RH,
        'stable': Q_RH < 1.0,
        'unstable': Q_RH >= 1.0
    }

def assign_scheme_b(perm: Tuple[int, ...]) -> Dict[str, float]:
    """
    Assignment Scheme B (alternative splitting):
    - N = first three digits
    - pairCorrSum = last two digits as integer
    - logDensity = (product of digits) / 100.0
    - primeSum = sum of digits
    - operatorTrace = ( permutation as number ) % 20 - 10
    - higherCorr = 0.0
    - electricDensity = 0.0
    - magneticDensity = 0.0
    - varianceOfNormalizedGaps = pairCorrSum / (logDensity * N) if N > 0 and logDensity > 0 else 0.0
    """
    N = int(''.join(map(str, perm[:3])))  # First three digits
    pairCorrSum = int(''.join(map(str, perm[3:])))  # Last two digits
    logDensity = np.prod(perm) / 100.0
    primeSum = sum(perm)
    operatorTrace = (int(''.join(map(str, perm))) % 20) - 10
    higherCorr = 0.0
    electricDensity = 0.0
    magneticDensity = 0.0

    if N > 0 and logDensity > 0:
        varianceOfNormalizedGaps = pairCorrSum / (logDensity * N)
    else:
        varianceOfNormalizedGaps = 0.0

    Q_RH = abs(varianceOfNormalizedGaps - 1.0)

    return {
        'permutation': perm,
        'N': N,
        'pairCorrSum': pairCorrSum,
        'logDensity': logDensity,
        'primeSum': primeSum,
        'operatorTrace': operatorTrace,
        'higherCorr': higherCorr,
        'electricDensity': electricDensity,
        'magneticDensity': magneticDensity,
        'varianceOfNormalizedGaps': varianceOfNormalizedGaps,
        'Q_RH': Q_RH,
        'stable': Q_RH < 1.0,
        'unstable': Q_RH >= 1.0
    }

def assign_scheme_c(perm: Tuple[int, ...]) -> Dict[str, float]:
    """
    Assignment Scheme C (using timestamp idea):
    - N = (product of digits) % 1000
    - pairCorrSum = (timestamp % 100)  # last two digits of timestamp
    - logDensity = (sum of digits) / 10.0
    - primeSum = (timestamp % 1000)  # last three digits of timestamp
    - operatorTrace = ( (permutation as number) + timestamp ) % 10 - 5
    - higherCorr = 0.0
    - electricDensity = 0.0
    - magneticDensity = 0.0
    - varianceOfNormalizedGaps = pairCorrSum / (logDensity * N) if N > 0 and logDensity > 0 else 0.0
    """
    timestamp = 972555980
    perm_num = int(''.join(map(str, perm)))

    N = np.prod(perm) % 1000
    pairCorrSum = timestamp % 100
    logDensity = sum(perm) / 10.0
    primeSum = timestamp % 1000
    operatorTrace = (perm_num + timestamp) % 10 - 5
    higherCorr = 0.0
    electricDensity = 0.0
    magneticDensity = 0.0

    if N > 0 and logDensity > 0:
        varianceOfNormalizedGaps = pairCorrSum / (logDensity * N)
    else:
        varianceOfNormalizedGaps = 0.0

    Q_RH = abs(varianceOfNormalizedGaps - 1.0)

    return {
        'permutation': perm,
        'perm_num': perm_num,
        'N': N,
        'pairCorrSum': pairCorrSum,
        'logDensity': logDensity,
        'primeSum': primeSum,
        'operatorTrace': operatorTrace,
        'higherCorr': higherCorr,
        'electricDensity': electricDensity,
        'magneticDensity': magneticDensity,
        'varianceOfNormalizedGaps': varianceOfNormalizedGaps,
        'Q_RH': Q_RH,
        'stable': Q_RH < 1.0,
        'unstable': Q_RH >= 1.0
    }

def test_axioms(results: List[Dict]) -> Dict:
    """Test the axioms and derived theorems from the Riemann Hypothesis documents."""
    axioms = {
        'stable_if_Q_RH_lt_one': [],
        'unstable_if_Q_RH_ge_one': [],
        'prime_sum_controlled': [],
        'hilbert_polya_connection': []
    }

    for result in results:
        # Test stable_if_Q_RH_lt_one
        if result['Q_RH'] < 1.0:
            axioms['stable_if_Q_RH_lt_one'].append(result)

        # Test unstable_if_Q_RH_ge_one
        if result['Q_RH'] >= 1.0:
            axioms['unstable_if_Q_RH_ge_one'].append(result)

        # Test prime_sum_controlled (if primeSum < 1000, then Q_RH < 2)
        if result['primeSum'] < 1000:
            if result['Q_RH'] < 2.0:
                axioms['prime_sum_controlled'].append(result)

        # Test hilbert_polya_connection (if operatorTrace == 0, then Q_RH == 1)
        if result['operatorTrace'] == 0:
            # We expect Q_RH to be close to 1, but due to discretization we check if it's near 1
            if abs(result['Q_RH'] - 1.0) < 0.1:  # tolerance
                axioms['hilbert_polya_connection'].append(result)

    return axioms

def main():
    """Main numerical exploration function."""
    digits = [0, 1, 2, 2, 6]
    permutations = generate_permutations(digits)

    print(f"Generated {len(permutations)} permutations of {digits}")
    print("=" * 50)

    # Test each assignment scheme
    schemes = [
        ("Scheme A (inspired by RHData)", assign_scheme_a),
        ("Scheme B (alternative splitting)", assign_scheme_b),
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

        Q_RH_values = [r['Q_RH'] for r in results]
        if Q_RH_values:
            min_Q_RH = min(Q_RH_values)
            max_Q_RH = max(Q_RH_values)
            mean_Q_RH = np.mean(Q_RH_values)
        else:
            min_Q_RH = max_Q_RH = mean_Q_RH = 0.0

        print(f"Stable (Q_RH < 1): {stable_count}/{len(results)}")
        print(f"Unstable (Q_RH >= 1): {unstable_count}/{len(results)}")
        print(f"Q_RH range: {min_Q_RH:.4f} to {max_Q_RH:.4f}")
        print(f"Mean Q_RH: {mean_Q_RH:.4f}")

        # Show some examples
        print("\nFirst 5 results:")
        for i, result in enumerate(results[:5]):
            print(f"  {result['permutation']}: Q_RH = {result['Q_RH']:.4f} "
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

    with open('scripts/numerical_exploration/riemann_results.json', 'w') as f:
        json.dump(output_data, f, indent=2)

    print(f"\nResults saved to scripts/numerical_exploration/riemann_results.json")

    # Create visualizations
    create_visualizations(all_results)

def create_visualizations(results_dict):
    """Create visualizations of the numerical exploration results."""
    try:
        plt.figure(figsize=(15, 5))

        for idx, (scheme_name, results) in enumerate(results_dict.items()):
            plt.subplot(1, 3, idx + 1)

            # Extract Q_RH values
            Q_RH_values = [r['Q_RH'] for r in results]
            permutations_str = [''.join(map(str, r['permutation'])) for r in results]
            stable = [r['stable'] for r in results]

            # Create bar chart
            colors = ['green' if s else 'red' for s in stable]
            bars = plt.bar(range(len(Q_RH_values)), Q_RH_values, color=colors, alpha=0.7)

            # Add threshold line
            plt.axhline(y=1.0, color='black', linestyle='--', alpha=0.5, label='Q_RH = 1')

            plt.xlabel('Permutation Index')
            plt.ylabel('Q_RH Value')
            plt.title(f'{scheme_name}\n(Green: Stable, Red: Unstable)')
            plt.xticks(range(len(permutations_str)), permutations_str, rotation=45, ha='right')
            plt.legend()

            # Add value labels on bars
            for i, (bar, value) in enumerate(zip(bars, Q_RH_values)):
                plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                        f'{value:.2f}', ha='center', va='bottom', fontsize=8)

        plt.tight_layout()
        plt.savefig('scripts/numerical_exploration/riemann_visualization.png', dpi=150, bbox_inches='tight')
        print("Visualization saved to scripts/numerical_exploration/riemann_visualization.png")

    except ImportError:
        print("Matplotlib not available, skipping visualization")

if __name__ == "__main__":
    main()