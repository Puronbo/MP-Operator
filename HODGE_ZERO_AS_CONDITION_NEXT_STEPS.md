# Concrete Next Steps for HODGE.lean Using Zero-as-Condition Perspective

This document develops specific, actionable research directions for transforming the axiomatic assumptions in HODGE.lean into proven theorems by applying the 'zero-as-condition' perspective (treating zero as a condition rather than a number) to each sorry statement.

## 1. stable_if_Q_H_lt_one

**Zero-condition interpretation**: The apparent 'zero' corresponds to the Griffiths group vanishing (griffithsSize = 0). The condition Q_H < 1 is a relaxation where the Griffiths group is non-zero but sufficiently small relative to the Hodge space.

**State space**: The moduli space of algebraic varieties of fixed dimension, where each point represents a Hodge structure with varying Griffiths group size and Hodge space dimension. Specifically, this lives in the Griffiths group Griffiths^dim(X) = {homologically trivial algebraic cycles} / {algebraically trivial}.

**Evolution equation**: The period map (or Gauss-Manin connection) governs how the Hodge filtration varies in families. The Griffiths group size relates to the kernel of the Abel-Jacobi map into intermediate Jacobians: Griff^p(X) ≅ ker(AJ: CH^p_{hom}(X) → J^p(X)).

**Concrete estimates/inequalities to resolve**:
- Establish an explicit bound: griffithsSize ≤ C · hodgeSpaceDim for some constant C < 1/2 that ensures algebraicity of Hodge classes.
- Using the Bloch-Beilinson conjectures: if the regulator map from motivic cohomology to Deligne cohomology is injective with bounded kernel, then griffithsSize ≤ dim(ker(regulator)).
- Specifically, prove that if griffithsSize/hodgeSpaceDim < 1/2, then the Hodge conjecture holds for the family by constructing an explicit algebraic cycle representing any Hodge class.

**Connection to user's data**:
- Primary digit set {0,1,2,2,6} and timestamp 972555980 generate permutation 10212 as starting point.
- Interpret permutation values as griffithsSize and hodgeSpaceDim: griffithsSize = first two digits (10), hodgeSpaceDim = last three digits (212) → Q_H = 10/212 ≈ 0.047 < 1.
- Numerical exploration: Compute Q_H for all 48 permutations using this splitting scheme and identify the threshold value where Q_H crosses 1.

**Actionable research direction**:
1. Develop a precise relationship between griffithsSize and hodgeSpaceDim using Voisin's work on Griffiths groups of complete intersections.
2. Prove that if griffithsSize/hodgeSpaceDim < 1/2, then the Abel-Jacobi map is injective on homologically trivial cycles, implying all Hodge classes are algebraic.
3. Connect to existing results: For complete intersections of dimension ≥ 3, Voisin showed that Griffiths groups are often finitely generated; use this to bound griffithsSize.

## 2. unstable_if_Q_H_ge_one

**Zero-condition interpretation**: The 'zero' condition here is the triviality of the obstruction (griffithsSize = 0). The condition Q_H ≥ 1 means the obstruction is at least as large as the Hodge space, suggesting a failure of algebraicity.

**State space**: Same moduli space, but focusing on regions where the Griffiths group is large relative to Hodge classes.

**Evolution equation**: The variation of Hodge structure via the period map; monodromy actions can increase Griffiths group size in degenerations. Specifically, the monodromy weight ladder limits the possible sizes of Griffiths groups in families.

**Concrete estimates/inequalities to resolve**:
- Show that if griffithsSize ≥ hodgeSpaceDim, then there exists a non-algebraic Hodge class by constructing an explicit element in Griff^p(X) that maps to zero under the cycle class map.
- Use the intermediate Jacobian: if the Abel-Jacobi map has non-trivial kernel in Griffiths^p(X), then obstructions persist.
- Specifically, prove that griffithsSize ≥ hodgeSpaceDim implies the existence of a Hodge class not in the image of the cycle class map CH^p(X) → H^{2p}(X,Q).

**Connection to user's data**:
- For permutation 22610: griffithsSize = 22, hodgeSpaceDim = 610 → Q_H ≈ 0.036 < 1 (still stable).
- To get Q_H ≥ 1 with digits {0,1,2,2,6}, we need griffithsSize ≥ hodgeSpaceDim. Maximum griffithsSize = 62, minimum hodgeSpaceDim = 012 = 12 (but permutations exclude leading zeros, so actual min is 102 = 102? Need to clarify splitting).
- Alternative splitting: griffithsSize = first three digits, hodgeSpaceDim = last two digits. Then for 62200: griffithsSize=622, hodgeSpaceDim=00=0 (invalid). For 22016: griffithsSize=220, hodgeSpaceDim=16 → Q_H=13.75 ≥ 1.
- This suggests we need a consistent way to extract Hodge invariants from permutations for numerical exploration.

**Actionable research direction**:
1. Construct families of varieties where griffithsSize can be made arbitrarily large relative to hodgeSpaceDim (e.g., using products with elliptic curves or specific constructions of non-trivial Griffiths groups).
2. Prove that in such families, when griffithsSize ≥ hodgeSpaceDim, the Abel-Jacobi map has a kernel that surjects onto a subspace of Hodge classes not algebraic.
3. Connect to the infinitesimal period relation and the notion of 'weakly exceptional' varieties where the Griffiths group is particularly large.

## 3. motivic_vanishing_controls_Griffiths

**Zero-condition interpretation**: The 'zero' is the vanishing of motivic cohomology (motivicCohoSize = 0). This condition should control the Griffiths group, making it small enough that Q_H < 1.

**State space**: The category of mixed motives or the space of algebraic cycles with cohomological descriptions. The motivic cohomology group is H^1_M(X, Q(dim)) or similar, which conjecturally maps to the Griffiths group via the regulator map.

**Evolution equation**: Motivic cohomology groups vary in families via regulators or étale realizations; the vanishing condition should be open in families under certain conditions (e.g., in smooth proper families over connected bases).

**Concrete estimates/inequalities to resolve**:
- Establish that griffithsSize ≤ motivicCohoSize + K, where K is some correction term that vanishes under good reduction.
- If motivicCohoSize = 0, then griffithsSize = 0 (under appropriate hypotheses), hence Q_H = 0 < 1.
- More precisely, use the cycle class map and the assumption that motivic cohomology detects algebraic cycles: the size of the Griffiths group is bounded by the cokernel of the regulator map from motivic cohomology to Deligne cohomology.

**Connection to user's data**:
- Assign motivicCohoSize from permutation: e.g., motivicCohoSize = sum of digits. For 10212: sum = 1+0+2+1+2=6.
- If griffithsSize = first two digits (10), hodgeSpaceDim = last three digits (212), then Q_H=10/212≈0.047.
- To test the axiom, we need motivicCohoSize=0. From our digit set, sum of digits=0 only with all zeros (not available). Alternative: motivicCohoSize = (product of digits) - (timestamp mod 10) or similar to achieve zero for some permutations.
- For permutation 10212 and timestamp 972555980: product = 0, so motivicCohoSize = 0 - (972555980 mod 10) = -0 = 0 (since last digit is 0).

**Actionable research direction**:
1. Precisely define the motivic cohomology group and construct the regulator map to the Griffiths group.
2. Prove that the kernel of this regulator map controls the size of the Griffiths group, so that vanishing motivic cohomology implies trivial Griffiths group.
3. Relate to the Bloch-Beilinson conjectures and the motivic spectral sequence; verify the implication in cases where these are known (e.g., for curves, abelian varieties).

## 4. monodromy_constrains_variation

**Zero-condition interpretation**: The 'zero' corresponds to unipotent monodromy (logarithm of monodromy nilpotent) where the trace of the logarithm is small. The condition monodromyTrace < 10 likely corresponds to the monodromy being sufficiently close to identity.

**State space**: The local system of primitive cohomology in a family, where monodromy acts. The trace of monodromy (or its logarithm) measures the deviation from unipotency.

**Evolution equation**: The Gauss-Manin connection governs the infinitesimal variation of Hodge structure; monodromy is the exponential of the residue of this connection: T = exp(2πi N) where N is the nilpotent part.

**Concrete estimates/inequalities to resolve**:
- Relate monodromy trace to griffithsSize via the monodromy weight ladder: if N is the logarithm of monodromy, then griffithsSize ≤ C · dim(ker(N)) for some constant C.
- Show that if |trace(N)| < 10, then the variation of Hodge structure is constrained, limiting griffithsSize growth.
- Specifically, prove an inequality: griffithsSize ≤ C · |trace(N)| + D, so that if trace(N) < 10 then griffithsSize < 10C + D, and with hodgeSpaceDim sufficiently large, Q_H < 2.

**Connection to user's data**:
- Assign monodromyTrace from permutation: e.g., monodromyTrace = (permutation mod 20) - 10 to center around zero.
- For permutation 10212: 10212 mod 20 = 12, so monodromyTrace = 12-10=2 (<10).
- Using griffithsSize=10, hodgeSpaceDim=212 from earlier, Q_H≈0.047 < 2, satisfying the conclusion.
- Explore how variations in permutation (via timestamp changes) affect both monodromyTrace and Q_H.

**Actionable research direction**:
1. Use the nilpotent orbit theorem and Schmid's estimates to bound the variation of the Hodge norm in terms of monodromy weight.
2. Connect griffithsSize to the extension data in the limiting mixed Hodge structure: the size of Griff^p is related to dim(gr^W_{−1} H^{p-1,p}(X)) in the limit.
3. Prove that when the monodromy logarithm N has small trace (i.e., ||N|| < ε), then the associated graded of the weight ladder forces griffithsSize to be small relative to hodgeSpaceDim.

## Derived Theorems

### Q_H_lt_one_implies_algebraic
This is equivalent to stable_if_Q_H_lt_one if we interpret "algebraic" as the Hodge conjecture holding. Research direction identical to section 1.

### Q_H_ge_one_implies_nonalgebraic
Identical to unstable_if_Q_H_ge_one (section 2).

### griffiths_size_bound
**Zero-condition interpretation**: The bound should express that griffithsSize = 0 when certain obstructions vanish (motivic cohomology vanishes, monodromy is sufficiently unipotent, etc.).

**Research direction**:
- Establish bounds of the form griffithsSize ≤ F(motivicCohoSize, monodromyData, deformationData) where F = 0 when all obstructions are zero.
- For example: griffithsSize ≤ motivicCohoSize + G(monodromyTrace) where G(t) = 0 for |t| < ε.
- Use the provided number sets to test candidate bounds numerically: compute griffithsSize, motivicCohoSize, monodromyTrace for each permutation and verify the bound.

### period_map_differential
**Zero-condition interpretation**: The differential of the period map should vanish when the Griffiths group is zero (i.e., when the infinitesimal invariant of normal functions is zero).

**Research direction**:
- Recall that the infinitesimal invariant δν of a normal function ν lies in H^{p-1,q+1}(X, Ω^1_log) and obstructs the lift to an algebraic cycle.
- The Griffiths group relates to the kernel of the Abel-Jacobi map, and its infinitesimal version is Griff^p of the infinitesimal variation.
- Prove that if the period map differential dπ satisfies rank(dπ|_F) ≥ dim(H^{p,dim-p}) - ε (where F is the Hodge filtration), then griffithsSize < ε · hodgeSpaceDim.
- Specifically, bound griffithsSize by the cokernel of the period map differential twisted by the Hodge filtration: griffithsSize ≤ dim(coker(dπ ⊗ F^{-p})).

## General Numerical Exploration Plan

Using the user's number sets and timestamp:

1. **Generate permutations** of {0,1,2,2,6} (excluding leading zero) as in NUMERICAL_EXPLORATION.md (48 total).
2. **Assign Hodge invariants** to each permutation using a consistent scheme:
   - Option A (split): first two digits → griffithsSize, next two → hodgeSpaceDim, last digit → motivicCohoSize, timestamp mod 20 → monodromyTrace
   - Option B (functions): griffithsSize = sum of first two digits, hodgeSpaceDim = product of last three digits, etc.
3. **Compute Q_H** and check axioms/derived theorems for each permutation.
4. **Identify permutations** where premises hold but conclusions fail (potential counterexamples) or where they hold (building intuition).
5. **Vary the timestamp** and observe how assignments change, simulating a family.
6. **Visualize** Q_H, griffithsSize, etc., against permutation order to see threshold behavior.

This numerical exploration will help identify realistic constraints and suggest what mathematical estimates are needed to turn axioms into theorems.