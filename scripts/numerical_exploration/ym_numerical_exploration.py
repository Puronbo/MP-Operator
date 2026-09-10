#!/usr/bin/env python3
"""
Numerical exploration for Yang-Mills mass gap using zero-as-condition perspective.
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
    Assignment Scheme A (inspired by MassGap structure and RHData connection):
    - Based on the MassGap.lean file, we connect to RHData where:
      * Virtual sector: Q_RH > 1
      * Physical sector: Q_RH < 1
      * Mass gap point: Q_RH = 1 (where God force balances sectors)
    - We'll create a Q_YM parameter that follows similar logic
    - Using timestamp 972555980 and digits [0,1,2,2,6]

    Scheme A:
    - N = first two digits as integer
    - m = (third digit) * (fourth digit) + (fifth digit)  # modified from RH
    - baseValue = sum of digits / 10.0
    - Q_YM = |(m / (baseValue * N)) - 1| if N > 0 and baseValue > 0 else 1.0
    """
    # Convert permutation to number
    perm_num = int(''.join(map(str, perm)))

    N = int(''.join(map(str, perm[:2])))  # First two digits
    m = perm[2] * perm[3] + perm[4]       # Third * fourth + fifth (modified from RH's subtract)
    baseValue = sum(perm) / 10.0

    # Compute Q_YM analogous to Q_RH = |varianceOfNormalizedGaps - 1|
    if N > 0 and baseValue > 0:
        normalizedValue = m / (baseValue * N)
        Q_YM = abs(normalizedValue - 1.0)
    else:
        Q_YM = 1.0  # Default to mass gap point when undefined

    return {
        'permutation': perm,
        'perm_num': perm_num,
        'N': N,
        'm': m,
        'baseValue': baseValue,
        'normalizedValue': m / (baseValue * N) if N > 0 and baseValue > 0 else 0.0,
        'Q_YM': Q_YM,
        'virtualSector': Q_YM > 1.0,   # Q_YM > 1 -> virtual sector (like Q_RH > 1)
        'physicalSector': Q_YM < 1.0,  # Q_YM < 1 -> physical sector (like Q_RH < 1)
        'massGapPoint': abs(Q_YM - 1.0) < 0.001,  # Approximately Q_YM = 1
        'stable': Q_YM < 1.0,          # Stable when in physical sector
        'unstable': Q_YM >= 1.0        # Unstable when in virtual sector or at boundary
    }

def assign_scheme_b(perm: Tuple[int, ...]) -> Dict[str, float]:
    """
    Assignment Scheme B (alternative splitting with timestamp):
    - N = first three digits as integer
    - m = last two digits as integer
    - baseValue = (product of digits) / 100.0
    - Q_YM = |(m / (baseValue * N)) - 1| if N > 0 and baseValue > 0 else 1.0
    """
    N = int(''.join(map(str, perm[:3])))  # First three digits
    m = int(''.join(map(str, perm[3:])))  # Last two digits
    baseValue = np.prod(perm) / 100.0

    # Compute Q_YM analogous to Q_RH
    if N > 0 and baseValue > 0:
        normalizedValue = m / (baseValue * N)
        Q_YM = abs(normalizedValue - 1.0)
    else:
        Q_YM = 1.0  # Default to mass gap point when undefined

    return {
        'permutation': perm,
        'perm_num': int(''.join(map(str, perm))),
        'N': N,
        'm': m,
        'baseValue': baseValue,
        'normalizedValue': m / (baseValue * N) if N > 0 and baseValue > 0 else 0.0,
        'Q_YM': Q_YM,
        'virtualSector': Q_YM > 1.0,
        'physicalSector': Q_YM < 1.0,
        'massGapPoint': abs(Q_YM - 1.0) < 0.001,
        'stable': Q_YM < 1.0,
        'unstable': Q_YM >= 1.0
    }

def assign_scheme_c(perm: Tuple[int, ...]) -> Dict[str, float]:
    """
    Assignment Scheme C (using timestamp idea with mass gap connection):
    - N = (product of digits) % 1000
    - m = (timestamp % 100)  # last two digits of timestamp
    - baseValue = (sum of digits) / 10.0
    - Q_YM = |(m / (baseValue * N)) - 1| if N > 0 and baseValue > 0 else 1.0
    """
    timestamp = 972555980
    perm_num = int(''.join(map(str, perm)))

    N = np.prod(perm) % 1000
    m = timestamp % 100
    baseValue = sum(perm) / 10.0

    # Compute Q_YM analogous to Q_RH
    if N > 0 and baseValue > 0:
        normalizedValue = m / (baseValue * N)
        Q_YM = abs(normalizedValue - 1.0)
    else:
        Q_YM = 1.0  # Default to mass gap point when undefined

    return {
        'permutation': perm,
        'perm_num': perm_num,
        'N': N,
        'm': m,
        'baseValue': baseValue,
        'normalizedValue': m / (baseValue * N) if N > 0 and baseValue > 0 else 0.0,
        'Q_YM': Q_YM,
        'virtualSector': Q_YM > 1.0,
        'physicalSector': Q_YM < 1.0,
        'massGapPoint': abs(Q_YM - 1.0) < 0.001,
        'stable': Q_YM < 1.0,
        'unstable': Q_YM >= 1.0
    }

def test_axioms(results: List[Dict]) -> Dict:
    """Test the axioms and derived theorems from Yang-Mills mass gap documents."""
    axioms = {
        'stable_if_Q_YM_lt_one': [],
        'unstable_if_Q_YM_ge_one': [],
        'massGap_balance': [],  # God force at mass gap point
        'sector_separation': []  # Virtual and physical sectors are disjoint
    }

    for result in results:
        # Test stable_if_Q_YM_lt_one
        if result['Q_YM'] < 1.0:
            axioms['stable_if_Q_YM_lt_one'].append(result)

        # Test unstable_if_Q_YM_ge_one
        if result['Q_YM'] >= 1.0:
            axioms['unstable_if_Q_YM_ge_one'].append(result)

        # Test massGap_balance (at Q_YM ≈ 1, we should have God force equilibrium)
        if abs(result['Q_YM'] - 1.0) < 0.1:  # Near mass gap point
            # At mass gap: not in virtual sector AND not in physical sector
            if not result['virtualSector'] and not result['physicalSector']:
                axioms['massGap_balance'].append(result)

        # Test sector_separation (virtual and physical sectors should be disjoint)
        if result['virtualSector'] and result['physicalSector']:
            # This should never happen - a point can't be in both sectors
            pass  # Intentionally empty - we want 0 cases here
        else:
            axioms['sector_separation'].append(result)

    return axioms

def main():
    """Main numerical exploration function."""
    digits = [0, 1, 2, 2, 6]
    permutations = generate_permutations(digits)

    print(f"Generated {len(permutations)} permutations of {digits}")
    print("=" * 50)

    # Test each assignment scheme
    schemes = [
        ("Scheme A (inspired by MassGap/RH connection)", assign_scheme_a),
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
        mass_gap_count = sum(1 for r in results if r['massGapPoint'])
        virtual_count = sum(1 for r in results if r['virtualSector'])
        physical_count = sum(1 for r in results if r['physicalSector'])

        Q_YM_values = [r['Q_YM'] for r in results]
        if Q_YM_values:
            min_Q_YM = min(Q_YM_values)
            max_Q_YM = max(Q_YM_values)
            mean_Q_YM = np.mean(Q_YM_values)
        else:
            min_Q_YM = max_Q_YM = mean_Q_YM = 0.0

        print(f"Stable (Q_YM < 1): {stable_count}/{len(results)}")
        print(f"Unstable (Q_YM >= 1): {unstable_count}/{len(results)}")
        print(f"Mass gap points (Q_YM ~ 1): {mass_gap_count}/{len(results)}")
        print(f"Virtual sector (Q_YM > 1): {virtual_count}/{len(results)}")
        print(f"Physical sector (Q_YM < 1): {physical_count}/{len(results)}")
        print(f"Q_YM range: {min_Q_YM:.4f} to {max_Q_YM:.4f}")
        print(f"Mean Q_YM: {mean_Q_YM:.4f}")

        # Show some examples
        print("\nFirst 5 results:")
        for i, result in enumerate(results[:5]):
            sector = ""
            if result['massGapPoint']:
                sector = " [Mass Gap]"
            elif result['virtualSector']:
                sector = " [Virtual]"
            elif result['physicalSector']:
                sector = " [Physical]"
            print(f"  {result['permutation']}: Q_YM = {result['Q_YM']:.4f}{sector}")

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

    with open('scripts/numerical_exploration/ym_results.json', 'w') as f:
        json.dump(output_data, f, indent=2)

    print(f"\nResults saved to scripts/numerical_exploration/ym_results.json")

    # Create visualizations
    create_visualizations(all_results)

def create_visualizations(results_dict):
    """Create visualizations of the numerical exploration results."""
    try:
        plt.figure(figsize=(15, 5))

        for idx, (scheme_name, results) in enumerate(results_dict.items()):
            plt.subplot(1, 3, idx + 1)

            # Extract Q_YM values
            Q_YM_values = [r['Q_YM'] for r in results]
            permutations_str = [''.join(map(str, r['permutation'])) for r in results]
            stable = [r['stable'] for r in results]
            mass_gap = [r['massGapPoint'] for r in results]
            virtual = [r['virtualSector'] for r in results]
            physical = [r['physicalSector'] for r in results]

            # Create color scheme: blue for stable/physical, red for unstable/virtual, green for mass gap
            colors = []
            for i in range(len(results)):
                if mass_gap[i]:
                    colors.append('green')      # Mass gap point
                elif virtual[i]:
                    colors.append('red')        # Virtual sector (unstable)
                else:  # physical[i] and stable[i]
                    colors.append('blue')       # Physical sector (stable)

            # Create bar chart
            bars = plt.bar(range(len(Q_YM_values)), Q_YM_values, color=colors, alpha=0.7)

            # Add threshold lines
            plt.axhline(y=1.0, color='black', linestyle='--', alpha=0.5, label='Q_YM = 1 (Mass Gap)')
            plt.axhline(y=0.0, color='gray', linestyle='-', alpha=0.3, label='Q_YM = 0')

            plt.xlabel('Permutation Index')
            plt.ylabel('Q_YM Value')
            plt.title(f'{scheme_name}\n(Green: Mass Gap, Red: Virtual/Unstable, Blue: Physical/Stable)')
            plt.xticks(range(len(permutations_str)), permutations_str, rotation=45, ha='right')
            plt.legend()

            # Add value labels on bars
            for i, (bar, value) in enumerate(zip(bars, Q_YM_values)):
                plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                        f'{value:.2f}', ha='center', va='bottom', fontsize=8)

        plt.tight_layout()
        plt.savefig('scripts/numerical_exploration/ym_visualization.png', dpi=150, bbox_inches='tight')
        print("Visualization saved to scripts/numerical_exploration/ym_visualization.png")

    except ImportError:
        print("Matplotlib not available, skipping visualization")

if __name__ == "__main__":
    main()