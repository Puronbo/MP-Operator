# Dose Safety Comparison

## Assumptions

- Beam cross-sectional area: 1 mm² (0.01 cm²)
- Tissue density: 1 g/cm³ (1000 kg/m³)
- Skin thermal damage threshold: 10 J/cm² (for exposure durations >10 s, based on IEC 62471/ANSI Z136.1)
- Photon energy deposition fraction from Monte Carlo simulation (20k photons per wavelength).

## Deposition Fractions

| Wavelength (nm) | Photon Energy (J) | Deposition Fraction |
|-----------------|-------------------|---------------------|
| 450 | 4.414324e-19 | 1.457207e-01 |
| 550 | 3.611720e-19 | 2.951634e-01 |
| 650 | 3.056071e-19 | 1.917917e-01 |

## Time to Reach Thermal Damage Threshold (10 J/cm²)

Assuming continuous wave illumination.

| Wavelength (nm) | Source Power (W) | Irradiance (W/cm²) | Deposited Power Density (W/cm²) | Time to Threshold (s) |
|-----------------|------------------|--------------------|---------------------------------|----------------------|
| 450 | 1.0e-09 | 1.000000e-07 | 1.457207e-08 | 6.86e+08 |
| 450 | 1.0e-08 | 1.000000e-06 | 1.457207e-07 | 6.86e+07 |
| 450 | 1.0e-07 | 1.000000e-05 | 1.457207e-06 | 6.86e+06 |
| 450 | 1.0e-06 | 1.000000e-04 | 1.457207e-05 | 6.86e+05 |
| 450 | 1.0e-05 | 1.000000e-03 | 1.457207e-04 | 6.86e+04 |
| 450 | 1.0e-04 | 1.000000e-02 | 1.457207e-03 | 6.86e+03 |
| 450 | 1.0e-03 | 1.000000e-01 | 1.457207e-02 | 6.86e+02 |
| 550 | 1.0e-09 | 1.000000e-07 | 2.951634e-08 | 3.39e+08 |
| 550 | 1.0e-08 | 1.000000e-06 | 2.951634e-07 | 3.39e+07 |
| 550 | 1.0e-07 | 1.000000e-05 | 2.951634e-06 | 3.39e+06 |
| 550 | 1.0e-06 | 1.000000e-04 | 2.951634e-05 | 3.39e+05 |
| 550 | 1.0e-05 | 1.000000e-03 | 2.951634e-04 | 3.39e+04 |
| 550 | 1.0e-04 | 1.000000e-02 | 2.951634e-03 | 3.39e+03 |
| 550 | 1.0e-03 | 1.000000e-01 | 2.951634e-02 | 3.39e+02 |
| 650 | 1.0e-09 | 1.000000e-07 | 1.917917e-08 | 5.21e+08 |
| 650 | 1.0e-08 | 1.000000e-06 | 1.917917e-07 | 5.21e+07 |
| 650 | 1.0e-07 | 1.000000e-05 | 1.917917e-06 | 5.21e+06 |
| 650 | 1.0e-06 | 1.000000e-04 | 1.917917e-05 | 5.21e+05 |
| 650 | 1.0e-05 | 1.000000e-03 | 1.917917e-04 | 5.21e+04 |
| 650 | 1.0e-04 | 1.000000e-02 | 1.917917e-03 | 5.21e+03 |
| 650 | 1.0e-03 | 1.000000e-01 | 1.917917e-02 | 5.21e+02 |

## Notes

- The deposition fraction includes all energy deposited via absorption (continuous slowing down approximation).
- Scattering does not deposit energy directly but increases path length, potentially increasing absorption.
- The threshold of 10 J/cm² is a conservative estimate for thermal damage; actual thresholds may vary with wavelength and exposure duration.
- For pulsed lasers, different limits apply.
- The simulation does not account for secondary electron transport or thermal diffusion.
