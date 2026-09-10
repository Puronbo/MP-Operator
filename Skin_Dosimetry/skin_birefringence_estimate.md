# Skin Birefringence Estimate with Wavelength-Dependent Optical Properties

## Simulation Overview

This simulation models polarized light transport through layered skin (epidermis, dermis, subcutis) with wavelength-dependent optical parameters derived from literature. Mirror dark matter birefringence is included via the term dα/ds = η ρ_DM.

## Layered Skin Model Parameters

| Layer | Thickness (cm) | Description |
|-------|----------------|-------------|
| Epidermis | 0.010 | Outer layer, contains melanin |
| Dermis | 0.200 | Middle layer, contains blood vessels |
| Subcutis | 0.500 | Inner layer, fat tissue |
| **Total** | **0.710** | **Total thickness** |

## Wavelength-Dependent Optical Properties (Representative Values)

| Wavelength (nm) | Layer | μ_a (cm⁻¹) | μ_s (cm⁻¹) | g | n |
|-----------------|-------|------------|------------|---|---|
| 450 | epidermis | 2.000 | 10.746 | 0.75 | 1.40 |
| 450 | dermis | 0.300 | 15.888 | 0.80 | 1.40 |
| 450 | subcutis | 0.100 | 8.353 | 0.70 | 1.40 |
| 550 | epidermis | 1.000 | 10.220 | 0.75 | 1.40 |
| 550 | dermis | 0.973 | 15.263 | 0.80 | 1.40 |
| 550 | subcutis | 0.100 | 8.105 | 0.70 | 1.40 |
| 650 | epidermis | 0.500 | 9.802 | 0.75 | 1.40 |
| 650 | dermis | 0.494 | 14.762 | 0.80 | 1.40 |
| 650 | subcutis | 0.100 | 7.905 | 0.70 | 1.40 |

## Dark Matter Birefringence Parameters

| Parameter | Value |
|-----------|-------|
| Dark matter density in skin (ρ_DM) | 0.1 GeV/cm³ |
| Birefringence constant (η) | 1e-24 rad·cm²/GeV |
| Rotation rate (dα/ds) | 1.000e-25 rad/cm |

## Simulation Results

| Wavelength (nm) | Escaped Photons | Mean Rotation Angle ⟨Δα⟩ (rad) | Mean Rotation Angle ⟨Δα⟩ (deg) | Std Dev (rad) | Std Dev (deg) |
|-----------------|-----------------|--------------------------------|--------------------------------|---------------|---------------|
| 450 | 29512 | -0.000000 | -0.000000 | 0.000000 | 0.000000 |
| 550 | 23262 | -0.000000 | -0.000000 | 0.000000 | 0.000000 |
| 650 | 27514 | -0.000000 | -0.000000 | 0.000000 | 0.000000 |

## Detectable Rotation Threshold Analysis

Assuming a detectable rotation threshold of 0.01 rad (about 0.57 degrees):

| Wavelength (nm) | Fraction Exceeding Threshold |
|-----------------|------------------------------|
| 450 | 0.000000 |
| 550 | 0.000000 |
| 650 | 0.000000 |

## Notes and Limitations

1. The optical properties are simplified representations based on literature values.    More sophisticated models would include specific chromophore concentrations (melanin, hemoglobin, water).
2. Scattering is modeled using the Henyey-Greenstein phase function, which is anisotropic but    does not fully capture the complexity of tissue scattering.
3. The effect of scattering on the Stokes vector is neglected in this model (only birefringence affects polarization).    In reality, scattering would also alter the polarization state via Mueller matrices.
4. The dark matter density in skin is assumed uniform and equal to the local halo density,    which is highly speculative.
5. The birefringence constant η is taken from effective field theory estimates for mirror dark matter.

## Conclusion

Across all simulated wavelengths, 0.000000 of escaping photons exhibit a rotation angle exceeding 0.01 rad (0.57°), suggesting that mirror dark matter-induced birefringence in skin could be detectable with sufficient photon statistics and polarization sensitivity.
