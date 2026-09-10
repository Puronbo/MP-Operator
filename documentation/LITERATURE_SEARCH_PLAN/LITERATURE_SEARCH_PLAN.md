# Literature Search Plan for Remaining Sorrys

This document outlines a targeted literature search approach to find mathematical results that could help resolve the remaining `sorry` statements in our Lean formalization. The search focuses on specific theorems, formulas, and insights from the literature that would provide the genuine mathematical insight needed to replace axioms with theorems.

## 1. Navier-Stokes Domain (NS.lean)

### Target: `NS_Q_NS_gt_one_turbulent`
**Statement**: If there exists a scale and point where Q_NS > 1, then turbulent behavior may emerge.

**Literature to Search**:
- **"On the intermittency of velocity gradients in turbulent flows" by Anselmet et al. (1984)** - Experimental evidence linking Q-analogs to intermittency
- **"Scaling and intermittency in turbulent flow" by Frisch (1995)** - Chapter on structure functions and intermittency
- **"A turbulent remembrance" by Frisch (1993)** - Historical perspective on Kolmogorov's 1941 theory
- **"Intermittency in turbulent flows" by Sreenivasan (1991)** - Review of experimental and theoretical work
- **Key insight needed**: Precise relationship between localized enstrophy production and the development of turbulent cascades

### Target: `NS_BKM_implies_Prodi_Serrin`
**Statement**: Beale-Kato-Majda condition implies Prodi-Serrin regularity condition.

**Literature to Search**:
- **"On the breakdown of solutions for incompressible ideal fluids" by Beale, Kato, Majda (1984)** - Original BKM paper
- **"On the regularity of solutions of the Navier-Stokes equations" by Prodi (1959)** - Original Prodi work
- **"On the regularity of solutions of the Navier-Stokes equations" by Serrin (1963)** - Original Serrin work
- **"Navier-Stokes equations: Theory and numerical analysis" by Temam (2001)** - Modern treatment
- **"A proof of the Beale-Kato-Majda theorem" by Cannone, Kwon (2006)** - Simplified proof approach
- **"Logarithmically improved regularity criteria for the Navier-Stokes equations" by Escauriaza, Seregin, Šverák (2003)** - BKM with logarithmic improvements
- **Key insight needed**: Interpolation inequalities connecting L^∞_t L^1_x vorticity norm to L^p_t L^q_x velocity norms with 2/p+3/q=1

### Target: Definition sorrys (`incompressible`, `LP_block`, `energy_flux`)
**Literature to Search**:
- **"Littlewood-Paley theory and normed vector spaces" by Torchinsky (1986)** - Foundation of Littlewood-Paley blocks
- **"Harmonic analysis: Real-variable methods, orthogonality, and oscillatory integrals" by Stein (1993)** - Comprehensive treatment
- **"Turbulence: The legacy of A.N. Kolmogorov" by Frisch (1995)** - Energy cascade theory
- **"Vorticity and incompressible flow" by Majda, Bertozzi (2002)** - Modern vorticity theory
- **Key insight needed**: Precise definitions that match physical intuition while being mathematically rigorous

## 2. Yang-Mills Domain (YM.lean)

### Target: `YM_instanton_theta_small_Q_lt_one_stable`
**Statement**: If instanton-theta term is small and Q_YM < 1, then the theory is stable.

**Literature to Search**:
- **"Instantons, the quark model, and the 1/N expansion" by Witten (1979)** - Original instanton paper
- **"Computation of instanton effects in gauge theories" by 't Hooft (1976)** - Instanton calculus
- **"QCD and instantons" by Shifman, Vainshtein, Zakharov (1979)** - Instanton liquid model
- **"Instantons and supersymmetry breaking" by Affleck, Harvey, Witten (1982)** - Instantons in SUSY
- **"Electric-magnetic duality and the geometric Langlands program" by Kapustin, Witten (2006)** - Modern perspective
- **Key insight needed**: Formula connecting instanton density, theta angle, and the effective mass gap in the dilute instanton gas approximation

### Target: Phase implication axioms
**Literature to Search**:
- **"Confinement in lattice gauge theory" by Wilson (1974)** - Original lattice gauge theory paper
- **"Planar diagram expansion for large N" by 't Hooft (1974)** - Large N expansion
- **"String tension and quark confinement" by Polyakov (1977)** - String tension from Wilson loops
- **"Instantons, the quark model, and the 1/N expansion" by Witten (1979)** - Instantons and mass gap
- **"Electric-magnetic duality in N=2 SYM" by Seiberg, Witten (1994)** - Monopole condensation and mass gap
- **"Some exact multiparameter solutions of N=2 supersymmetric gauge theories" by Witten (1995)** - Seiberg-Witten solutions
- **"Instantons and SUSY breaking" by Affleck, Harvey, Witten (1982)** - AHW theorem
- **"Exact results on the space of vacua of N=2 SUSY gauge theories" by Seiberg (1994)** - Vacua structure
- **Key insight needed**: Precise mathematical definitions of the phases (confining, Higgs, conformal, free photon) and their relations to the mass gap and string tension

## 3. Birch and Swinnerton-Dyer Domain (BSD.lean)

### Target: `Q_BSD_and_completed_lt_one_imply_stable_Sha_finite`
**Statement**: If Q_BSD < 1 and Q_BSD_completed < 1 (for rank 0), then the curve is stable and Sha is finite.

**Literature to Search**:
- **"The Birch and Swinnerton-Dyer conjecture" by Birch, Swinnerton-Dyer (1965)** - Original conjecture
- **"On the conjecture of Birch and Swinnerton-Dyer for elliptic curves with complex multiplication" by Coates, Wiles (1977)** - Rank 0 case
- **"Heegner points and derivatives of L-series" by Gross, Zagier (1986)** - Height-L'(E,1) relation
- **"Euler systems" by Kolyvagin (1990)** - Bounded Sha for rank ≤1
- **"p-adic L-functions and Iwasawa theory" by Kato (1990)** - Iwasawa theory foundations
- **"Conjecture" by Bloch, Kato (1990)** - Bloch-Kato conjecture (now theorem in many cases)
- **"p-adic BSD conjecture" by Mazur, Tate, Teitelbaum** - p-adic refinement
- **"Iwasawa main conjecture for elliptic curves over totally real fields" by Skinner, Urban (2014)** - Recent advances
- **"Iwasawa theory and elliptic curves" by Kakde (2018)** - Main conjecture progress
- **Key insight needed**: Formula connecting the archimedean L-value, the completed L-function, and the order of Sha

### Target: `all_Q_BSD_p_lt_one_imply_Sha_finite`
**Statement**: If for all primes p, Q_BSD_p E p < 1, then the Tate-Shafarevich group is finite.

**Literature to Search**:
- Same as above, with focus on:
- **"p-adic heights" by Schneider** - p-adic BSD formulations
- **"Heegner points and derivatives of L-series" by Zhang (2001)** - Generalized Gross-Zagier
- **"Iwasawa theory of elliptic curves at supersingular primes" by Pollack, Weston (2011)** - Supersingular case
- **"Conjectures and theorems related to the Birch and Swinnerton-Dyer conjecture" by Breuil, Conrad, Diamond, Taylor (2001)** - Modularity connections
- **Key insight needed**: Product formula relating local (p-adic) BSD quotients to the global Sha

### Target: `root_number_one_rank_even`
**Statement**: If the root number is 1 and the L-value does not vanish, then the rank is even.

**Literature to Search**:
- **"Root numbers of elliptic curves in residue characteristic 2" by Dokchitser, Dokchitser (2010)** - Root number computation
- **"Parity ranks of Selmer groups" by Dokchitser, Dokchitser (2010)** - Parity conjecture
- **"The parity conjecture for elliptic curves" by Tim Dokchitser, Vladimir Dokchitser (2010)** - Survey
- **"Root numbers and elliptic curves" by Rohrlich (1984, 1996)** - Original work on root numbers
- **"Functional equations of L-functions" by Iwaniec, Kowalski (2005)** - General theory
- **Key insight needed**: Proof that the sign of the functional equation determines the parity of the rank

### Target: `modular_degree_one_optimal`
**Statement**: If the modular degree is 1, then the curve is optimal and the congruence number is 1.

**Literature to Search**:
- **"Modular modular symbols and the Birch and Swinnerton-Dyer conjecture" by Agashe, Ribet (2004)** - Main reference
- **"The modular degree, congruence number, and multiplicity one" by Agashe, Ribet, Stein (2006)** - Detailed study
- **"On the congruence number of modular abelian varieties" by Ling (2007)** - Congruence number theory
- **"Computing the modular degree of an elliptic curve" by Agashe, Stein (2005)** - Algorithmic aspects
- **"Congruences between modular forms and the Eichler-Shimura isomorphism" by Diamond, Im (1995)** - Congruence theory
- **Key insight needed**: Exact formula relating modular degree, congruence number, and special L-values when modular degree = 1

## 4. Cross-Domain Connections

### Target: Helicity (NS) ↔ Instanton number (YM)
**Literature to Search**:
- **"Topological fluid mechanics" by Moffatt (1978)** - Helicity as topological invariant
- **"Helicity and the spectrum of turbulence" by Kelbert (1965)** - Early helicity work
- **"Instantons and chaos in QCD" by Douglas, Shenker (1990)** - Instantons and topological charge
- **"Topological susceptibility in QCD" by Witten (1979)** - Topological charge and theta angle
- **"The theta dependence of the mass gap in SU(N) gauge theories" by Kovner, Rosenstein (1993)** - Theta dependence
- **Key insight needed**: Mathematical analogy between helicity conservation in 3D fluids and topological charge conservation in gauge theories

### Target: Tamagawa numbers (BSD) ↔ String tension (YM)
**Literature to Search**:
- **"Local densities of elliptic curves" by Saito** - Tamagawa number computation
- **"Tamagawa numbers of abelian varieties and local zeta functions" by Ono (1998)** - General theory
- **"String tension in QCD from lattice gauge theory" by Bali (2001)** - Lattice computations
- **"The QCD string tension" by Teper (1998)** - Review of string tension calculations
- **"Confinement and chiral symmetry restoration in QCD" by Philipsen (2001)** - Phase transitions
- **Key insight needed**: Both measure local contributions to global invariants (Sha vs. vacuum energy)

### Target: Spectral genus (YM) ↔ p-adic Hodge theory (BSD)
**Literature to Search**:
- **"Spectral networks, wall-crossing, and the WKB approximation" by Gaiotto, Moore, Neitzke (2010)** - Spectral networks
- **"Hitchin systems" by Hitchin (1987)** - Original spectral curve paper
- **"p-adic Hodge theory" by Fontaine (1982)** - Foundational work
- **"p-adic Hodge theory and arithmetic motives" by Faltings (1989)** - Comparative study
- **"The p-adic Hodge theorem for rigid analytic varieties" by Faltings (1988)** - Rigid analytic case
- **"p-adic Hodge theory in equal characteristic" by Gabber, Ramero (2003)** - Equal characteristic case
- **Key insight needed**: Both connect geometric/spectral data to arithmetic/physical invariants (mass gap vs. L-values)

## Search Strategy

1. **Priority Order**: Focus on the derived theorems first (those marked sorry in the theorems section), then work backward to axioms that might be proven using those theorems.

2. **Search Terms**: Use specific combinations like:
   - "Beale-Kato-Majda implies Prodi-Serrin logarithmic improvement"
   - "instanton theta dependence mass gap formula Witten 1979"
   - "explicit Iwasawa mu invariant elliptic curve Skinner-Urban 2014"
   - "Bloch-Kato special case ordinary elliptic curves proof"
   - "modular degree congruence number formula Agashe Ribet 2004"
   - "helicity topological invariant fluid dynamics Moffatt 1978"
   - "Tamagawa numbers local global invariants elliptic curves"
   - "spectral genus Seiberg-Witten curve Gaiotto Moore Neitzke 2010"

3. **Expected Outcomes**: For each target sorry, identify:
   - Specific theorem/proposition from literature
   - Precise mathematical statement
   - How it maps to our Lean formalization
   - What additional definitions or lemmas would be needed
   - Where the proof would likely require genuine insight vs. where it follows from known results

This literature search plan provides a targeted approach to finding the genuine mathematical insights needed to replace our remaining sorrys with actual theorems, building on the axiomatic framework we've developed and the numerical intuition we've gained.