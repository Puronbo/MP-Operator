#!/usr/bin/env python3
"""
Numerical exploration for HODGE.lean using zero-as-condition perspective.
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

def assign_scheme_a(perm: Tuple[int, ...]) -> Dict[str, int]:
    """
    Assignment Scheme A (from hodge_zero_as_condition_next_steps.tex):
    - griffithsSize = first two digits
    - hodgeSpaceDim = last three digits
    - motivicCohoSize = sum of digits
    - monodromyTrace = (permutation mod 20) - 10
    """
    # Convert permutation to number
    perm_num = int(''.join(map(str, perm)))

    griffithsSize = int(''.join(map(str, perm[:2])))  # First two digits
    hodgeSpaceDim = int(''.join(map(str, perm[2:])))  # Last three digits
    motivicCohoSize = sum(perm)  # Sum of digits
    monodromyTrace = (perm_num % 20) - 10  # Centered around zero

    Q_H = griffithsSize / hodgeSpaceDim if hodgeSpaceDim != 0 else float('inf')

    return {
        'permutation': perm,
        'perm_num': perm_num,
        'griffithsSize': griffithsSize,
        'hodgeSpaceDim': hodgeSpaceDim,
        'motivicCohoSize': motivicCohoSize,
        'monodromyTrace': monodromyTrace,
        'Q_H': Q_H,
        'stable': Q_H < 1,
        'unstable': Q_H >= 1
    }

def assign_scheme_b(perm: Tuple[int, ...]) -> Dict[str, int]:
    """
    Assignment Scheme B (alternative splitting):
    - griffithsSize = first three digits
    - hodgeSpaceDim = last two digits
    """
    griffithsSize = int(''.join(map(str, perm[:3])))  # First three digits
    hodgeSpaceDim = int(''.join(map(str, perm[3:])))  # Last two digits

    # Avoid division by zero
    if hodgeSpaceDim == 0:
        hodgeSpaceDim = 1  # Small default to avoid inf

    Q_H = griffithsSize / hodgeSpaceDim

    return {
        'permutation': perm,
        'griffithsSize': griffithsSize,
        'hodgeSpaceDim': hodgeSpaceDim,
        'Q_H': Q_H,
        'stable': Q_H < 1,
        'unstable': Q_H >= 1
    }

def assign_scheme_c(perm: Tuple[int, ...]) -> Dict[str, int]:
    """
    Assignment Scheme C (using timestamp idea):
    - motivicCohoSize = (product of digits) - (timestamp mod 10)
    - griffithsSize = first two digits
    - hodgeSpaceDim = last three digits
    """
    timestamp = 972555980
    perm_num = int(''.join(map(str, perm)))

    griffithsSize = int(''.join(map(str, perm[:2])))  # First two digits
    hodgeSpaceDim = int(''.join(map(str, perm[2:])))  # Last three digits
    motivicCohoSize = (np.prod(perm)) - (timestamp % 10)
    monodromyTrace = (perm_num % 20) - 10

    Q_H = griffithsSize / hodgeSpaceDim if hodgeSpaceDim != 0 else float('inf')

    return {
        'permutation': perm,
        'perm_num': perm_num,
        'griffithsSize': griffithsSize,
        'hodgeSpaceDim': hodgeSpaceDim,
        'motivicCohoSize': motivicCohoSize,
        'monodromyTrace': monodromyTrace,
        'Q_H': Q_H,
        'stable': Q_H < 1,
        'unstable': Q_H >= 1,
        'motivic_zero': motivicCohoSize == 0
    }

def test_axioms(results: List[Dict]) -> Dict:
    """Test the axioms and derived theorems from the Hodge documents."""
    axioms = {
        'stable_if_Q_H_lt_one': [],
        'unstable_if_Q_H_ge_one': [],
        'motivic_vanishing_controls_Griffiths': [],
        'monodromy_constrains_variation': []
    }

    for result in results:
        # Test stable_if_Q_H_lt_one
        if result['Q_H'] < 1:
            axioms['stable_if_Q_H_lt_one'].append(result)

        # Test unstable_if_Q_H_ge_one
        if result['Q_H'] >= 1:
            axioms['unstable_if_Q_H_ge_one'].append(result)

        # Test motivic_vanishing_controls_Griffiths (if available)
        if 'motivic_zero' in result and result['motivic_zero']:
            axioms['motivic_vanishing_controls_Griffiths'].append(result)

        # Test monodromy_constrains_variation (if available)
        if 'monodromyTrace' in result:
            # Simplified test: if |monodromyTrace| < 10, then expect Q_H < 2
            if abs(result['monodromyTrace']) < 10:
                if result['Q_H'] < 2:
                    axioms['monodromy_constrains_variation'].append(result)

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

        Q_H_values = [r['Q_H'] for r in results if r['Q_H'] != float('inf')]
        if Q_H_values:
            min_Q_H = min(Q_H_values)
            max_Q_H = max(Q_H_values)
            mean_Q_H = np.mean(Q_H_values)
        else:
            min_Q_H = max_Q_H = mean_Q_H = 0

        print(f"Stable (Q_H < 1): {stable_count}/{len(results)}")
        print(f"Unstable (Q_H >= 1): {unstable_count}/{len(results)}")
        print(f"Q_H range: {min_Q_H:.4f} to {max_Q_H:.4f}")
        print(f"Mean Q_H: {mean_Q_H:.4f}")

        # Show some examples
        print("\nFirst 5 results:")
        for i, result in enumerate(results[:5]):
            print(f"  {result['permutation']}: Q_H = {result['Q_H']:.4f} "
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

    with open('scripts/numerical_exploration/hodge_results.json', 'w') as f:
        json.dump(output_data, f, indent=2)

    print(f"\nResults saved to scripts/numerical_exploration/hodge_results.json")

    # Create visualizations
    create_visualizations(all_results)

def create_visualizations(results_dict):
    """Create visualizations of the numerical exploration results."""
    try:
        plt.figure(figsize=(15, 5))

        for idx, (scheme_name, results) in enumerate(results_dict.items()):
            plt.subplot(1, 3, idx + 1)

            # Extract Q_H values (excluding inf)
            valid_results = [r for r in results if r['Q_H'] != float('inf')]
            if not valid_results:
                continue

            Q_H_values = [r['Q_H'] for r in valid_results]
            permutations_str = [''.join(map(str, r['permutation'])) for r in valid_results]
            stable = [r['stable'] for r in valid_results]

            # Create bar chart
            colors = ['green' if s else 'red' for s in stable]
            bars = plt.bar(range(len(Q_H_values)), Q_H_values, color=colors, alpha=0.7)

            # Add threshold line
            plt.axhline(y=1, color='black', linestyle='--', alpha=0.5, label='Q_H = 1')

            plt.xlabel('Permutation Index')
            plt.ylabel('Q_H Value')
            plt.title(f'{scheme_name}\n(Green: Stable, Red: Unstable)')
            plt.xticks(range(len(permutations_str)), permutations_str, rotation=45, ha='right')
            plt.legend()

            # Add value labels on bars
            for i, (bar, value) in enumerate(zip(bars, Q_H_values)):
                plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                        f'{value:.2f}', ha='center', va='bottom', fontsize=8)

        plt.tight_layout()
        plt.savefig('scripts/numerical_exploration/hodge_visualization.png', dpi=150, bbox_inches='tight')
        print("Visualization saved to scripts/numerical_exploration/hodge_visualization.png")

    except ImportError:
        print("Matplotlib not available, skipping visualization")

if __name__ == "__main__":
    main()