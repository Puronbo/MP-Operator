import numpy as np
import math

# Constants and parameters for skin layers (same as before)
epidermis_thickness = 0.01   # 0.1 mm
dermis_thickness = 0.2       # 2 mm
subcutis_thickness = 0.5     # 5 mm
total_thickness = epidermis_thickness + dermis_thickness + subcutis_thickness

def get_optical_properties(layer, wavelength_nm=600):
    wavelength_um = wavelength_nm / 1000.0
    if layer == 0:  # epidermis
        if wavelength_nm < 500:
            mu_a = 2.0
        elif wavelength_nm < 600:
            mu_a = 1.0
        else:
            mu_a = 0.5
        mu_s = 10.0 * (600 / wavelength_nm) ** 0.25
        g = 0.75
        n = 1.4
    elif layer == 1: # dermis
        mu_a = 0.3
        if 500 <= wavelength_nm <= 600:
            mu_a += 0.5 * np.exp(-((wavelength_nm - 540) ** 2) / (2 * 30 ** 2))
            mu_a += 0.3 * np.exp(-((wavelength_nm - 577) ** 2) / (2 * 30 ** 2))
        elif wavelength_nm > 600:
            mu_a += 0.2 * np.exp(-((wavelength_nm - 660) ** 2) / (2 * 40 ** 2))
        if wavelength_nm > 900:
            mu_a += 0.1 * ((wavelength_nm - 900) / 100)
        mu_s = 15.0 * (600 / wavelength_nm) ** 0.2
        g = 0.8
        n = 1.4
    else:            # subcutis
        mu_a = 0.1
        if wavelength_nm > 800:
            mu_a += 0.05 * ((wavelength_nm - 800) / 200)
        mu_s = 8.0 * (600 / wavelength_nm) ** 0.15
        g = 0.7
        n = 1.4
    return mu_a, mu_s, g, n

def mu_t(layer, wavelength_nm=600):
    mu_a, mu_s, g, n = get_optical_properties(layer, wavelength_nm)
    return mu_a + mu_s

def albedo(layer, wavelength_nm=600):
    mu_a, mu_s, g, n = get_optical_properties(layer, wavelength_nm)
    mu_tot = mu_a + mu_s
    if mu_tot > 0:
        return mu_s / mu_tot
    else:
        return 0.0

def dalpha_dsr(ds):
    eta = 1e-24
    rho_DM = 0.1
    return eta * rho_DM * ds

def rotate_stokes(S, delta_alpha):
    cos_2dal = math.cos(2.0 * delta_alpha)
    sin_2dal = math.sin(2.0 * delta_alpha)
    Q_old = S[1]
    U_old = S[2]
    S_new = np.array([
        S[0],
        Q_old * cos_2dal + U_old * sin_2dal,
        -Q_old * sin_2dal + U_old * cos_2dal,
        S[3]
    ])
    return S_new

def sample_henyey_greenstein(g):
    if abs(g) < 1e-6:
        return np.random.uniform(-1, 1)
    else:
        xi = np.random.uniform(0, 1)
        denominator = 1 - g + 2 * g * xi
        cos_theta = (1 + g**2 - ((1 - g**2) / denominator)**2) / (2 * g)
        if cos_theta > 1:
            cos_theta = 1
        elif cos_theta < -1:
            cos_theta = -1
        return cos_theta

def random_unit_vector():
    costheta = np.random.uniform(-1, 1)
    phi = np.random.uniform(0, 2*math.pi)
    sintheta = math.sqrt(1 - costheta**2)
    return np.array([sintheta * math.cos(phi), sintheta * math.sin(phi), costheta])

def get_layer(z):
    if z < 0:
        return -1  # above epidermis (air)
    elif z < epidermis_thickness:
        return 0   # epidermis
    elif z < epidermis_thickness + dermis_thickness:
        return 1   # dermis
    elif z < total_thickness:
        return 2   # subcutis
    else:
        return 3   # below subcutis

def simulate_photon_tracking(wavelength_nm=600):
    """Returns energy deposited per layer (J) for a single photon."""
    z0 = epidermis_thickness + np.random.uniform(0, dermis_thickness)
    r = np.array([0.0, 0.0, z0])
    v = random_unit_vector()
    S = np.array([1.0, 1.0, 0.0, 0.0])
    h = 6.62607015e-34
    c = 2.99792458e8
    hc = h * c
    lam_m = wavelength_nm * 1e-9
    E_photon = hc / lam_m
    energy_per_layer = np.zeros(3)  # epidermis, dermis, subcutis
    while True:
        layer = get_layer(r[2])
        if layer == -1:
            return energy_per_layer
        elif layer == 3:
            return energy_per_layer
        mu_a, mu_s, g, n = get_optical_properties(layer, wavelength_nm)
        mu_tot = mu_a + mu_s
        if mu_tot <= 0:
            ds = 1.0
            r = r + v * ds
            continue
        xi = np.random.uniform(0, 1)
        while xi == 0:
            xi = np.random.uniform(0, 1)
        ds = -math.log(xi) / mu_tot
        r_new = r + v * ds
        dalpha = dalpha_dsr(ds)
        S = rotate_stokes(S, dalpha)
        r = r_new
        layer_new = get_layer(r[2])
        if layer_new == -1:
            return energy_per_layer
        elif layer_new == 3:
            return energy_per_layer
        # Energy deposited along step (continuous slowing down) for the current layer
        # Deposit at midpoint
        r_mid = r + v * (ds / 2.0)
        z_mid = r_mid[2]
        if 0 <= z_mid < total_thickness:
            # Determine which layer the midpoint belongs to (should be same as current layer unless we crossed boundary mid-step)
            layer_mid = get_layer(z_mid)
            if layer_mid >= 0 and layer_mid < 3:
                energy_per_layer[layer_mid] += E_photon * mu_a * ds
        # Interaction
        if np.random.uniform(0, 1) < albedo(layer, wavelength_nm):
            # Scattering
            cos_theta = sample_henyey_greenstein(g)
            phi = np.random.uniform(0, 2*math.pi)
            sin_theta = math.sqrt(1 - cos_theta**2)
            if abs(v[2]) < 0.9:
                v1 = np.array([0.0, 0.0, 1.0])
            else:
                v1 = np.array([0.0, 1.0, 0.0])
            v1 = v1 - np.dot(v1, v) * v
            v1_norm = np.linalg.norm(v1)
            if v1_norm < 1e-10:
                v1 = np.array([1.0, 0.0, 0.0])
                v1 = v1 - np.dot(v1, v) * v
                v1_norm = np.linalg.norm(v1)
            v1 = v1 / v1_norm
            v2 = np.cross(v, v1)
            v_new = sin_theta * (math.cos(phi) * v1 + math.sin(phi) * v2) + cos_theta * v
            v = v_new / np.linalg.norm(v_new)
        else:
            # Absorption: photon dies after depositing energy along step (already accounted)
            return energy_per_layer

def run_simulation(wavelength_nm, N_photons):
    energy_per_layer_total = np.zeros(3)  # epidermis, dermis, subcutis
    for i in range(N_photons):
        energy_per_layer = simulate_photon_tracking(wavelength_nm)
        energy_per_layer_total += energy_per_layer
        if (i+1) % 10000 == 0:
            print(f"  {i+1} photons processed")
    return energy_per_layer_total

if __name__ == "__main__":
    print("Computing strand-specific energy deposition...")
    wavelengths = [450, 550, 650]  # nm
    N_photons = 20000  # per wavelength
    results = {}
    # Strand fractions per layer (illustrative)
    # Epidermis: melanin 100%
    # Dermis: hemoglobin 40%, collagen 60%
    # Subcutis: elastin 70%, collagen 30%
    strand_fractions = {
        'epidermis': {'melanin': 1.0},
        'dermis': {'hemoglobin': 0.4, 'collagen': 0.6},
        'subcutis': {'elastin': 0.7, 'collagen': 0.3}
    }
    for wl in wavelengths:
        print(f"\nWavelength {wl} nm:")
        energy_per_layer_J = run_simulation(wl, N_photons)
        results[wl] = {
            'epidermis_J': energy_per_layer_J[0],
            'dermis_J': energy_per_layer_J[1],
            'subcutis_J': energy_per_layer_J[2]
        }
        print(f"  Epidermis energy: {energy_per_layer_J[0]:.6e} J")
        print(f"  Dermis energy: {energy_per_layer_J[1]:.6e} J")
        print(f"  Subcutis energy: {energy_per_layer_J[2]:.6e} J")
    # Compute strand-specific energies
    print("\n--- Strand-Specific Energy Deposition (Illustrative Fractions) ---")
    print("Assuming fractions:")
    print("  Epidermis: melanin 100%")
    print("  Dermis: hemoglobin 40%, collagen 60%")
    print("  Subcutis: elastin 70%, collagen 30%")
    print("\nWavelength (nm) | Strand | Energy (J) | Fraction of Total Deposited Energy")
    print("----------------|--------|------------|-----------------------------------")
    with open('strand_specific_dose.md', 'w', encoding='utf-8') as f:
        f.write("# Strand-Specific Photon Energy Deposition\n\n")
        f.write("## Assumptions\n\n")
        f.write("- Beam cross-sectional area: 1 mm² (0.01 cm²)\n")
        f.write("- Monte Carlo photons per wavelength: 20,000\n")
        f.write("- Strand fractions (illustrative):\n")
        f.write("  - Epidermis: melanin 100%\n")
        f.write("  - Dermis: hemoglobin 40%, collagen 60%\n")
        f.write("  - Subcutis: elastin 70%, collagen 30%\n")
        f.write("- Energy deposited per layer obtained from Monte Carlo simulation with continuous slowing down approximation.\n\n")
        f.write("## Results\n\n")
        f.write("| Wavelength (nm) | Strand | Energy Deposited (J) | Fraction of Total Deposited Energy |\n")
        f.write("|-----------------|--------|----------------------|------------------------------------|\n")
        for wl in wavelengths:
            total_energy = results[wl]['epidermis_J'] + results[wl]['dermis_J'] + results[wl]['subcutis_J']
            # Epidermis strands
            epi_frac = strand_fractions['epidermis']
            for strand, frac in epi_frac.items():
                energy = results[wl]['epidermis_J'] * frac
                frac_of_total = energy / total_energy if total_energy > 0 else 0
                f.write(f"| {wl} | {strand} | {energy:.6e} | {frac_of_total:.6f} |\n")
            # Dermis strands
            derm_frac = strand_fractions['dermis']
            for strand, frac in derm_frac.items():
                energy = results[wl]['dermis_J'] * frac
                frac_of_total = energy / total_energy if total_energy > 0 else 0
                f.write(f"| {wl} | {strand} | {energy:.6e} | {frac_of_total:.6f} |\n")
            # Subcutis strands
            sub_frac = strand_fractions['subcutis']
            for strand, frac in sub_frac.items():
                energy = results[wl]['subcutis_J'] * frac
                frac_of_total = energy / total_energy if total_energy > 0 else 0
                f.write(f"| {wl} | {strand} | {energy:.6e} | {frac_of_total:.6f} |\n")
        f.write("\n")
        f.write("## Notes\n\n")
        f.write("- The fractions are illustrative and not based on actual mass attenuation coefficients from NIST XCOM. For a precise calculation, one would need the mass attenuation coefficients (μ/ρ) for each biochemical strand at the given wavelengths and the weight fractions within each layer.\n")
        f.write("- The simulation tracks energy deposition per layer; splitting by strand is a post-processing step based on assumed fractions.\n")
        f.write("- Future work could integrate strand-specific absorption coefficients into the optical property model.\n")
    print("\nResults written to strand_specific_dose.md")