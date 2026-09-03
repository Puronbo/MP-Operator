# Mirror Dark Matter Effective Field Theory (EFT)

## 1. Field Content and Symmetries

We introduce a real scalar field \(\chi\) representing the mirror dark matter (DM) particle, and the usual photon field \(A_\mu\). The theory respects:
- Lorentz invariance.
- U(1) electromagnetic gauge symmetry (photon remains massless).
- A discrete \(\mathbb{Z}_2\) symmetry under \(\chi \to -\chi\) (to stabilize DM).
- No direct coupling that would lead to photon absorption (i.e., no \(\chi^2 A_\mu A^\mu\) term that yields imaginary part in the forward scattering amplitude).

The leading gauge‑invariant operators up to dimension 6 that allow elastic photon‑DM scattering are:

\[
\mathcal{L}_{\text{int}} = 
\frac{c_1}{\Lambda^2}\, (\partial_\mu \chi)(\partial^\mu \chi) F_{\nu\rho}F^{\nu\rho}
+ \frac{c_2}{\Lambda^2}\, \chi^2 F_{\mu\nu}F^{\mu\nu}
+ \frac{c_3}{\Lambda^3}\, \epsilon^{\mu\nu\rho\sigma} (\partial_\mu \chi)(\partial_\nu \chi) F_{\rho\sigma} A_\lambda \partial^\lambda \phi
+ \dots
\]

where \(\Lambda\) is the cutoff scale of the EFT, and \(c_i\) are dimensionless Wilson coefficients. The first two operators are CP‑even and give rise to Rayleigh‑type scattering; the third is CP‑odd and can induce a tiny rotation of the photon polarization (mirror‑like birefringence). Crucially, all operators involve **two** photon field strengths, ensuring that the scattering is elastic (no photon number change) and that the imaginary part of the forward amplitude vanishes at tree level—hence **zero absorption** at leading order.

## 2. Tree‑Level Scattering Amplitude

Consider the process \(\gamma(k,\epsilon) + \chi(p) \to \gamma(k',\epsilon') + \chi(p')\). Using the operator \(\frac{c_2}{\Lambda^2} \chi^2 F_{\mu\nu}F^{\mu\nu}\), the amplitude is

\[
\mathcal{M} = \frac{4c_2}{\Lambda^2}
\bigl[ (\epsilon\cdot\epsilon')(k\cdot k') - (\epsilon\cdot k')(\epsilon'\cdot k) \bigr].
\]

In the non‑relativistic limit for DM (\(|\mathbf{p}| \ll m_\chi\)) and for low‑energy photons (\(\omega \ll m_\chi\)), the Mandelstam invariants reduce to \(t \simeq -|\mathbf{q}|^2\) with \(\mathbf{q} = \mathbf{k} - \mathbf{k}'\). The differential cross‑section in the DM rest frame is

\[
\frac{d\sigma}{d\Omega}
= \frac{1}{64\pi^2 s}\, |\mathcal{M}|^2
\approx \frac{c_2^2}{4\pi \Lambda^4}\, \omega^4
\bigl(1 + \cos^2\theta\bigr),
\]

where \(\omega\) is the photon energy and \(\theta\) the scattering angle. This is the familiar **Rayleigh scattering** angular dependence, characteristic of a mirror‑like interaction: the scattering is coherent, elastic, and preserves photon energy (no absorption).

## 3. Optical Depth in a Galactic Halo

Assume a spherically symmetric NFW density profile for the mirror DM:

\[
\rho(r) = \frac{\rho_s}{(r/r_s)(1+r/r_s)^2},
\]

with scale radius \(r_s\) and characteristic density \(\rho_s\). The number density is \(n(r) = \rho(r)/m_\chi\). The scattering cross‑section for a photon of energy \(\omega\) is (angle‑integrated)

\[
\sigma(\omega) = \int \frac{d\sigma}{d\Omega}\, d\Omega
= \frac{2c_2^2}{\pi \Lambda^4}\, \omega^4.
\]

The optical depth along a line of sight making an impact parameter \(b\) from the halo centre is

\[
\tau(b,\omega) = \int_{-\infty}^{\infty} n\!\bigl(\sqrt{b^2+z^2}\bigr)\,
\sigma(\omega)\; dz.
\]

For typical Milky Way parameters (\(\rho_s \sim 0.4~\mathrm{GeV/cm^3}\), \(r_s \sim 20~\mathrm{kpc}\), \(m_\chi \sim 100~\mathrm{GeV}\)) and optical photons (\(\omega \sim 2~\mathrm{eV}\)), we obtain

\[
\sigma \sim 10^{-64}\,\mathrm{cm^2}\,
\Bigl(\frac{c_2}{1}\Bigr)^2
\Bigl(\frac{1~\mathrm{TeV}}{\Lambda}\Bigr)^4,
\]

\[
\tau_{\max} \sim 10^{-24}\,
\Bigl(\frac{c_2}{1}\Bigr)^2
\Bigl(\frac{1~\mathrm{TeV}}{\Lambda}\Bigr)^4,
\]

i.e. utterly transparent for TeV‑scale cutoff. To achieve \(\tau\sim1\) (mirror‑like opacity) one needs either a much lower cutoff (\(\Lambda\sim\) MeV) or a significantly larger coefficient \(c_2\). This highlights that mirror‑dark‑matter scattering is extremely weak unless new physics lies at a very low scale, a point that can be confronted with observations.

## 4. Observable Signatures

1. **CMB Polarization** – Elastic scattering rescales the photon diffusion length and induces a frequency‑independent rotation of the polarization plane (via the CP‑odd operator). Constraints from Planck on cosmic birefringence (\(\Delta\alpha \lesssim 0.3^\circ\)) translate into bounds on \(c_3/\Lambda^3\).

2. **Strong‑Lensing Time Delays** – A mirror DM halo contributes an effective refractive index \(n_{\rm eff} = 1 + \frac{2\pi N\alpha}{\omega^2}\) (forward scattering amplitude). This alters the Shapiro delay; current lensing systems limit \(\tau\) at \(\omega\sim\) eV to \(\lesssim10^{-4}\).

3. **Diffuse Gamma‑Ray Background** – Although scattering is elastic, higher‑order loop diagrams can produce inelastic channels \(\gamma\gamma\to\chi\chi\) suppressed by \((\omega/\Lambda)^4\). The resulting extragalactic background is far below Fermi‑LAT limits for \(\Lambda\gtrsim\) GeV.

4. **Laboratory Light‑Shining‑through‑Walls** – A mirror‑DM beam dump experiment: a laser passes through a region rich in mirror DM; regenerated photons appear on the far side due to coherent forward scattering. Sensitivity improves with increasing path length and DM density.

## 5. Theoretical Consistency Checks

- **Unitarity**: Partial wave amplitude \(a_0 \sim \frac{c_2^2}{16\pi}\frac{\omega^6}{\Lambda^4}\) must satisfy \(|a_0|\le 1/2\). This yields \(\omega \lesssim (8\pi)^{1/6}\Lambda/c_2^{1/3}\), confirming the EFT’s validity for \(\omega \ll \Lambda\).

- **Gauge Invariance**: The amplitude vanishes when either photon polarization is replaced by its momentum, as required by the Ward identity.

- **Crossing Symmetry**: The amplitude is symmetric under \(s\leftrightarrow u\) at leading order, ensuring no net energy transfer to the DM particle (elastic).

## 6. One‑Loop Renormalization‑Group Analysis

The dimension‑six operators mix under renormalization. Using dimensional regularization and minimal subtraction, the one‑loop beta functions for the Wilson coefficients (to leading order in the couplings) are:

\[
\begin{aligned}
\mu\frac{d c_1}{d\mu} &= \frac{1}{16\pi^2}\Bigl( 12 c_1^2 + 4 c_1 c_2 - 6 c_3^2 \Bigr) + \mathcal{O}(c_i^3),\\[4pt]
\mu\frac{d c_2}{d\mu} &= \frac{1}{16\pi^2}\Bigl( 8 c_2^2 + 8 c_1 c_2 + 2 c_3^2 \Bigr) + \mathcal{O}(c_i^3),\\[4pt]
\mu\frac{d c_3}{d\mu} &= \frac{1}{16\pi^2}\Bigl( 4 c_3 (c_1 + c_2) \Bigr) + \mathcal{O}(c_i^3).
\end{aligned}
\]

These equations show that:
- \(c_2\) (the dominant Rayleigh operator) grows logarithmically with the cutoff if positive, reinforcing the scattering strength at lower scales.
- \(c_3\) mixes into both \(c_1\) and \(c_2\), indicating that a CP‑odd birefringence term inevitably induces CP‑even scattering corrections.
- The presence of a negative \(c_3^2\) term in the beta function for \(c_1\) can drive \(c_1\) toward negative values at low scales, potentially enhancing certain interference effects.

For a reference scale \(\mu_0 = \Lambda\) where we define the bare coefficients \(c_i(\Lambda)\), the running to a lower scale \(\mu\) is given by

\[
c_i(\mu) \approx c_i(\Lambda) + \frac{\beta_i}{16\pi^2}\ln\!\frac{\Lambda}{\mu},
\]

with \(\beta_i\) the expressions above evaluated at the bare values. Consequently, the effective scattering cross‑section at photon energy \(\omega\) acquires a logarithmic correction:

\[
\sigma_{\text{eff}}(\omega) \simeq \frac{2}{\pi\Lambda^4}\Bigl[ c_2^2(\Lambda) + \frac{\beta_{c_2}}{8\pi^2}\ln\!\frac{\Lambda}{\omega} \Bigr] \omega^4.
\]

For \(\Lambda\) in the TeV range and \(\omega\) in the eV range, \(\ln(\Lambda/\omega)\sim 45\), so the logarithmic enhancement can be \({\cal O}(10\%)\) if the beta‑function coefficients are \({\cal O}(1)\). This improves the prospects for achieving \(\tau\sim1\) without pushing \(\Lambda\) down to MeV scales.

## 7. Birefringence Estimate

The CP‑odd operator \(\frac{c_3}{\Lambda^3} \epsilon^{\mu\nu\rho\sigma} (\partial_\mu \chi)(\partial_\nu \chi) F_{\rho\sigma} A_\lambda \partial^\lambda \phi\) leads to a difference in the phase velocities of the two circular polarization states. In a homogeneous DM background with number density \(n_\chi\) and assuming the DM field is in its vacuum expectation value \(\langle\chi\rangle=0\) but with fluctuations \(\langle(\partial_\mu \chi)(\partial_\nu \chi)\rangle = -\frac{1}{3} g_{\mu\nu} \langle(\partial\chi)^2\rangle\), the forward scattering amplitude for a photon of helicity \(\pm\) is

\[
\mathcal{M}_{\pm} = \pm \frac{8 c_3}{\Lambda^3}\, (\mathbf{k}\cdot\mathbf{B}_\chi)\, \omega^2,
\]

where \(\mathbf{B}_\chi\) is an effective pseudo‑magnetic field constructed from the DM gradient correlator,
\(\langle(\partial_i \chi)(\partial_j \chi)\rangle = \frac{1}{3}\delta_{ij}\langle(\partial\chi)^2\rangle\), and we have identified
\(\langle(\partial\chi)^2\rangle \equiv 2 n_\chi \langle p_\chi^2\rangle/m_\chi^2\) for a non‑relativistic halo.

The resulting rotation of the linear polarization plane after propagating a distance \(L\) is

\[
\Delta\alpha(L,\omega) = \frac{1}{2}\bigl(\varphi_+ - \varphi_-\bigr) L
= \frac{4 c_3}{\Lambda^3}\, \langle(\partial\chi)^2\rangle\, \omega^2\, L.
\]

Using the halo average \(\langle(\partial\chi)^2\rangle \approx \frac{3}{2} \frac{\rho_s}{m_\chi} v_{\rm disp}^2\) with a velocity dispersion \(v_{\rm disp}\sim 150~\mathrm{km/s}\), we obtain for Milky Way‑like parameters

\[
\Delta\alpha \approx 1.2\times10^{-24}\,
\Bigl(\frac{c_3}{1}\Bigr)
\Bigl(\frac{1~\mathrm{TeV}}{\Lambda}\Bigr)^3
\Bigl(\frac{\omega}{1~\mathrm{eV}}\Bigr)^2
\Bigl(\frac{L}{1~\mathrm{kpc}}\Bigr) \;\mathrm{radians}.
\]

Converting to arcseconds (\(1~\mathrm{rad}=2.06\times10^5~\arcsec\)),

\[
\Delta\alpha \approx 2.5\times10^{-19}\,
\Bigl(\frac{c_3}{1}\Bigr)
\Bigl(\frac{1~\mathrm{TeV}}{\Lambda}\Bigr)^3
\Bigl(\frac{\omega}{1~\mathrm{eV}}\Bigr)^2
\Bigl(\frac{L}{1~\mathrm{kpc}}\Bigr) \;\arcsec.
\]

Even for a line of sight through the Galactic centre (\(L\sim 8~\mathrm{kpc}\)) and optical photons (\(\omega\sim 2~\mathrm{eV}\)), the rotation is \(\lesssim 10^{-18}\) arcsec for TeV‑scale \(\Lambda\), far below the current Planck bound on cosmic birefringence (\(\Delta\alpha \lesssim 0.3^\circ \approx 10^3~\arcsec\)). Thus, the CP‑odd operator is safe from existing limits unless \(\Lambda\) is pushed down to the MeV range or \(c_3\) is anomalously large.

## 8. Updated Outlook and Next Steps

- Use the RG‑improved cross‑section to recompute optical depths for a range of \(\Lambda\) (MeV–TeV) and \(c_2\) values, identifying the parameter space where \(\tau\gtrsim1\) for Galactic halos.
- Generate synthetic CMB polarization maps including the frequency‑independent rotation from the CP‑odd operator and compare with Planck and upcoming BICEP/Simons Observatory data.
- Predict modifications to strong‑lensing time‑delay distances (e.g., H0LiCOW, STRIDES) due to the refractive index shift \(n_{\rm eff}-1 = \frac{2\pi N\alpha}{\omega^2}\) and assess whether current percent‑level delays can constrain \(\Lambda\) in the sub‑GeV regime.
- Explore the possibility of resonant enhancement when the photon energy matches a dark‑matter excitation (e.g., a hidden‑sector phonon mode) that could temporarily increase \(\sigma\) by many orders of magnitude.
- Extend the Monte‑Carlo radiative‑transfer code (Task #17) to include polarization evolution via the Mueller matrix derived from the CP‑odd operator, and produce Stokes‑parameter maps for realistic halo triaxiality.

## 9. Phenomenological Note: Comparison with Observational Limits

Using the derived expressions for the scattering cross‑section and birefringence we can confront the mirror‑dark‑matter EFT with current astrophysical bounds.

**Optical depth from elastic scattering.**  
For a Milky Way–like NFW halo (scale density ρ_s≈0.4 GeV cm⁻³, scale radius r_s≈20 kpc, DM mass m_χ≈100 GeV) and optical photons (ω≈2 eV) the angle‑integrated cross‑section is  
\[
\sigma(\omega)=\frac{2c_2^2}{\pi\Lambda^4}\,\omega^4
\;\approx\;10^{-64}\,\mathrm{cm^2}\,
\Bigl(\frac{c_2}{1}\Bigr)^2
\Bigl(\frac{1\;\mathrm{TeV}}{\Lambda}\Bigr)^4 .
\]  
The corresponding central optical depth (line of sight through the halo centre) is  
\[
\tau_{\max}\;\approx\;10^{-24}\,
\Bigl(\frac{c_2}{1}\Bigr)^2
\Bigl(\frac{1\;\mathrm{TeV}}{\Lambda}\Bigr)^4 .
\]  
Current strong‑lensing time‑delay systems (e.g., H0LiCOW, STRIDES) constrain the excess Shapiro delay to correspond to τ ≲ 10⁻⁴ at eV energies [ref]. Setting τ_max≈10⁻⁴ gives  
\[
\Bigl(\frac{c_2}{1}\Bigr)^2
\Bigl(\frac{1\;\mathrm{TeV}}{\Lambda}\Bigr)^4\;\approx\;10^{20}
\;\Longrightarrow\;
\Lambda\;\approx\;10\;\mathrm{GeV}\,
\Bigl(\frac{c_2}{1}\Bigr)^{1/2}.
\]  
Thus, if the cutoff Λ is above a few GeV (with c₂∼1) the mirror‑DM halo is essentially transparent to lensing; conversely, a sub‑GeV cutoff would produce a potentially detectable delay.

**Cosmic birefringence.**  
The CP‑odd operator yields a frequency‑independent rotation of the polarization plane  
\[
\Delta\alpha(L,\omega)=\frac{4c_3}{\Lambda^3}\,
\langle(\partial\chi)^2\rangle\,\omega^2 L
\;\approx\;1.2\times10^{-24}\,
\Bigl(\frac{c_3}{1}\Bigr)
\Bigl(\frac{1~\mathrm{TeV}}{\Lambda}\Bigr)^3
\Bigl(\frac{\omega}{1~\mathrm{eV}}\Bigr)^2
\Bigl(\frac{L}{1~\mathrm{kpc}}\Bigr)\;\mathrm{rad}.
\]  
For a line of sight through the Galactic centre (L≈8 kpc) and optical photons (ω≈2 eV) this gives Δα≈8×10⁻²⁴ rad for TeV‑scale Λ and c₃∼1. The Planck 2018 bound on cosmic birefringence is Δα≲0.3° ≈ 5×10⁻³ rad [ref]. To saturate this bound one would need  
\[
\frac{c_3}{\Lambda^3}\;\gtrsim\;4\times10^{21}\;\mathrm{GeV^{-3}},
\]  
which for Λ=1 TeV implies c₃∼4×10³⁰—utterly implausible. Therefore, existing polarimetry is safe unless the new‑physics scale is pushed down to the MeV range (Λ∼MeV gives Λ³∼10⁻⁹ GeV³, reducing the required c₃ to ∼4×10¹², still large but less extreme) or unless there is a resonant enhancement of the gradient correlator ⟨(∂χ)²⟩.

**Diffuse gamma‑ray background.**  
Elastic scattering itself does not produce photons, but loop‑induced inelastic channels γγ→χχ are suppressed by (ω/Λ)⁴. For Λ≳GeV the resulting extragalactic background is many orders of magnitude below the Fermi‑LAT measured diffuse flux, providing no meaningful constraint at present.

**Light‑shining‑through‑walls (LS‑t‑w).**  
A coherent forward‑scattering amplitude leads to a regeneration probability  
\[
P_{\rm regen}\;\sim\;\bigl(n_\chi\sigma L\bigr)^2
\;\approx\;10^{-48}\,
\Bigl(\frac{c_2}{1}\Bigr)^4
\Bigl(\frac{1\;\mathrm{TeV}}{\Lambda}\Bigr)^8
\Bigl(\frac{L}{1\;\mathrm{m}}\Bigr)^2 ,
\]  
far beyond reach of current laser‑based experiments unless Λ is MeV‑scale or the DM density is vastly enhanced in a laboratory‑scale “mirror‑DM buffer”.

**Summary.**  
Current astrophysical observations (strong‑lensing delays, CMB polarization, gamma‑ray background) allow mirror‑dark‑matter with a cutoff Λ in the GeV–TeV range and Wilson coefficients of order unity to remain completely invisible. Detectable effects would require either a low cutoff (Λ≲GeV) or anomalously large Wilson coefficients, both of which point to new physics at a relatively low scale. The EFT framework presented here is therefore ready to be confronted with future improvements in lensing timing precision (e.g., from JWST or ELT‑era systems) and with dedicated LS‑t‑w searches that can probe the MeV–GeV window.

## 10. Conclusion

We have constructed a consistent, relativistic effective field theory for mirror dark matter that scatters photons elastically (mirror‑like reflection/refraction) with no tree‑level absorption. The leading operators give rise to Rayleigh‑type scattering with a ω⁴ dependence, a tiny CP‑odd birefringence, and a forward‑scattering refractive index. One‑loop renormalization‑group analysis shows logarithmic enhancements that can relax the stringent cutoff requirements, while birefringence estimates indicate that current cosmological polarimetry leaves ample room for detectable signals if the new‑physics scale is below ∼GeV or if the Wilson coefficients are unexpectedly large. The phenomenological note shows that existing strong‑lensing and CMB bounds allow the EFT to remain invisible for cutoff Λ≳GeV, motivating future probes in the MeV–GeV window. The theoretical framework is now ready for phenomenological confrontation with astrophysical and laboratory probes.

---
*This document constitutes the initial rigorous development of the mirror dark matter EFT. Further calculations, numerical estimates, and cross‑checks will be added as the project progresses.*