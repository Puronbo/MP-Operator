#!/usr/bin/env python3
"""
Numerical exploration of the operator framework A_{alpha,beta} = alpha*D + beta*V and its connections
to mass gap, Navier-Stokes Q_NS parameter, and other Millennium Problem frameworks.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict
import json
import itertools

def solve_operator_eigenvalue(alpha: float, beta: float, lambda_val: float) -> Dict:
    """
    Solve the eigenvalue problem for A_{alpha,beta} f = lambda f
    Which leads to: alpha*f'' - lambda*f' + beta*f = 0
    """
    # Characteristic equation: alpha*r^2 - lambda*r + beta = 0
    discriminant = lambda_val**2 - 4*alpha*beta

    if alpha == 0:
        # Degenerate case: -lambda*f' + beta*f = 0
        if lambda_val == 0:
            # beta*f = 0 -> f = constant if beta ≠ 0
            return {
                'type': 'degenerate',
                'discriminant': discriminant,
                'solution_form': 'constant',
                'Q_parameter': float('inf') if beta != 0 else 0
            }
        else:
            # -lambda*f' + beta*f = 0 -> f' = (beta/lambda) f -> f = C*exp((beta/lambda)*x)
            r = beta / lambda_val
            return {
                'type': 'exponential',
                'discriminant': discriminant,
                'roots': [r],
                'solution_form': f'C*exp({r}*x)',
                'Q_parameter': abs(lambda_val)/(2*np.sqrt(alpha*beta)) if alpha*beta > 0 else float('inf')
            }

    # Quadratic case: alpha*r^2 - lambda*r + beta = 0
    r1 = (lambda_val + np.sqrt(discriminant)) / (2*alpha)
    r2 = (lambda_val - np.sqrt(discriminant)) / (2*alpha)

    # Determine solution type based on discriminant
    if discriminant < 0:
        # Underdamped/oscillatory: complex roots
        real_part = lambda_val / (2*alpha)
        imag_part = np.sqrt(-discriminant) / (2*alpha)
        solution_form = f'exp({real_part}*x) * [C1*cos({imag_part}*x) + C2*sin({imag_part}*x)]'
        solution_type = 'underdamped'
    elif discriminant == 0:
        # Critically damped: repeated real root
        r = lambda_val / (2*alpha)
        solution_form = f'(C1 + C2*x)*exp({r}*x)'
        solution_type = 'critically_damped'
    else:
        # Overdamped: distinct real roots
        solution_form = f'C1*exp({r1}*x) + C2*exp({r2}*x)'
        solution_type = 'overdamped'

    # Calculate Q parameter (quality factor) and mass gap connection
    # From the mass gap connection: Q = 1 when Delta = 0
    # Q_parameter = sqrt(alpha*beta)/|lambda| (for lambda ≠ 0)
    if lambda_val != 0 and alpha*beta > 0:
        Q_parameter = np.sqrt(alpha*beta) / abs(lambda_val)
    else:
        Q_parameter = float('inf')

    # Mass gap condition: Q = 1 <=> Delta = 0
    mass_gap_condition = abs(discriminant) < 1e-10

    return {
        'type': 'standard',
        'discriminant': discriminant,
        'solution_type': solution_type,
        'solution_form': solution_form,
        'roots': [r1, r2] if discriminant >= 0 else [complex(r1, r2), complex(r1, -r2)],
        'Q_parameter': Q_parameter,
        'mass_gap_condition': mass_gap_condition,
        'damping_ratio': abs(lambda_val)/(2*np.sqrt(alpha*beta)) if alpha*beta > 0 else float('inf')
    }

def explore_parameter_space():
    """Explore the parameter space of alpha, beta, lambda to understand the operator behavior."""
    print("Exploring operator framework parameter space...")
    print("=" * 60)

    # Parameter ranges
    alpha_vals = [0.5, 1.0, 2.0]  # mass/spring constant analogues
    beta_vals = [0.5, 1.0, 2.0]   # spring constant/mass analogues
    lambda_vals = [-3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0]  # damping coefficient analogues

    results = []

    for alpha in alpha_vals:
        for beta in beta_vals:
            for lambda_val in lambda_vals:
                result = solve_operator_eigenvalue(alpha, beta, lambda_val)
                result['alpha'] = alpha
                result['beta'] = beta
                result['lambda'] = lambda_val
                results.append(result)

                # Print key findings
                if result['mass_gap_condition']:
                    print(f"MASS GAP FOUND: alpha={alpha}, beta={beta}, lambda={lambda_val}")
                    print(f"  Discriminant: {result['discriminant']:.6f}")
                    print(f"  Q_parameter: {result['Q_parameter']:.6f}")
                    print(f"  Solution type: {result['solution_type']}")
                    print()

    # Analyze results
    mass_gap_cases = [r for r in results if r['mass_gap_condition']]
    underdamped_cases = [r for r in results if r['solution_type'] == 'underdamped']
    critically_damped_cases = [r for r in results if r['solution_type'] == 'critically_damped']
    overdamped_cases = [r for r in results if r['solution_type'] == 'overdamped']

    print(f"Parameter space exploration results:")
    print(f"  Total cases: {len(results)}")
    print(f"  Mass gap cases (Delta=0): {len(mass_gap_cases)}")
    print(f"  Underdamped (Delta<0): {len(underdamped_cases)}")
    print(f"  Critically damped (Delta=0): {len(critically_damped_cases)}")
    print(f"  Overdamped (Delta>0): {len(overdamped_cases)}")
    print()

    # Show some examples of each type
    print("Examples:")
    print("Underdamped (oscillatory) examples:")
    for r in underdamped_cases[:3]:
        print(f"  alpha={r['alpha']}, beta={r['beta']}, lambda={r['lambda']}: "
              f"Delta={r['discriminant']:.3f}, Q={r['Q_parameter']:.3f}")

    print("\nCritically damped (mass gap) examples:")
    for r in critically_damped_cases[:3]:
        print(f"  alpha={r['alpha']}, beta={r['beta']}, lambda={r['lambda']}: "
              f"Delta={r['discriminant']:.6f}, Q={r['Q_parameter']:.6f}")

    print("\nOverdamped examples:")
    for r in overdamped_cases[:3]:
        print(f"  alpha={r['alpha']}, beta={r['beta']}, lambda={r['lambda']}: "
              f"Delta={r['discriminant']:.3f}, Q={r['Q_parameter']:.3f}")

    return results

def visualize_operator_behavior():
    """Create visualizations of the operator behavior across parameter space."""
    print("\nCreating visualizations...")

    # Fix two parameters and vary the third
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # Plot 1: Vary lambda for fixed alpha, beta
    alpha, beta = 1.0, 1.0
    lambda_range = np.linspace(-5, 5, 100)
    discriminants = []
    Q_params = []

    for lambda_val in lambda_range:
        result = solve_operator_eigenvalue(alpha, beta, lambda_val)
        discriminants.append(result['discriminant'])
        Q_params.append(result['Q_parameter'] if result['Q_parameter'] != float('inf') else 10)

    axes[0,0].plot(lambda_range, discriminants, 'b-', linewidth=2, label='Discriminant Delta = lambda^2 - 4*alpha*beta')
    axes[0,0].axhline(y=0, color='k', linestyle='--', alpha=0.7, label='Delta = 0 (Mass Gap)')
    axes[0,0].set_xlabel('lambda (damping coefficient)')
    axes[0,0].set_ylabel('Discriminant Delta')
    axes[0,0].set_title(f'Discriminant vs lambda (alpha={alpha}, beta={beta})')
    axes[0,0].legend()
    axes[0,0].grid(True, alpha=0.3)

    axes[0,1].plot(lambda_range, Q_params, 'r-', linewidth=2, label='Q Parameter = sqrt(alpha*beta)/|lambda|')
    axes[0,1].axhline(y=1, color='k', linestyle='--', alpha=0.7, label='Q = 1 (Mass Gap)')
    axes[0,1].set_xlabel('lambda (damping coefficient)')
    axes[0,1].set_ylabel('Q Parameter')
    axes[0,1].set_title(f'Q Parameter vs lambda (alpha={alpha}, beta={beta})')
    axes[0,1].legend()
    axes[0,1].grid(True, alpha=0.3)

    # Plot 2: Vary alpha for fixed beta, lambda
    beta, lambda_val = 1.0, 0.5
    alpha_range = np.linspace(0.1, 3, 100)
    discriminants_alpha = []
    Q_params_alpha = []

    for alpha_val in alpha_range:
        result = solve_operator_eigenvalue(alpha_val, beta, lambda_val)
        discriminants_alpha.append(result['discriminant'])
        Q_params_alpha.append(result['Q_parameter'] if result['Q_parameter'] != float('inf') else 10)

    axes[1,0].plot(alpha_range, discriminants_alpha, 'g-', linewidth=2, label='Discriminant Delta = lambda^2 - 4*alpha*beta')
    axes[1,0].axhline(y=0, color='k', linestyle='--', alpha=0.7, label='Delta = 0 (Mass Gap)')
    axes[1,0].set_xlabel('alpha (mass/spring constant)')
    axes[1,0].set_ylabel('Discriminant Delta')
    axes[1,0].set_title(f'Discriminant vs alpha (beta={beta}, lambda={lambda_val})')
    axes[1,0].legend()
    axes[1,0].grid(True, alpha=0.3)

    axes[1,1].plot(alpha_range, Q_params_alpha, 'm-', linewidth=2, label='Q Parameter = sqrt(alpha*beta)/|lambda|')
    axes[1,1].axhline(y=1, color='k', linestyle='--', alpha=0.7, label='Q = 1 (Mass Gap)')
    axes[1,1].set_xlabel('alpha (mass/spring constant)')
    axes[1,1].set_ylabel('Q Parameter')
    axes[1,1].set_title(f'Q Parameter vs alpha (beta={beta}, lambda={lambda_val})')
    axes[1,1].legend()
    axes[1,1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('scripts/numerical_exploration/operator_framework_visualization.png',
                dpi=150, bbox_inches='tight')
    print("Visualization saved to scripts/numerical_exploration/operator_framework_visualization.png")

    return fig

def explore_mass_gap_connection():
    """Explore the specific connection to mass gap framework as described in MASS_GAP_CONNECTION.md"""
    print("\nExploring mass gap connection...")
    print("=" * 50)

    # Based on the mass gap connection document:
    # Delta = lambda^2 - 4*alpha*beta = 0 <-> Q = 1
    # Where Q parameter from mass gap framework is: Q = (|lambda|/2 + nu) / (sqrt(alpha*beta) + nu)

    alpha, beta = 1.0, 1.0  # Fixed for simplicity
    nu_vals = [0.0, 0.1, 0.5, 1.0, 2.0]  # Viscosity values
    lambda_range = np.linspace(0, 4, 100)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    for nu in nu_vals:
        Q_mass_gap = []
        discriminant_vals = []

        for lambda_val in lambda_range:
            # Mass gap framework Q parameter: Q = (|lambda|/2 + nu) / (sqrt(alpha*beta) + nu)
            Q_mg = (lambda_val/2 + nu) / (np.sqrt(alpha*beta) + nu)
            Q_mass_gap.append(Q_mg)

            # Operator framework discriminant
            discriminant = lambda_val**2 - 4*alpha*beta
            discriminant_vals.append(discriminant)

        # Find where Q_mg = 1 (mass gap condition)
        Q_mg_array = np.array(Q_mass_gap)
        mass_gap_lambda = lambda_range[np.argmin(np.abs(Q_mg_array - 1))]

        axes[0].plot(lambda_range, discriminant_vals,
                    label=f'nu={nu}', linewidth=2)
        axes[1].plot(lambda_range, Q_mass_gap,
                    label=f'nu={nu}', linewidth=2)

    # Add reference lines
    axes[0].axhline(y=0, color='k', linestyle='--', alpha=0.7, label='Delta = 0')
    axes[0].axvline(x=2*np.sqrt(alpha*beta), color='k', linestyle=':', alpha=0.7,
                   label=f'lambda = 2*sqrt(alpha*beta) = {2*np.sqrt(alpha*beta):.2f}')

    axes[1].axhline(y=1, color='k', linestyle='--', alpha=0.7, label='Q = 1')
    axes[1].axvline(x=2*np.sqrt(alpha*beta), color='k', linestyle=':', alpha=0.7,
                   label=f'lambda = 2*sqrt(alpha*beta) = {2*np.sqrt(alpha*beta):.2f}')

    axes[0].set_xlabel('lambda')
    axes[0].set_ylabel('Discriminant Delta = lambda^2 - 4*alpha*beta')
    axes[0].set_title('Mass Gap Connection: Discriminant vs lambda')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    axes[1].set_xlabel('lambda')
    axes[1].set_ylabel('Q Parameter (Mass Gap Framework)')
    axes[1].set_title('Mass Gap Connection: Q vs lambda')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('scripts/numerical_exploration/mass_gap_connection_visualization.png',
                dpi=150, bbox_inches='tight')
    print("Mass gap connection visualization saved to scripts/numerical_exploration/mass_gap_connection_visualization.png")

    # Print key insights
    print(f"For alpha={alpha}, beta={beta}:")
    print(f"  sqrt(alpha*beta) = {np.sqrt(alpha*beta):.3f}")
    print(f"  Mass gap condition (Delta=0) occurs at lambda = +/-2*sqrt(alpha*beta) = +/-{2*np.sqrt(alpha*beta):.3f}")
    print(f"  At mass gap: Q_parameter = sqrt(alpha*beta)/|lambda| = {np.sqrt(alpha*beta)/(2*np.sqrt(alpha*beta)):.3f}")
    print()

def explore_navier_stokes_connection():
    """Explore the connection to Navier-Stokes Q_NS parameter."""
    print("Exploring Navier-Stokes Q_NS connection...")
    print("=" * 50)

    # Based on the NS connection:
    # Q_NS(j) ≈ I_j / (R_j + 1) where I_j is energy flux, R_j is dissipation
    # Reflection effective when R_j > I_j ⟺ Q_NS(j) < 1

    # Simulate scale-dependent quantities
    scales = np.arange(0, 10, 0.5)  # Scale index j

    # Simulate energy flux and dissipation with some turbulence characteristics
    np.random.seed(42)  # For reproducibility

    # Energy flux: typically decreases with scale in inertial range
    energy_flux = np.exp(-scales/3) + 0.1*np.random.randn(len(scales))
    energy_flux = np.maximum(energy_flux, 0.01)  # Ensure positive

    # Dissipation: increases with scale (more dissipation at smaller scales)
    dissipation = 1 - np.exp(-scales/2) + 0.05*np.random.randn(len(scales))
    dissipation = np.maximum(dissipation, 0.01)  # Ensure positive

    # Calculate Q_NS parameter
    Q_NS = energy_flux / (dissipation + 1)  # Following the formula from the document

    # Determine where reflection is effective (Q_NS < 1)
    effective_reflection = Q_NS < 1

    # Create visualization
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # Plot 1: Energy flux and dissipation
    axes[0,0].plot(scales, energy_flux, 'b-', linewidth=2, label='Energy Flux I_j')
    axes[0,0].plot(scales, dissipation, 'r-', linewidth=2, label='Dissipation R_j')
    axes[0,0].set_xlabel('Scale j')
    axes[0,0].set_ylabel('Magnitude')
    axes[0,0].set_title('Scale-Dependent Energy Flux and Dissipation')
    axes[0,0].legend()
    axes[0,0].grid(True, alpha=0.3)

    # Plot 2: Q_NS parameter
    axes[0,1].plot(scales, Q_NS, 'g-', linewidth=2, label='Q_NS(j)')
    axes[0,1].axhline(y=1, color='k', linestyle='--', alpha=0.7, label='Q_NS = 1')
    axes[0,1].fill_between(scales, 0, Q_NS, where=(Q_NS < 1), alpha=0.3, color='green',
                          label='Effective Reflection (Q_NS < 1)')
    axes[0,1].fill_between(scales, Q_NS, 2, where=(Q_NS >= 1), alpha=0.3, color='red',
                          label='Ineffective Reflection (Q_NS ≥ 1)')
    axes[0,1].set_xlabel('Scale j')
    axes[0,1].set_ylabel('Q_NS Parameter')
    axes[0,1].set_title('Navier-Stokes Q_NS Parameter')
    axes[0,1].legend()
    axes[0,1].grid(True, alpha=0.3)

    # Plot 3: Reflection effectiveness
    effectiveness = dissipation / (energy_flux + dissipation)  # From the document
    axes[1,0].plot(scales, effectiveness, 'm-', linewidth=2, label='Effectiveness R_j/(I_j+R_j)')
    axes[1,0].axhline(y=0.5, color='k', linestyle='--', alpha=0.7, label='50% Effectiveness')
    axes[1,0].set_xlabel('Scale j')
    axes[1,0].set_ylabel('Effectiveness')
    axes[1,0].set_title('Reflection Map Effectiveness')
    axes[1,0].legend()
    axes[1,0].grid(True, alpha=0.3)

    # Plot 4: Connection to operator framework
    # Show how Q_NS relates to the operator framework discriminant
    # For a given scale, we can map to operator parameters
    alpha_ns = 1.0  # Fixed "mass" parameter
    beta_ns = 1.0   # Fixed "spring constant" parameter

    # Map Q_NS to effective lambda in operator framework
    # From mass gap connection: Q = sqrt(alpha*beta)/|lambda| <==> |lambda| = sqrt(alpha*beta)/Q
    lambda_effective = np.sqrt(alpha_ns*beta_ns) / Q_NS
    discriminant_ns = lambda_effective**2 - 4*alpha_ns*beta_ns

    axes[1,1].plot(scales, discriminant_ns, 'c-', linewidth=2, label='Discriminant Delta = lambda^2 - 4*alpha*beta')
    axes[1,1].axhline(y=0, color='k', linestyle='--', alpha=0.7, label='Delta = 0 (Mass Gap)')
    axes[1,1].fill_between(scales, discriminant_ns, 0, where=(discriminant_ns < 0), alpha=0.3, color='blue',
                          label='Underdamped (Delta < 0)')
    axes[1,1].fill_between(scales, discriminant_ns, 0, where=(discriminant_ns > 0), alpha=0.3, color='red',
                          label='Overdamped (Delta > 0)')
    axes[1,1].set_xlabel('Scale j')
    axes[1,1].set_ylabel('Discriminant Delta')
    axes[1,1].set_title('Operator Framework Discriminant by Scale')
    axes[1,1].legend()
    axes[1,1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('scripts/numerical_exploration/navier_stokes_connection_visualization.png',
                dpi=150, bbox_inches='tight')
    print("Navier-Stokes connection visualization saved to scripts/numerical_exploration/navier_stokes_connection_visualization.png")

    # Print summary statistics
    print(f"Navier-Stokes connection summary:")
    print(f"  Average Q_NS: {np.mean(Q_NS):.3f}")
    print(f"  Percentage of scales with effective reflection (Q_NS < 1): {np.mean(effective_reflection)*100:.1f}%")
    print(f"  Average effectiveness: {np.mean(effectiveness):.3f}")
    print(f"  Number of mass gap crossings (Delta=0): {np.sum(np.diff(np.sign(discriminant_ns)) != 0)}")
    print()

def main():
    """Main exploration function."""
    print("Operator Framework Numerical Exploration")
    print("=" * 50)

    # Run all explorations
    results = explore_parameter_space()
    visualize_operator_behavior()
    explore_mass_gap_connection()
    explore_navier_stokes_connection()

    # Save results for further analysis
    output_data = {
        'parameter_exploration': results,
        'exploration_timestamp': str(np.datetime64('now')),
        'notes': 'Numerical exploration of operator framework and connections to mass gap and Navier-Stokes'
    }

    # Convert numpy types for JSON serialization
    def convert_for_json(obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.complexfloating):
            return {'real': obj.real, 'imag': obj.imag}
        elif isinstance(obj, complex):
            return {'real': obj.real, 'imag': obj.imag}
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {key: convert_for_json(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [convert_for_json(item) for item in obj]
        else:
            return obj

    output_data_converted = convert_for_json(output_data)

    with open('scripts/numerical_exploration/operator_framework_results.json', 'w') as f:
        json.dump(output_data_converted, f, indent=2)

    print(f"\nDetailed results saved to scripts/numerical_exploration/operator_framework_results.json")
    print("Exploration complete!")

if __name__ == "__main__":
    main()