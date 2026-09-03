# Numerical Exploration Files

This directory contains numerical exploration scripts and documentation related to the axiomatic framework connecting the three Millennium Prize Problems through a generalized Toomre Q parameter.

## Files

1. **NUMERICAL_EXPLORATION.md** - Detailed documentation of the numerical exploration approach using:
   - User-provided number sets: {10262, 21026, 22610, 26102}
   - Unix timestamp: 972555980
   - ISO date-time string considerations
   - Permutation generation and analysis
   - Simplified threshold models for each domain
   - Observations about threshold crossing behavior

2. **numerical_exploration.py** - Python script implementing the numerical exploration:
   - Generates all 48 valid permutations of digit set {0,1,2,2,6}
   - Computes simplified Q_NS, Q_YM, and Q_BSD analogs for each permutation
   - Analyzes threshold crossing behavior (Q < 1 vs Q ≥ 1)
   - Provides statistics on stable/unstable predictions across the permutation set
   - Includes detailed analysis of the starting permutation selected by timestamp

## Purpose

These numerical explorations serve to:
1. Build intuition about the sharp threshold phenomenon central to all three Millennium Prize Problems
2. Observe how simplified threshold models behave across the provided number sets
3. Identify patterns that might suggest where genuine mathematical insight is needed
4. Complement the axiomatic Lean 4 formalization with empirical grounding

The numerical work does not replace the need for mathematical insight in proving theorems, but rather helps develop intuition about where such insights might be most profitably applied.

## Key Insights from Numerical Exploration

- **NS Domain**: Q_NS values remained well below 1.0 for all permutations in our simplified model, suggesting smooth dissipation behavior dominates. This highlights the need for more sophisticated modeling of the enstrophy production/dissipation balance.

- **YM Domain**: 93.8% of permutations predicted Q_YM ≥ 1 (unstable/conformal phase), showing how instanton, theta angle, and spectral genus effects can dominate the YM threshold behavior.

- **BSD Domain**: 0% of permutations were predicted stable in our simplified model, indicating how easily the stability conditions (rank=0 ∧ L_val≠0) can be violated in naive formulations.

These observations underscore why genuine mathematical insight is required to replace the axiomatic `sorry` statements with actual theorems - the real mathematical structures contain subtle balances and cancellations that simple numerical models miss.

## Connection to Axiomatic Work

The numerical exploration complements the axiomatic work in:
- **NS.lean**: Where axioms connect Q_NS bounds to smooth/turbulent solutions
- **YM.lean**: Where axioms connect Q_YM bounds to mass gap existence  
- **BSD.lean**: Where axioms connect Q_BSD bounds to stability/Sha finiteness

By examining how the simplified models behave, we gain intuition about where the actual mathematical theories must provide compensating effects to produce the sharp threshold behaviors observed in the real problems.