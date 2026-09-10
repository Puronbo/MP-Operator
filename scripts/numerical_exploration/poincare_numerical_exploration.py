#!/usr/bin/env python3
"""
Numerical exploration for Poincaré Conjecture using zero-as-condition perspective.
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
    Assignment Scheme A (inspired by Poincaré Conjecture structure in POINCARE.lean):
    - Based on the Q_P definition in the file:
      * Q_P = complexity / stabilizing where:
        - complexity = scalarCurvatureIntegral + (surgCount : ℝ) * 10 + (1 / (minVol + 1))
        - stabilizing = entropy + (reducedVolume : ℝ) + (1 / (diam + 1))
    - We'll create analogous quantities using our digits and timestamp

    Scheme A:
    - entropy = first two digits as integer
    - surgCount = third digit
    - minVol = fourth digit
    - diam = fifth digit
    - scalarCurvatureIntegral = (permutation as number) % 100
    - reducedVolume = sum of digits / 10.0
    - Q_P = complexity / stabilizing
    """
    # Convert permutation to number
    perm_num = int(''.join(map(str, perm)))

    entropy = int(''.join(map(str, perm[:2])))  # First two digits
    surgCount = perm[2]                         # Third digit
    minVol = perm[3]                            # Fourth digit
    diam = perm[4]                              # Fifth digit
    scalarCurvatureIntegral = perm_num % 100
    reducedVolume = sum(perm) / 10.0

    # Avoid division by zero in stabilizing term
    if entropy <= 0:
        Q_P = 1.0  # As per the definition in POINCARE.lean
    else:
        complexity = scalarCurvatureIntegral + (surgCount * 10) + (1.0 / (minVol + 1))
        stabilizing = entropy + reducedVolume + (1.0 / (diam + 1))
        Q_P = complexity / stabilizing if stabilizing > 0 else 1.0

    return {
        'permutation': perm,
        'perm_num': perm_num,
        'entropy': entropy,
        'surgCount': surgCount,
        'minVol': minVol,
        'diam': diam,
        'scalarCurvatureIntegral': scalarCurvatureIntegral,
        'reducedVolume': reducedVolume,
        'complexity': entropy > 0 and (scalarCurvatureIntegral + (surgCount * 10) + (1.0 / (minVol + 1))) or 0.0,
        'stabilizing': entropy > 0 and (entropy + reducedVolume + (1.0 / (diam + 1))) or 0.0,
        'Q_P': Q_P,
        'stable': Q_P < 1.0,   # Stable when Q_P < 1 (converges to round sphere)
        'unstable': Q_P >= 1.0 # Unstable when Q_P >= 1 (risk of infinite surgery)
    }

def assign_scheme_b(perm: Tuple[int, ...]) -> Dict[str, float]:
    """
    Assignment Scheme B (alternative splitting):
    - entropy = first three digits as integer
    - surgCount = (fourth digit) * (fifth digit)
    - minVol = (permutation as number) % 10
    - diam = sum of digits
    - scalarCurvatureIntegral = (permutation as number) % 50
    - reducedVolume = product of digits / 100.0
    - Q_P = complexity / stabilizing
    """
    entropy = int(''.join(map(str, perm[:3])))  # First three digits
    surgCount = perm[3] * perm[4]               # Fourth * fifth
    minVol = int(''.join(map(str, perm))) % 10
    diam = sum(perm)
    scalarCurvatureIntegral = int(''.join(map(str, perm))) % 50
    reducedVolume = np.prod(perm) / 100.0

    # Avoid division by zero in stabilizing term
    if entropy <= 0:
        Q_P = 1.0  # As per the definition in POINCARE.lean
    else:
        complexity = scalarCurvatureIntegral + (surgCount * 10) + (1.0 / (minVol + 1))
        stabilizing = entropy + reducedVolume + (1.0 / (diam + 1))
        Q_P = complexity / stabilizing if stabilizing > 0 else 1.0

    return {
        'permutation': perm,
        'perm_num': int(''.join(map(str, perm))),
        'entropy': entropy,
        'surgCount': surgCount,
        'minVol': minVol,
        'diam': diam,
        'scalarCurvatureIntegral': scalarCurvatureIntegral,
        'reducedVolume': reducedVolume,
        'complexity': entropy > 0 and (scalarCurvatureIntegral + (surgCount * 10) + (1.0 / (minVol + 1))) or 0.0,
        'stabilizing': entropy > 0 and (entropy + reducedVolume + (1.0 / (diam + 1))) or 0.0,
        'Q_P': Q_P,
        'stable': Q_P < 1.0,
        'unstable': Q_P >= 1.0
    }

def assign_scheme_c(perm: Tuple[int, ...]) -> Dict[str, float]:
    """
    Assignment Scheme C (using timestamp idea with Poincaré connection):
    - entropy = (product of digits) % 1000
    - surgCount = (timestamp % 100)  # last two digits of timestamp
    - minVol = (sum of digits) % 10
    - diam = (timestamp % 1000)  # last three digits of timestamp
    - scalarCurvatureIntegral = (permutation as number) % 100
    - reducedVolume = (sum of digits) / 10.0
    - Q_P = complexity / stabilizing
    """
    timestamp = 972555980
    perm_num = int(''.join(map(str, perm)))

    entropy = np.prod(perm) % 1000
    surgCount = timestamp % 100
    minVol = sum(perm) % 10
    diam = timestamp % 1000
    scalarCurvatureIntegral = perm_num % 100
    reducedVolume = sum(perm) / 10.0

    # Avoid division by zero in stabilizing term
    if entropy <= 0:
        Q_P = 1.0  # As per the definition in POINCARE.lean
    else:
        complexity = scalarCurvatureIntegral + (surgCount * 10) + (1.0 / (minVol + 1))
        stabilizing = entropy + reducedVolume + (1.0 / (diam + 1))
        Q_P = complexity / stabilizing if stabilizing > 0 else 1.0

    return {
        'permutation': perm,
        'perm_num': perm_num,
        'entropy': entropy,
        'surgCount': surgCount,
        'minVol': minVol,
        'diam': diam,
        'scalarCurvatureIntegral': scalarCurvatureIntegral,
        'reducedVolume': reducedVolume,
        'complexity': entropy > 0 and (scalarCurvatureIntegral + (surgCount * 10) + (1.0 / (minVol + 1))) or 0.0,
        'stabilizing': entropy > 0 and (entropy + reducedVolume + (1.0 / (diam + 1))) or 0.0,
        'Q_P': Q_P,
        'stable': Q_P < 1.0,
        'unstable': Q_P >= 1.0
    }

def test_axioms(results: List[Dict]) -> Dict:
    """Test the axioms and derived theorems from Poincaré Conjecture documents."""
    axioms = {
        'stable_if_Q_P_lt_one': [],
        'unstable_if_Q_P_ge_one': [],
        'noncollapsing_controls_curvature': [],  # If reducedVolume > 0.1 and scalarCurvatureIntegral < 1000, then Q_P < 2
        'canonical_neighborhoods_control_flow': []  # If entropy > 10 and surgCount < 100, then Q_P < 1
    }

    for result in results:
        # Test stable_if_Q_P_lt_one
        if result['Q_P'] < 1.0:
            axioms['stable_if_Q_P_lt_one'].append(result)

        # Test unstable_if_Q_P_ge_one
        if result['Q_P'] >= 1.0:
            axioms['unstable_if_Q_P_ge_one'].append(result)

        # Test noncollapsing_controls_curvature (if reducedVolume > 0.1 and scalarCurvatureIntegral < 1000, then Q_P < 2)
        if result['reducedVolume'] > 0.1 and result['scalarCurvatureIntegral'] < 1000:
            if result['Q_P'] < 2.0:
                axioms['noncollapsing_controls_curvature'].append(result)

        # Test canonical_neighborhoods_control_flow (if entropy > 10 and surgCount < 100, then Q_P < 1)
        if result['entropy'] > 10 and result['surgCount'] < 100:
            if result['Q_P'] < 1.0:
                axioms['canonical_neighborhoods_control_flow'].append(result)

    return axioms

def main():
    """Main numerical exploration function."""
    digits = [0, 1, 2, 2, 6]
    permutations = generate_permutations(digits)

    print(f"Generated {len(permutations)} permutations of {digits}")
    print("=" * 50)

    # Test each assignment scheme
    schemes = [
        ("Scheme A (inspired by POINCARE.lean structure)", assign_scheme_a),
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

        Q_P_values = [r['Q_P'] for r in results]
        if Q_P_values:
            min_Q_P = min(Q_P_values)
            max_Q_P = max(Q_P_values)
            mean_Q_P = np.mean(Q_P_values)
        else:
            min_Q_P = max_Q_P = mean_Q_P = 0.0

        print(f"Stable (Q_P < 1): {stable_count}/{len(results)}")
        print(f"Unstable (Q_P >= 1): {unstable_count}/{len(results)}")
        print(f"Q_P range: {min_Q_P:.4f} to {max_Q_P:.4f}")
        print(f"Mean Q_P: {mean_Q_P:.4f}")

        # Show some examples
        print("\nFirst 5 results:")
        for i, result in enumerate(results[:5]):
            stability = "Stable" if result['stable'] else "Unstable"
            print(f"  {result['permutation']}: Q_P = {result['Q_P']:.4f} [{stability}]")

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

    with open('scripts/numerical_exploration/poincare_results.json', 'w') as f:
        json.dump(output_data, f, indent=2)

    print(f"\nResults saved to scripts/numerical_exploration/poincare_results.json")

    # Create visualizations
    create_visualizations(all_results)

def create_visualizations(results_dict):
    """Create visualizations of the numerical exploration results."""
    try:
        plt.figure(figsize=(15, 5))

        for idx, (scheme_name, results) in enumerate(results_dict.items()):
            plt.subplot(1, 3, idx + 1)

            # Extract Q_P values
            Q_P_values = [r['Q_P'] for r in results]
            permutations_str = [''.join(map(str, r['permutation'])) for r in results]
            stable = [r['stable'] for r in results]

            # Create bar chart
            colors = ['green' if s else 'red' for s in stable]
            bars = plt.bar(range(len(Q_P_values)), Q_P_values, color=colors, alpha=0.7)

            # Add threshold line
            plt.axhline(y=1.0, color='black', linestyle='--', alpha=0.5, label='Q_P = 1')

            plt.xlabel('Permutation Index')
            plt.ylabel('Q_P Value')
            plt.title(f'{scheme_name}\n(Green: Stable (Q_P < 1), Red: Unstable (Q_P >= 1))')
            plt.xticks(range(len(permutations_str)), permutations_str, rotation=45, ha='right')
            plt.legend()

            # Add value labels on bars
            for i, (bar, value) in enumerate(zip(bars, Q_P_values)):
                plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                        f'{value:.2f}', ha='center', va='bottom', fontsize=8)

        plt.tight_layout()
        plt.savefig('scripts/numerical_exploration/poincare_visualization.png', dpi=150, bbox_inches='tight')
        print("Visualization saved to scripts/numerical_exploration/poincare_visualization.png")

    except ImportError:
        print("Matplotlib not available, skipping visualization")

if __name__ == "__main__":
    main()