# Concrete Research Directions for PNP.lean using Zero-as-Condition Perspective

## Overview
This document develops specific, actionable research directions for transforming the axiomatic assumptions in PNP.lean into proven theorems by applying the 'zero-as-condition' perspective. Each sorry statement is analyzed to identify what computational 'zero' represents, the state space where this condition lives, evolution equations, and concrete mathematical estimates needed.

---

## 1. stable_if_Q_SAT_lt_one

**Axiom**: If Q_SAT < 1 then Stable ens (typical instances easy)

### Zero-as-Condition Analysis
- **Apparent 'zero'**: The condition where the *unsatisfiability probability* is zero (or exponentially small in n)
- **Computational meaning**: Below the satisfiability threshold (α < α_c), random k-SAT formulas are satisfiable with high probability, and typically easy to solve by local search algorithms like unit propagation
- **State space**: Ensemble of random k-SAT formulas with clause density α ∈ [0, α_c), where α_c is the critical threshold
- **Evolution equation**: As α increases from 0 to α_c:
  - Solution space remains connected and expansive
  - Clause-variable factor graph remains tree-like with high probability
  - Survey propagation messages converge to trivial fixed point (all messages equal)
  - The evolution of solution space geometry follows: 
    ```
    d/dα [log(#solutions)] = -n * 𝔼[∂log Z/∂α] 
    ```
    where Z is the partition function, remaining positive and O(2^n) throughout this phase

### Concrete Estimates Needed
To prove this axiom, we need:
1. **Sharp threshold location**: Rigorous bounds on α_c(k) for k≥3
   - Current best: 2^k ln 2 - O(k) ≤ α_c ≤ 2^k ln 2 - (1+o(1)) ln k
   - Need: α_c(k) = 2^k ln 2 - (1/2) ln k + O(1) (sharp threshold conjecture)

2. **Algorithmic easiness proof**: 
   - For α < α_c - ε, unit propagation finds a solution in O(n) time with probability 1 - e^(-Ω(n))
   - Key inequality: Probability of encountering a contradiction during unit propagation < e^(-c(α_c - α)n) for some c>0

3. **Solution space connectivity**:
   - Below threshold, solution space forms a single giant cluster
   - Hamming distance between solutions concentrates around n/2
   - Need: Expansion property of solution space graph

### Numerical Exploration Initial Conditions
- **Random seed**: Use timestamp (2026-08-28) mod large prime as seed for SAT formula generation
- **Clause density values**: α ∈ {0.1, 0.2, ..., 0.95} × α_c_estimate(k) for k=3,4,5
- **Number sets**: Use {n | n = 2^k, k=10..20} for finite-size scaling analysis

---

## 2. unstable_if_Q_SAT_ge_one

**Axiom**: If Q_SAT ≥ 1 then Unstable ens (typical instances hard)

### Zero-as-Condition Analysis
- **Apparent 'zero'**: The condition where the *solution count* is zero (or exponentially small in n)
- **Computational meaning**: At or above the satisfiability threshold (α ≥ α_c), random k-SAT formulas are unsatisfiable with high probability, and refutation requires super-polynomial time for resolution-based algorithms
- **State space**: Ensemble of random k-SAT formulas with clause density α ∈ [α_c, ∞)
- **Evolution equation**: As α increases past α_c:
  ```
  d/dα [log(#solutions)] = -n * 𝔼[∂log Z/∂α] → -∞ as α → α_c+
  ```
  The solution count undergoes a discontinuous jump from exponential to zero at α_c (for k≥3)
  - Order parameter: 𝔼[#solutions] = 2^n (1 - α/2^k)^m → 0 at α_c = 2^k ln 2

### Concrete Estimates Needed
To prove this axiom, we need:
1. **Unsatisfiability proof**: 
   - For α > α_c + ε, Prob[formula is satisfiable] ≤ e^(-Ω(n))
   - Key inequality: Using first moment method, 𝔼[#solutions] = 2^n (1 - 2^-k)^(αn) < e^(-δn) for δ>0 when α > α_c

2. **Refutation hardness**:
   - Resolution width required to refute random k-SAT at density α is Ω(n) for α > α_c
   - Key inequality: Width(refutation) ≥ c(α - α_c)n for some c>0 (Ben-Sasson-Wigderson style bound)

3. **Proof complexity lower bound**:
   - For α > α_c, any resolution refutation requires size exp(Ω(n))
   - Need: Strong exponential separation between SAT and UNSAT instances near threshold

### Numerical Exploration Initial Conditions
- **Random seed**: Use (timestamp + 1) mod large prime to avoid correlation with previous exploration
- **Clause density values**: α ∈ {1.0, 1.05, 1.1, ..., 2.0} × α_c_estimate(k)
- **Number sets**: Use {n | n = 100 * k, k=10..50} to observe scaling behavior

---

## 3. hardness_affects_Q

**Axiom**: If hardness > 100 then Q_SAT > 0.5

### Zero-as-Condition Analysis
- **Apparent 'zero'**: The condition where *resolution width* is zero (trivial refutation possible)
- **Computational meaning**: Even well below threshold, high hardness (large resolution width) indicates proximity to the critical region where solution space begins to deteriorate
- **State space**: Ensemble of random k-SAT formulas where hardness measure (e.g., expected resolution width) exceeds a constant threshold
- **Evolution equation**: As hardness increases from 0:
  ```
  d/d(hardness) [Q_SAT] > 0
  ```
  Hardness and Q_SAT are positively correlated; increasing hardness indicates movement toward the threshold

### Concrete Estimates Needed
To prove this axiom, we need:
1. **Hardness-Q_SAT relationship**:
   - Establish lower bound: hardness ≥ f(Q_SAT) for some increasing function f
   - Specifically: hardness > 100 ⇒ Q_SAT > 0.5
   - Based on: Expected resolution width w(α) ~ g(α_c - α)^(-ν) as α → α_c-
   
2. **Concrete inequality**:
   - Need to show: If w(α) > 100, then α/α_c > 0.5
   - Equivalent: α_c - α < α_c * [1 - (C/100)^(1/ν)] for constants C, ν from critical scaling
   
3. **Finite-size scaling connection**:
   - For finite n, hardness measure should correlate with distance to threshold
   - Need: 𝔼[hardness | α] ≥ h((α_c - α)n^(1/ν)) for some scaling function h

### Numerical Exploration Initial Conditions
- **Random seed**: Use (timestamp + 2) mod large prime
- **Clause density values**: α ∈ {0.1, 0.2, ..., 0.9} × α_c_estimate (focus on moderate densities)
- **Number sets**: Use {n | n = 500, 1000, 2000, 5000} to compute average hardness over 100 instances each
- **Hardness proxy**: Implement resolution width estimator or clause learning difficulty measure

---

## 4. clustering_shifts_threshold

**Axiom**: If msgEntropy < 1 then Q_SAT ≥ 0.9 → Unstable ens

### Zero-as-Condition Analysis
- **Apparent 'zero'**: The condition where *survey propagation message entropy* is zero (indicating perfect clustering/order)
- **Computational meaning**: Low message entropy indicates the solution space has clustered into exponentially many pure states, making local search algorithms ineffective even below the nominal threshold
- **State space**: Ensemble of random k-SAT formulas where survey propagation indicates clustering (low msgEntropy)
- **Evolution equation**: As α increases:
  ```
  d/dα [msgEntropy] < 0 for α > α_d (dynamical transition)
  ```
  Message entropy decreases from log(#clusters) to 0 as α increases from α_d to α_c
  - At α_d < α_c: Clustering transition (msgEntropy drops from O(1) to small positive)
  - At α_c: Condensation transition (msgEntropy → 0)

### Concrete Estimates Needed
To prove this axiom, we need:
1. **Clustering threshold identification**:
   - Locate α_d where msgEntropy first drops significantly below its maximum
   - For k-SAT: α_d ≈ 2^k ln 2 - (3/2) ln k + O(1)
   
2. **Entropy-hardness connection**:
   - Prove: msgEntropy < ε ⇒ typical instance requires exp(Ω(n)) time for local search
   - Key inequality: If msgEntropy < 1, then overlap gap property holds with parameter δ > 0
   
3. **Threshold shift quantification**:
   - Show: Effective algorithmic threshold α_alg ≤ α_c - Δ where Δ increases as msgEntropy decreases
   - Specifically: If msgEntropy < 1 and Q_SAT ≥ 0.9, then α > α_alg for some α_alg < α_c

### Numerical Exploration Initial Conditions
- **Random seed**: Use (timestamp + 3) mod large prime
- **Clause density values**: α ∈ {0.7, 0.75, ..., 1.2} × α_c_estimate (covers clustering region)
- **Number sets**: Use {n | n = 1000 * 2^k, k=0..5} for observing clustering effects
- **SP implementation**: Implement survey propagation to compute msgEntropy = -Σ_μ p_μ log p_μ where p_μ are cluster weights

---

## 5. Derived Theorems Research Directions

These theorems follow logically from the axioms, so their resolution depends on proving the underlying axioms:

### Q_SAT_lt_one_implies_easy
- **Research path**: Prove stable_if_Q_SAT_lt_one + strengthen stability definition to actual polynomial-time solvability
- **Needed**: Construct explicit algorithm (e.g., belief propagation guided decimation) and prove its efficiency for Q_SAT < 1 - ε

### Q_SAT_ge_one_implies_hard
- **Research path**: Prove unstable_if_Q_SAT_ge_one + connect to average-case hardness
- **Needed**: Establish reduction from planted satisfiable instances or use overlap gap property to rule out efficient algorithms

### phase_transition_location
- **Research path**: Determine precise value of α_c where Q_SAT = 1 corresponds to computational hardness peak
- **Needed**: Sharp threshold determination + proof that hardness(α) is unimodal with maximum at α_c

### proof_width_lower_bound
- **Research path**: Connect Q_SAT parameter to resolution width via hardness measure
- **Needed**: Prove hardness ≥ c * resolution_width for some c>0, then use existing width lower bounds

---

## General Methodology for Zero-as-Condition Approach

1. **Identify the zero**: For each axiom, determine what quantity reaches zero at the critical condition
2. **Define order parameter**: Construct a measurable quantity that is zero in one phase and non-zero in another
3. **Establish scaling relations**: Derive how the order parameter scales with distance to threshold
4. **Prove concentration**: Show the order parameter concentrates around its expectation for large n
5. **Connect to complexity**: Relate the order parameter's behavior to algorithmic difficulty measures

This approach transforms the axiomatic assumptions into questions about phase transitions in random constraint satisfaction problems, where rigorous mathematical physics techniques can be applied.

## Next Steps
1. Select one axiom to focus on initially (recommend starting with stable_if_Q_SAT_lt_one as it's most empirically established)
2. Implement numerical experiments using the specified initial conditions
3. Attempt to derive the concrete inequalities suggested above
4. Connect with existing literature on rigorous results for random k-SAT (Achlioptas, Coja-Oghlan, Ding-Sly-Sun, etc.)
5. Gradually build toward a proof sketch that could replace the `sorry`