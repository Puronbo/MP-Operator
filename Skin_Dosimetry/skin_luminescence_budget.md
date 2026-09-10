# Luminescence Transmission Through Skin

## 1. Optical Coefficients (from literature)

Values at λ = 600 nm (representative red‑orange) taken from
[Absorption and reduced scattering coefficients in epidermis and dermis](https://pmc.ncbi.nlm.nih.gov/articles/PMC10704088/):

| Layer          | μₐ (mm⁻¹) | μₛ′ (mm⁻¹) |
|----------------|-----------|------------|
| Epidermis      | 1.75*     | 1.99       |
| Dermis (upper) | 0.049     | 1.99       |
| Dermis (lower) | 0.029     | 1.99       |

\* Epidermal absorption derived from melanin content: μₐ,epi × t_epi = 0.11 (dimensionless) with median epidermal thickness t_epi = 0.063 mm → μₐ,epi ≈ 0.11 / 0.063 ≈ 1.75 mm⁻¹.

The reduced scattering coefficient is taken as uniform across layers: μₛ′ ≈ 1.99 mm⁻¹.

## 2. Effective Attenuation Coefficient

In the diffusion approximation the effective attenuation coefficient is

\[
\mu_{\text{eff}} = \sqrt{3\,\mu_a\,(\mu_a + \mu_s')}.
\]

Computations:

- Epidermis:  
  \(\mu_{\text{eff, epi}} = \sqrt{3 \times 1.75 \times (1.75 + 1.99)} 
   = \sqrt{3 \times 1.75 \times 3.74}
   = \sqrt{19.635}
   \approx 4.43\ \text{mm}^{-1}\)

- Dermis (average μₐ ≈ 0.04 mm⁻¹):  
  \(\mu_{\text{eff, derm}} = \sqrt{3 \times 0.04 \times (0.04 + 1.99)}
   = \sqrt{3 \times 0.04 \times 2.03}
   = \sqrt{0.2436}
   \approx 0.494\ \text{mm}^{-1}\)

## 3. Transmittance Through Skin Layers

Assuming normal incidence and neglecting reflections, the transmittance for a stack of layers is

\[
T = \exp\!\Bigl[-\sum_i \mu_{\text{eff},i}\,L_i\Bigr],
\]

where \(L_i\) is the thickness of layer i.

We consider three representative total thicknesses:

| Total thickness | Layer breakdown (mm)                                   | Attenuation Σμ_eff L | Transmittance T |
|-----------------|--------------------------------------------------------|----------------------|-----------------|
| 0.1 mm (epidermis only) | epidermis = 0.10                                      | 4.43 × 0.10 = 0.443  | e⁻⁰·⁴⁴³ ≈ 0.642 |
| 1.0 mm (epidermis + dermis) | epidermis = 0.063, dermis = 0.937                | 4.43 × 0.063 + 0.494 × 0.937 = 0.279 + 0.463 = 0.742 | e⁻⁰·⁷⁴² ≈ 0.476 |
| 3.0 mm (epidermis + dermis) | epidermis = 0.063, dermis = 2.937                | 4.43 × 0.063 + 0.494 × 2.937 = 0.279 + 1.450 = 1.729 | e⁻¹·⁷²⁹ ≈ 0.177 |

*(Epidermal thickness taken as the median 0.063 mm from the source.)*

## 4. Required Source Luminescence for a Detectable Signal

Assume a detector with:
- Quantum efficiency η_det = 0.80
- Collection efficiency (solid‑angle, optics) η_coll = 0.10  
  → overall detection efficiency η = η_det · η_coll = 0.08.

To register **one detectable photon per second**, the emitted photon flux Φ_src (photons s⁻¹) must satisfy

\[
\Phi_{\text{src}} \times T \times \eta = 1
\quad\Longrightarrow\quad
\Phi_{\text{src}} = \frac{1}{T\,\eta}.
\]

With η = 0.08, this simplifies to \(\Phi_{\text{src}} = 12.5 / T\).

| Thickness | T        | Φ_src (photons s⁻¹) | Corresponding optical power at 600 nm* |
|-----------|----------|---------------------|----------------------------------------|
| 0.1 mm    | 0.642    | 19.5                | 6.5 × 10⁻¹⁸ W (6.5 aW)                |
| 1.0 mm    | 0.476    | 26.3                | 8.8 × 10⁻¹⁸ W (8.8 aW)                |
| 3.0 mm    | 0.177    | 70.6                | 2.4 × 10⁻¹⁷ W (24 aW)                |

\* Photon energy at 600 nm: \(E = hc/\lambda \approx 3.31\times10^{-19}\) J.  
Power = Φ_src × E.

### Interpretation

Even for several millimetres of skin, the required photon flux is extraordinarily low because the detection efficiency assumed (10 % collection, 80 % QE) is generous and we considered only a single count per second. In realistic experiments one would demand a higher signal‑to‑noise ratio (e.g., 100 counts s⁻¹) and account for isotropic emission, background autofluorescence, etc. Scaling linearly, a 100‑fold increase in desired count rate raises the required power to the femtowatt range, still easily achievable with modest LEDs or lasers.

Nevertheless, the calculation shows that **optical attenuation in skin is not a fundamental barrier** for detecting weak luminescence; the limiting factors are more likely detector noise, autofluorescence, and the intrinsic brightness of the luminescence source.

## 5. References

1. Absorption and reduced scattering coefficients in epidermis and dermis … – PMID: PMC10704088.  
   URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC10704088/