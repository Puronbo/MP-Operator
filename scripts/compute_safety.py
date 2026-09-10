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

def simulate_photon_deposition(wavelength_nm=600):
    """Returns energy deposited (J) for a single photon."""
    z0 = epidermis_thickness + np.random.uniform(0, dermis_thickness)
    r = np.array([0.0, 0.0, z0])
    v = random_unit_vector()
    S = np.array([1.0, 1.0, 0.0, 0.0])
    h = 6.62607015e-34
    c = 2.99792458e8
    hc = h * c
    lam_m = wavelength_nm * 1e-9
    E_photon = hc / lam_m
    energy_deposited = 0.0
    while True:
        layer = get_layer(r[2])
        if layer == -1:
            return energy_deposited
        elif layer == 3:
            return energy_deposited
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
            return energy_deposited
        elif layer_new == 3:
            return energy_deposited
        # Energy deposited along step (continuous slowing down)
        # Deposit at midpoint
        r_mid = r + v * (ds / 2.0)
        z_mid = r_mid[2]
        if 0 <= z_mid < total_thickness:
            energy_deposited += E_photon * mu_a * ds
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
            return energy_deposited

def run_simulation(wavelength_nm, N_photons):
    total_energy = 0.0
    for i in range(N_photons):
        total_energy += simulate_photon_deposition(wavelength_nm)
        if (i+1) % 10000 == 0:
            print(f"  {i+1} photons processed")
    return total_energy

if __name__ == "__main__":
    print("Computing photon energy deposition fraction for safety comparison...")
    wavelengths = [450, 550, 650]  # nm
    N_photons = 20000  # per wavelength for stats
    results = {}
    for wl in wavelengths:
        print(f"\nWavelength {wl} nm:")
        total_energy_J = run_simulation(wl, N_photons)
        h = 6.62607015e-34
        c = 2.99792458e8
        hc = h * c
        lam_m = wl * 1e-9
        E_photon = hc / lam_m
        fraction = total_energy_J / (N_photons * E_photon)
        results[wl] = {
            'total_energy_J': total_energy_J,
            'E_photon_J': E_photon,
            'fraction': fraction
        }
        print(f"  Total energy deposited: {total_energy_J:.6e} J")
        print(f"  Photon energy: {E_photon:.6e} J")
        print(f"  Fraction deposited: {fraction:.6e}")
    # Safety thresholds
    # Assume skin thermal damage threshold: H_th = 10 J/cm² (for exposure > 10 s)
    H_th = 10.0  # J/cm²
    # Beam area: 1 mm² = 0.01 cm²
    area_cm2 = 0.01
    # Consider a range of source powers: 1 nW to 1 mW
    powers_W = [1e-9, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3]
    print("\n--- Safety Comparison ---")
    print("Assuming beam area = 1 mm² (0.01 cm²), thermal damage threshold = 10 J/cm².")
    print("Wavelength (nm) | Power (W) | Irradiance (W/cm²) | Deposited Power Density (W/cm²) | Time to Threshold (s)")
    print("----------------|-----------|--------------------|---------------------------------|----------------------")
    for wl in wavelengths:
        frac = results[wl]['fraction']
        for P in powers_W:
            irradiance = P / area_cm2  # W/cm²
            deposited_power_density = frac * irradiance  # W/cm²
            if deposited_power_density > 0:
                t_threshold = H_th / deposited_power_density  # s
            else:
                t_threshold = float('inf')
            print(f"{wl:13} | {P:.1e} | {irradiance:.6e} | {deposited_power_density:.6e} | {t_threshold:.2e}")
    # Write to markdown
    with open('dose_safety_comparison.md', 'w', encoding='utf-8') as f:
        f.write("# Dose Safety Comparison\n\n")
        f.write("## Assumptions\n\n")
        f.write("- Beam cross-sectional area: 1 mm² (0.01 cm²)\n")
        f.write("- Tissue density: 1 g/cm³ (1000 kg/m³)\n")
        f.write("- Skin thermal damage threshold: 10 J/cm² (for exposure durations >10 s, based on IEC 62471/ANSI Z136.1)\n")
        f.write("- Photon energy deposition fraction from Monte Carlo simulation (20k photons per wavelength).\n\n")
        f.write("## Deposition Fractions\n\n")
        f.write("| Wavelength (nm) | Photon Energy (J) | Deposition Fraction |\n")
        f.write("|-----------------|-------------------|---------------------|\n")
        for wl in wavelengths:
            f.write(f"| {wl} | {results[wl]['E_photon_J']:.6e} | {results[wl]['fraction']:.6e} |\n")
        f.write("\n")
        f.write("## Time to Reach Thermal Damage Threshold (10 J/cm²)\n\n")
        f.write("Assuming continuous wave illumination.\n\n")
        f.write("| Wavelength (nm) | Source Power (W) | Irradiance (W/cm²) | Deposited Power Density (W/cm²) | Time to Threshold (s) |\n")
        f.write("|-----------------|------------------|--------------------|---------------------------------|----------------------|\n")
        for wl in wavelengths:
            frac = results[wl]['fraction']
            for P in powers_W:
                irradiance = P / area_cm2
                deposited_power_density = frac * irradiance
                if deposited_power_density > 0:
                    t_threshold = H_th / deposited_power_density
                else:
                    t_threshold = float('inf')
                f.write(f"| {wl} | {P:.1e} | {irradiance:.6e} | {deposited_power_density:.6e} | {t_threshold:.2e} |\n")
        f.write("\n")
        f.write("## Notes\n\n")
        f.write("- The deposition fraction includes all energy deposited via absorption (continuous slowing down approximation).\n")
        f.write("- Scattering does not deposit energy directly but increases path length, potentially increasing absorption.\n")
        f.write("- The threshold of 10 J/cm² is a conservative estimate for thermal damage; actual thresholds may vary with wavelength and exposure duration.\n")
        f.write("- For pulsed lasers, different limits apply.\n")
        f.write("- The simulation does not account for secondary electron transport or thermal diffusion.\n")
    print("\nResults written to dose_safety_comparison.md")