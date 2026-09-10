# Strand-Specific Photon Energy Deposition

## Assumptions

- Beam cross-sectional area: 1 mm² (0.01 cm²)
- Monte Carlo photons per wavelength: 20,000
- Strand fractions (illustrative):
  - Epidermis: melanin 100%
  - Dermis: hemoglobin 40%, collagen 60%
  - Subcutis: elastin 70%, collagen 30%
- Energy deposited per layer obtained from Monte Carlo simulation with continuous slowing down approximation.

## Results

| Wavelength (nm) | Strand | Energy Deposited (J) | Fraction of Total Deposited Energy |
|-----------------|--------|----------------------|------------------------------------|
| 450 | melanin | 3.553448e-17 | 0.027291 |
| 450 | hemoglobin | 2.918885e-16 | 0.224177 |
| 450 | collagen | 4.378328e-16 | 0.336266 |
| 450 | elastin | 3.757518e-16 | 0.288586 |
| 450 | collagen | 1.610365e-16 | 0.123680 |
| 550 | melanin | 5.605817e-17 | 0.026484 |
| 550 | hemoglobin | 5.580294e-16 | 0.263636 |
| 550 | collagen | 8.370441e-16 | 0.395455 |
| 550 | elastin | 4.658717e-16 | 0.220097 |
| 550 | collagen | 1.996593e-16 | 0.094327 |
| 650 | melanin | 2.971264e-17 | 0.024866 |
| 650 | hemoglobin | 2.889279e-16 | 0.241801 |
| 650 | collagen | 4.333919e-16 | 0.362701 |
| 650 | elastin | 3.100079e-16 | 0.259442 |
| 650 | collagen | 1.328605e-16 | 0.111190 |

## Notes

- The fractions are illustrative and not based on actual mass attenuation coefficients from NIST XCOM. For a precise calculation, one would need the mass attenuation coefficients (μ/ρ) for each biochemical strand at the given wavelengths and the weight fractions within each layer.
- The simulation tracks energy deposition per layer; splitting by strand is a post-processing step based on assumed fractions.
- Future work could integrate strand-specific absorption coefficients into the optical property model.
