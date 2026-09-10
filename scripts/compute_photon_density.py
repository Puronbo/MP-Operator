import numpy as np

# Constants
h = 6.62607015e-34  # J·s
c = 2.99792458e8    # m/s
hc = h * c          # J·m
# Source powers in W
powers_W = [1e-9, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3]  # 1 nW to 1 mW
# Wavelengths in nm
wavelengths_nm = [400, 500, 600, 700, 800]
# Skin thickness in m (assumed path length)
L = 1e-3  # 1 mm
# Cross-sectional area assumption: 1 mm^2 = 1e-6 m^2
A = 1e-6  # m^2
Volume = A * L  # m^3
# Density of tissue (approx water) for mass density conversion? Actually we compute photon mass density ργ = u/c^2
# where u is energy density (J/m^3)
# We'll compute u = (Power * residence time) / Volume
# residence time tau = L / c (time to traverse thickness)
tau = L / c
print("Photon energy density and mass density for source power P, wavelength lambda")
print("Assumptions: path length L = 1 mm, beam cross-section 1 mm^2, so volume = 1e-9 m^3")
print("Residence time tau = L/c =", tau, "s")
print()
print("Power (W) | lambda (nm) | E_photon (J) | Photon rate (s^-1) | u (J/m^3) |  rho_gamma (kg/m^3) | rho_gamma (g/cm^3)")
print("-"*100)
for P in powers_W:
    for lam in wavelengths_nm:
        lam_m = lam * 1e-9
        E_ph = hc / lam_m  # J
        photon_rate = P / E_ph  # photons per second
        u = photon_rate * E_ph * tau / Volume  # J/m^3
        rho_gamma = u / (c**2)  # kg/m^3
        rho_gamma_gcc = rho_gamma * 1e-3  # g/cm^3
        print(f"{P:.1e} | {lam:3d} | {E_ph:.2e} | {photon_rate:.2e} | {u:.2e} | {rho_gamma:.2e} | {rho_gamma_gcc:.2e}")