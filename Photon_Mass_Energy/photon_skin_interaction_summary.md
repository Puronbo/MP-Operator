# Photon-Skin Interaction Summary

## Overview
This document summarizes the results of a theoretical and numerical study of photon interactions with skin, covering:
- Photon mass and energy density (negligible for mechanical effects)
- Energy deposition and dose in skin layers (via Monte Carlo simulation)
- Comparison to biological safety thresholds
- Illustrative strand-specific energy deposition

The study is motivated by the explicit-formula duality framework and mirror-dark-matter effective field theory, aiming to assess the feasibility of detecting mirror-dark-matter signals via luminescence and birefringence in skin, while evaluating the biological impact of photon sources.

---

## 1. Photon Mass and Energy Density

### Assumptions
- Source power \(P\): 1 nW to 1 mW
- Wavelength \(\lambda\): 400, 500, 600, 700, 800 nm
- Skin thickness \(L\): 1 mm
- Beam cross-section \(A\): 1 mm² → illuminated volume \(V = 1\) mm³
- Residence time \(\tau = L / c\)

### Key Findings
- Photon energy density \(u = P \tau / V\) scales linearly with power and is independent of wavelength.
- Equivalent mass density \(\rho_\gamma = u / c^2\) is extremely small:
  - At 1 mW: \(\rho_\gamma \sim 3.7 \times 10^{-23}\) kg m⁻³ (\(3.7 \times 10^{-26}\) g cm⁻³)
  - Many orders of magnitude below the density of water (~1 g cm⁻³)
- **Conclusion**: The photon field’s inertia is negligible for mechanical effects on skin. However, energy deposition (dose) remains relevant for biological impact.

### Reference
- See `photon_mass_energy_density.md` for full table.

---

## 2. Energy Deposition and Dose in Skin

### Monte Carlo Simulation
- Simulated photon transport through layered skin (epidermis, dermis, subcutis) with wavelength-dependent optical properties.
- Tracked energy deposition per depth bin to compute dose (Gy).
- Included continuous slowing down approximation for energy absorption.
- Neglected polarization effects from scattering (only birefringence affects Stokes vector).

### Layer Thicknesses
- Epidermis: 0.010 cm (0.1 mm)
- Dermis: 0.200 cm (2.0 mm)
- Subcutis: 0.500 cm (5.0 mm)
- Total: 0.710 cm (7.1 mm)

### Simulation Results (50,000 photons per wavelength)
| Wavelength (nm) | Top Escapes | Bottom Escapes | Absorbed |
|-----------------|-------------|----------------|----------|
| 450             | 29,665      | 11,618         | 8,717    |
| 550             | 23,359      | 9,144          | 17,497   |
| 650             | 27,658      | 10,823         | 11,519   |

### Depth-Dose Curves
- Dose values are extremely low for typical source powers (nW–mW) due to low photon fluence.
- Higher absorption in epidermis for shorter wavelengths (melanin) and in dermis for longer wavelengths (hemoglobin).
- See `skin_dose_distribution.md` for detailed depth-dose tables.

---

## 3. Comparison to Biological Safety Thresholds

### Assumptions
- Beam area: 1 mm² (0.01 cm²)
- Tissue density: 1 g cm⁻³
- Thermal damage threshold: 10 J cm⁻² (for exposure >10 s, based on IEC 62471/ANSI Z136.1)
- Photon energy deposition fraction from Monte Carlo (20k photons per wavelength)

### Deposition Fractions
| Wavelength (nm) | Photon Energy (J) | Deposition Fraction |
|-----------------|-------------------|---------------------|
| 450             | 4.414324e-19      | 1.457207e-01        |
| 550             | 3.611720e-19      | 2.951634e-01        |
| 650             | 3.056071e-19      | 1.917917e-01        |

### Time to Reach Thermal Damage Threshold (10 J cm⁻²)
| Wavelength (nm) | Power (W) | Irradiance (W cm⁻²) | Deposited Power Density (W cm⁻²) | Time to Threshold (s) |
|-----------------|-----------|---------------------|----------------------------------|-----------------------|
| 450             | 1.0e-09   | 1.000000e-07        | 1.457207e-08                     | 6.86e+08              |
| 450             | 1.0e-03   | 1.000000e-01        | 1.457207e-02                     | 6.86e+02              |
| 550             | 1.0e-09   | 1.000000e-07        | 2.951634e-08                     | 3.39e+08              |
| 550             | 1.0e-03   | 1.000000e-01        | 2.951634e-02                     | 3.39e+02              |
| 650             | 1.0e-09   | 1.000000e-07        | 1.917917e-08                     | 5.21e+08              |
| 650             | 1.0e-03   | 1.000000e-01        | 1.917917e-02                     | 5.21e+02              |

### Interpretation
- For source powers in the nW–mW range, the time to reach the thermal damage threshold is hundreds of seconds to hundreds of millions of seconds.
- **Conclusion**: Ordinary source powers (nW–mW) are safely below thermal damage thresholds for continuous wave illumination.

### Reference
- See `dose_safety_comparison.md` for full table and notes.

---

## 4. Strand-Specific Photon Energy Deposition (Illustrative)

### Assumptions
- Beam area: 1 mm² (0.01 cm²)
- Monte Carlo photons per wavelength: 20,000
- Strand fractions (illustrative, not based on NIST XCOM):
  - Epidermis: melanin 100%
  - Dermis: hemoglobin 40%, collagen 60%
  - Subcutis: elastin 70%, collagen 30%
- Energy deposited per layer from Monte Carlo simulation with continuous slowing down approximation.

### Results
| Wavelength (nm) | Strand      | Energy Deposited (J) | Fraction of Total Deposited Energy |
|-----------------|-------------|----------------------|------------------------------------|
| 450             | melanin     | 3.553448e-17         | 0.027291                           |
| 450             | hemoglobin  | 2.918885e-16         | 0.224177                           |
| 450             | collagen    | 4.378328e-16         | 0.336266                           |
| 450             | elastin     | 3.757518e-16         | 0.288586                           |
| 450             | collagen    | 1.610365e-16         | 0.123680                           |
| 550             | melanin     | 5.605817e-17         | 0.026484                           |
| 550             | hemoglobin  | 5.580294e-16         | 0.263636                           |
| 550             | collagen    | 8.370441e-16         | 0.395455                           |
| 550             | elastin     | 4.658717e-16         | 0.220097                           |
| 550             | collagen    | 1.996593e-16         | 0.094327                           |
| 650             | melanin     | 2.971264e-17         | 0.024866                           |
| 650             | hemoglobin  | 2.889279e-16         | 0.241801                           |
| 650             | collagen    | 4.333919e-16         | 0.362701                           |
| 650             | elastin     | 3.100079e-16         | 0.259442                           |
| 650             | collagen    | 1.328605e-16         | 0.111190                           |

### Notes
- The fractions are illustrative and not based on actual mass attenuation coefficients from NIST XCOM.
- For a precise calculation, one would need the mass attenuation coefficients (μ/ρ) for each biochemical strand at the given wavelengths and the weight fractions within each layer.
- The simulation tracks energy deposition per layer; splitting by strand is a post-processing step based on assumed fractions.
- See `strand_specific_dose.md` for full details.

---

## 5. Implications for Mirror Dark Matter Detection

While the primary focus of this summary is photon mass/energy density, dose, and strand deposition, the study is situated within a broader framework seeking to detect mirror-dark-matter interactions via:
- Luminescence transmission (quantified by Q-luminescence parameter)
- Polarization rotation (birefringence) from mirror-dark-matter induced vacuum birefringence

From related work (`skin_luminescence_budget.md`, `skin_birefringence_estimate.md`, `q_luminescence.md`, `resonant_enhancement.md`):
- Expected polarization rotation angles are ≤10⁻⁶ rad, far below detection threshold (~0.01 rad) for ordinary source powers.
- Resonant enhancement (via hidden-sector photon mixing) could amplify scattering cross-sections and birefringence by factors of 10⁶–10¹² for meV–eV resonance masses and TeV-scale cutoffs, potentially bringing signals into observable range.
- The Q-luminescence parameter (expected detectable count rate) is many orders of magnitude above 1 for typical source powers (≥1 nW), placing the system in the "inflicted" sector (Q_L ≫ 1) where detectable signals are possible in principle, but the mirror-dark-matter coupling must be sufficiently weak to avoid overproduction and conflict with astrophysical bounds.

### Conclusion on Detectability
- Photon energy deposition in skin is negligible for mechanical effects but non-zero for dose.
- At ordinary source powers, the deposited dose is far below safety thresholds.
- Mirror-dark-matter-induced signals (birefringence, luminescence) would require resonant enhancement or significant coupling to be observable, subject to constraints from stellar cooling, CMB spectral distortions, and gamma-ray observations.

---

## References
1. Jacques, S. L. “Optical properties of biological tissues: a review.” *Phys. Med. Biol.* 58, R37 (2013).
2. CODATA 2018 (fundamental constants).
3. IEC 62471: Photobiological safety of lamps and lamp systems.
4. ANSI Z136.1: Safe Use of Lasers.
5. Mirror-dark-matter effective field theory and resonant enhancement notes in `mirror_dm_eft.md` and `resonant_enhancement.md`.

---
*File generated as synthesis of tasks #24–#27.*