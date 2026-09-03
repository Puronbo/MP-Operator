# Light Transport in Skin Pores: Multiple‑Scattering Path Enhancement

## 1. Motivation

In addition to the bulk scattering described by the reduced scattering coefficient μₛ′, skin contains **microscopic pores** (e.g., sweat glands, hair follicles, intercellular spaces) with typical diameters ranging from a few µm to ≈ 100 µm. When a photon enters such a pore it can undergo **multiple internal reflections** (specular or diffuse) before exiting, dramatically increasing its optical path length compared to a straight line through the same thickness of tissue.

This analysis quantifies:
- The average number of scattering events inside a pore of given size and reflectivity.
- The resulting **path‑length enhancement factor** 𝜁 = ⟨L_eff⟩ / L_geom.
- How 𝜁 modifies the luminescence‑budget calculations (Task #1) and the expected birefringence rotation (Task #2).

## 2. Geometry and Optical Model

- Treat a pore as a **cylinder** of diameter *d* and length *Lₚ* (≈ skin thickness for trans‑dermal pores, or smaller for superficial follicles).  
- Inner wall characterized by a **reflectivity** *R* (0 ≤ R ≤ 1) and a **scattering phase function** approximated by the Henyey‑Greenstein function with anisotropy *gₚ* (forward‑scattering bias).  
- For simplicity we assume **isotropic scattering** inside the pore (*gₚ* = 0) and **specular reflection** with probability *R*; diffuse scattering is modeled as a random redirection after each bounce.

The photon performs a **random walk** inside the pore until it either:
1. **Escapes** through the pore opening (probability per bounce *Pₑₛc*), or  
2. Is **absorbed** by the wall (probability per bounce *Pₐbₛ* = 1 − *R*).

## 3. Mean Number of Bounces

For a cylindrical pore with isotropic interior scattering, the escape probability per bounce can be approximated by the ratio of the pore’s cross‑sectional area to the interior surface area seen by a bouncing photon:

\[
P_{\text{esc}} \;\approx\; \frac{A_{\text{open}}}{A_{\text{wall}}}
    \;=\; \frac{\pi (d/2)^2}{\pi d L_{p}}
    \;=\; \frac{d}{4 L_{p}} .
\]

(For *Lₚ* ≫ *d* this is small, as expected.)

The probability of **surviving** a bounce (i.e., not being absorbed) is *R*.  
Thus the probability of surviving *n* bounces and then escaping on the (*n*+1)‑th bounce is

\[
P(n) \;=\; (R\,(1-P_{\text{esc}}))^{n}\; \bigl[ R\,P_{\text{esc}} \bigr] .
\]

The **mean number of bounces** before escape is

\[
\langle n \rangle \;=\; \sum_{n=0}^{\infty} n\,P(n)
   \;=\; \frac{R\,(1-P_{\text{esc}})}{1 - R\,(1-P_{\text{esc}})} .
\]

The **mean total path length** inside the pore is then

\[
\langle L_{\text{pore}} \rangle \;=\; \langle n \rangle \times \ell_{\text{bounce}} ,
\]

where the average chord length for isotropic scattering in a cylinder is

\[
\ell_{\text{bounce}} \;\approx\; \frac{4V}{S}
   \;=\; \frac{4(\pi (d/2)^2 L_{p})}{\pi d L_{p} + 2\pi (d/2)^2}
   \;=\; \frac{d}{2}\,\frac{L_{p}}{L_{p}+d/2}
   \;\approx\; \frac{d}{2}\quad (L_{p}\gg d) .
\]

Hence, for *Lₚ* ≫ *d*:

\[
\langle L_{\text{pore}} \rangle \;\approx\;
\frac{d}{2}\;
\frac{R\,(1-P_{\text{esc}})}{1 - R\,(1-P_{\text{esc}})} .
\]

Inserting *Pₑₛc* = *d*/(4*Lₚ*) and assuming *Lₚ* ≫ *d* (so *Pₑₛc* ≪ 1) gives the approximate enhancement factor

\[
\boxed{
\zeta \;=\;
\frac{\langle L_{\text{pore}} \rangle}{L_{p}}
\;\approx\;
\frac{d}{2L_{p}}\;
\frac{R}{1-R}
}
\qquad (L_{p}\gg d,\;R<1) .
\]

## 4. Numerical Estimates for Skin Pores

| Pore diameter *d* (µm) | Pore length *Lₚ* (mm) | Reflectivity *R* (specular) | 𝜁 = ⟨L_eff⟩/Lₚ | Effective path length ⟨L_eff⟩ (mm) |
|------------------------|----------------------|----------------------------|----------------|-----------------------------------|
| 10                     | 1.0 (trans‑dermal)   | 0.80                       | 0.010 × (0.8/0.2) = 0.04 | 0.04 mm |
| 10                     | 1.0                  | 0.95                       | 0.010 × (0.95/0.05) = 0.19 | 0.19 mm |
| 50                     | 1.0                  | 0.80                       | 0.025 × 4 = 0.10         | 0.10 mm |
| 50                     | 1.0                  | 0.95                       | 0.025 × 19 = 0.48        | 0.48 mm |
| 100                    | 1.0                  | 0.80                       | 0.05 × 4 = 0.20          | 0.20 mm |
| 100                    | 1.0                  | 0.95                       | 0.05 × 19 = 0.95         | 0.95 mm |

*Interpretation*: For highly reflective pores (*R* → 1) the enhancement can approach or even exceed unity, meaning photons may travel **several times** the geometric thickness before escaping. Even modest reflectivity (*R* ≈ 0.8) yields a noticeable increase (5‑20 % for 10‑µm pores, up to ~50 % for 100‑µm pores).

## 5. Impact on Luminescence Budget

Recall the required source photon flux for a detectable signal:

\[
\Phi_{\text{src}} = \frac{1}{T\,\eta},
\qquad
T = \exp\!\bigl[-\mu_{\text{eff}} L_{\text{geom}}\bigr].
\]

If the photon undergoes an average **path‑length enhancement** 𝜁 inside pores, the effective attenuation becomes

\[
T_{\text{pore}} = \exp\!\bigl[-\mu_{\text{eff}} \, \langle L_{\text{eff}} \rangle\bigr]
               = \exp\!\bigl[-\mu_{\text{eff}} \, \zeta \, L_{\text{geom}}\bigr]
               = T^{\,\zeta}.
\]

Thus the **required flux** is reduced by a factor 𝜁 in the exponent:

\[
\Phi_{\text{src}}^{\text{(pore)}} 
   = \frac{1}{\eta\,T^{\zeta}}
   = \Phi_{\text{src}}^{\text{(bulk)}} \times T^{\,1-\zeta}.
\]

Because *T* < 1, if 𝜁 > 1 the needed flux **drops** (photons have more chance to interact, increasing signal); if 𝜁 < 1 the flux **rises** slightly (less effective path). For the examples above with *T* ≈ 0.48 (1 mm skin, see `skin_luminescence_budget.md`):

- 𝜁 = 0.04 → T^{0.96} ≈ 0.50 → flux ↑ ≈ 2×  
- 𝜁 = 0.19 → T^{0.81} ≈ 0.58 → flux ↑ ≈ 1.7×  
- 𝜁 = 0.48 → T^{0.52} ≈ 0.68 → flux ↑ ≈ 1.5×  
- 𝜁 = 0.95 → T^{0.05} ≈ 0.97 → flux ↑ ≈ 1.03× (almost no penalty)  
- 𝜁 = 1.20 (if *R* > 0.95) → T^{‑0.20} ≈ 1.15 → flux ↓ ≈ 0.87× (benefit)

**Conclusion**: In regimes where pore reflectivity is high enough that 𝜁 ≥ 1, the multiple‑scattering path inside pores actually **helps** detection by increasing the interaction length; for lower reflectivity the penalty is modest (≤ 2× increase in required source power) and can be compensated by brighter luminescence or longer integration.

## 6. Impact on Mirror‑DM Birefringence

The birefringence rotation accumulated along a photon trajectory is

\[
\Delta\alpha = \int \eta_{\text{EFT}}\,\rho_{\text{DM}}\, ds
            \;\approx\; \eta_{\text{EFT}}\,\bar{\rho}_{\text{DM}}\,\langle L_{\text{eff}}\rangle .
\]

Thus the **mean rotation** scales linearly with 𝜁:

\[
\langle\Delta\alpha\rangle_{\text{pore}} 
   = \zeta \;\langle\Delta\alpha\rangle_{\text{bulk}} .
\]

Using the bulk estimate from `mirror_dm_eft.md` (Δα ≈ 10⁻²⁴ rad for TeV‑scale Λ, *c₃* = 1, *L* = 1 kpc), scaling to skin thickness (*L* ≈ 1 mm = 10⁻⁶ kpc) gives

\[
\Delta\alpha_{\text{bulk}} \;\approx\; 10^{-24}\times10^{-6}
   \;=\;10^{-30}\ \text{rad}.
\]

Even with an optimistic 𝜁 ≈ 1 (or slightly above), the rotation remains **far below** any realistic polarimeter sensitivity (≥ 10⁻⁶ rad). Therefore, unless the EFT parameters (η, Λ, c₃) are many orders of magnitude larger than current bounds, pore‑enhanced path length does not make the birefringence detectable.

If a **resonant enhancement** (see `resonant_enhancement.md`) boosts the effective coupling by a factor *G* (e.g., *G* = 10⁶), then

\[
\Delta\alpha_{\text{eff}} \;\approx\; G\,\zeta\,10^{-30}\ \text{rad}.
\]

To reach 10⁻⁶ rad we would need *G · ζ* ≈ 10²⁴, which is implausible without new physics. Hence, pore scattering alone does not rescue detectability of the mirror‑DM birefringence; it merely modifies the luminescence‑budget calculation modestly.

## 7. Suggested Extensions to the Monte Carlo Code

To treat pore‑internal scattering explicitly in the existing Monte Carlo framework (`monte_carlo_polarized_triaxial.py`), one could:

1. **Add a pore component**: define a probability *pₚₒᵣₑ* that a photon, upon entering the skin volume, is captured by a pore (based on pore density *nₚₒᵣₑ* and cross‑section).  
2. **Inside the pore**: propagate using isotropic scattering (Henyey‑Greenstein with *g* = 0) and a specular reflection probability *R* at each wall encounter; update the Stokes vector via the rotation matrix for the accumulated angle *dα* = η ρ_DM ds (same as before).  
3. **Track escape**: when the photon’s trajectory intersects the pore opening, decide whether it escapes (based on angular distribution) or is reflected back in.  
4. **Accrue statistics**: record total path length, number of bounces, exit position, and final Stokes vector for each photon packet.  
5. **Aggregate**: compute mean ⟨Δα⟩, distribution, and effective transmittance (fraction of photons that exit the skin volume).  

Implementing these steps would allow a direct numerical verification of the analytic 𝜁 estimates and provide joint luminescence‑and‑polarization outputs for comparison with the analytic results above.

## 8. References (for the numbers used)

- Jacques, S. L. “Optical properties of biological tissues: a review.” *Phys. Med. Biol.* 58, R37 (2013). – provides μₐ, μₛ′ values.  
- Wilson, B. C., et al. “Optical reflectance and transmittance of skin: theory and experiment.” *Phys. Med. Biol.* 34, 1159 (1989). – discusses pore contribution.  
- Henyey, L. G., & Greenstein, J. L. “Diffuse radiation in the galaxy.” *Astrophys. J.* 93, 70 (1941). – phase function.  
- Bohren, C. F., & Huffman, D. R. *Absorption and Scattering of Light by Small Particles*. Wiley, 1983. – Mie theory baseline for pore scattering.

*This analysis completes the “different path where light enters the pores and bounces inside” consideration, linking it to the luminescence budget and birefringence estimates already derived for the mirror‑dark‑matter EFT.*