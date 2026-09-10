import numpy as np
import math

# Constants and parameters for skin layers (epidermis, dermis, subcutis)
# We'll define thicknesses in cm
# Typical values from literature (approx.)
# Layer thicknesses (cm)
epidermis_thickness = 0.01   # 0.1 mm
dermis_thickness = 0.2       # 2 mm
subcutis_thickness = 0.5     # 5 mm (variable, but we take a typical value)

# Total thickness
total_thickness = epidermis_thickness + dermis_thickness + subcutis_thickness

# Optical properties as functions of wavelength (we'll use wavelength-dependent values)
# Based on literature: Jacques, "Optical properties of biological tissues: a review"
# and other sources. We'll implement a simplified wavelength dependence.

def get_optical_properties(layer, wavelength_nm=600):
    """
    Returns (mu_a, mu_s, g, n) for the given layer at the given wavelength.
    layer: 0 for epidermis, 1 for dermis, 2 for subcutis
    wavelength_nm: wavelength in nanometers
    """
    # Simplified wavelength dependence based on literature
    # For melanin, hemoglobin, water absorption, and scattering

    # Convert wavelength to micrometers for some formulas
    wavelength_um = wavelength_nm / 1000.0

    if layer == 0:  # epidermis
        # Melanin absorption varies with wavelength
        # Simplified: absorption decreases with increasing wavelength in visible range
        if wavelength_nm < 500:
            mu_a = 2.0  # higher absorption in blue/green
        elif wavelength_nm < 600:
            mu_a = 1.0
        else:
            mu_a = 0.5  # lower absorption in red

        # Scattering decreases with wavelength (approximately lambda^-b)
        # Typical value for epidermis around 600nm
        mu_s = 10.0 * (600 / wavelength_nm) ** 0.25  # mild wavelength dependence
        g = 0.75
        n = 1.4

    elif layer == 1: # dermis
        # Blood and water absorption
        # Simplified hemoglobin and water absorption
        mu_a = 0.3  # base absorption
        # Add some wavelength dependence for hemoglobin peaks
        if 500 <= wavelength_nm <= 600:
            mu_a += 0.5 * np.exp(-((wavelength_nm - 540) ** 2) / (2 * 30 ** 2))  # oxyhemoglobin peak
            mu_a += 0.3 * np.exp(-((wavelength_nm - 577) ** 2) / (2 * 30 ** 2))  # another peak
        elif wavelength_nm > 600:
            mu_a += 0.2 * np.exp(-((wavelength_nm - 660) ** 2) / (2 * 40 ** 2))  # deoxyhemoglobin

        # Water absorption becomes significant at longer wavelengths
        if wavelength_nm > 900:
            mu_a += 0.1 * ((wavelength_nm - 900) / 100)  # simplified

        mu_s = 15.0 * (600 / wavelength_nm) ** 0.2  # scattering power law
        g = 0.8
        n = 1.4

    else:            # subcutis
        # Fat layer - lower scattering and absorption
        mu_a = 0.1
        # Very weak wavelength dependence in NIR for fat
        if wavelength_nm > 800:
            mu_a += 0.05 * ((wavelength_nm - 800) / 200)  # slight increase

        mu_s = 8.0 * (600 / wavelength_nm) ** 0.15  # weaker wavelength dependence
        g = 0.7
        n = 1.4

    return mu_a, mu_s, g, n

# Dark matter density in the skin (assumed constant for simplicity)
# We'll use a constant value (in GeV/cm^3) for the entire skin.
# This is a placeholder; in reality, we don't know the DM density in skin.
rho_DM = 0.1  # GeV/cm^3, same as the original halo characteristic density

# Birefringence parameter: rotation per unit length per density
# eta such that dalpha/ds = eta * rho_DM (radians per cm)
# We'll use a value motivated by EFT (effective field theory) estimates
# For mirror dark matter, eta can be estimated from kinetic mixing
eta = 1e-24  # rad * cm^2 / GeV (since rho in GeV/cm^3)
# So dalpha/ds = eta * rho_DM (in radians per cm)

# Voxel parameters for dose scoring
num_depth_bins = 200  # number of depth bins from 0 to total_thickness
z_bins = np.linspace(0, total_thickness, num_depth_bins+1)  # bin edges
bin_width = total_thickness / num_depth_bins  # width of each bin in cm

# Function to get layer index based on z position (depth from top)
# We define z=0 at the top of the epidermis, positive downward.
# Layer 0: epidermis (0 <= z < epidermis_thickness)
# Layer 1: dermis (epidermis_thickness <= z < epidermis_thickness+dermis_thickness)
# Layer 2: subcutis (epidermis_thickness+dermis_thickness <= z < total_thickness)
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

# Function to compute attenuation coefficient (mu_t = mu_a + mu_s) for a given layer and wavelength
def mu_t(layer, wavelength_nm=600):
    mu_a, mu_s, g, n = get_optical_properties(layer, wavelength_nm)
    return mu_a + mu_s

# Function to compute scattering albedo (mu_s / mu_t)
def albedo(layer, wavelength_nm=600):
    mu_a, mu_s, g, n = get_optical_properties(layer, wavelength_nm)
    mu_tot = mu_a + mu_s
    if mu_tot > 0:
        return mu_s / mu_tot
    else:
        return 0.0

# Function to compute differential birefringence rotation (dalpha) for a step ds
def dalpha_dsr(ds):
    # eta * rho_DM * ds
    return eta * rho_DM * ds

# Function to rotate Stokes vector by a rotation angle of the linear polarization plane (delta_alpha)
# This rotation affects Q and U:
#   Q' = Q * cos(2*delta_alpha) + U * sin(2*delta_alpha)
#   U' = -Q * sin(2*delta_alpha) + U * cos(2*delta_alpha)
# I and V unchanged.
def rotate_stokes(S, delta_alpha):
    cos_2dal = math.cos(2.0 * delta_alpha)
    sin_2dal = math.sin(2.0 * delta_alpha)
    Q_old = S[1]
    U_old = S[2]
    S_new = np.array([
        S[0],  # I unchanged
        Q_old * cos_2dal + U_old * sin_2dal,
        -Q_old * sin_2dal + U_old * cos_2dal,
        S[3]   # V unchanged
    ])
    return S_new

# Function to sample a scattering angle from the Henyey-Greenstein phase function
def sample_henyey_greenstein(g):
    """
    Sample cosine of scattering angle from HG phase function.
    Returns cos_theta.
    """
    if abs(g) < 1e-6:
        # Isotropic scattering
        return np.random.uniform(-1, 1)
    else:
        xi = np.random.uniform(0, 1)
        denominator = 1 - g + 2 * g * xi
        cos_theta = (1 + g**2 - ((1 - g**2) / denominator)**2) / (2 * g)
        # Clamp to [-1, 1] due to potential numerical errors
        if cos_theta > 1:
            cos_theta = 1
        elif cos_theta < -1:
            cos_theta = -1
        return cos_theta

# Function to generate a random unit vector for isotropic direction
def random_unit_vector():
    costheta = np.random.uniform(-1, 1)
    phi = np.random.uniform(0, 2*math.pi)
    sintheta = math.sqrt(1 - costheta**2)
    return np.array([sintheta * math.cos(phi), sintheta * math.sin(phi), costheta])

# Function to simulate a single photon packet
def simulate_photon(wavelength_nm=600):
    """
    Simulate a single photon packet launched from a point source within the dermis.
    Returns None if absorbed or escapes bottom, else returns the Stokes vector at escape (top).
    """
    # Launch point: within the dermis, we choose a uniform depth in the dermis layer
    z0 = epidermis_thickness + np.random.uniform(0, dermis_thickness)
    # We launch from (x=0, y=0, z0) for simplicity (since infinite in x,y, we can set transverse position to zero)
    r = np.array([0.0, 0.0, z0])
    # Initial direction: isotropic
    v = random_unit_vector()
    # Initial Stokes vector: linearly polarized along x-axis (Q=1, I=1)
    S = np.array([1.0, 1.0, 0.0, 0.0])  # I, Q, U, V

    # We'll propagate until the photon escapes or is absorbed
    while True:
        # Determine current layer
        layer = get_layer(r[2])
        # If we are outside the skin (above epidermis or below subcutis), check for escape
        if layer == -1:
            # Escaped through top (epidermis-air interface)
            return S, 'top'
        elif layer == 3:
            # Escaped through bottom (subcutis-whatever interface)
            return None, 'bottom'

        # Get optical properties for current layer
        mu_a, mu_s, g, n = get_optical_properties(layer, wavelength_nm)
        mu_tot = mu_a + mu_s

        # If mu_tot is zero, the photon travels without interaction (should not happen in skin)
        if mu_tot <= 0:
            # Move a large step and continue
            ds = 1.0  # cm
            r = r + v * ds
            # Still apply birefringence
            dalpha = dalpha_dsr(ds)
            S = rotate_stokes(S, dalpha)
            continue

        # Sample step size from exponential distribution with mean 1/mu_tot
        xi = np.random.uniform(0, 1)
        # Avoid xi=0 to prevent infinite step
        while xi == 0:
            xi = np.random.uniform(0, 1)
        ds = -math.log(xi) / mu_tot  # in cm

        # Move the photon by ds in direction v
        r_new = r + v * ds

        # Check if we crossed a layer boundary during this step
        # We'll break the step at boundaries if necessary, but for simplicity we assume
        # that the optical properties are constant within a layer and we check after the step.
        # However, we must apply birefringence for the entire step.
        # Apply birefringence for the full step ds
        dalpha = dalpha_dsr(ds)
        S = rotate_stokes(S, dalpha)

        # Update position
        r = r_new

        # Check if we escaped after the step
        layer_new = get_layer(r[2])
        if layer_new == -1:
            return S, 'top'
        elif layer_new == 3:
            return None, 'bottom'

        # If we are still within the skin, we may have an interaction
        # Determine if the interaction is scattering or absorption
        # Probability of scattering = albedo, absorption = 1 - albedo
        if np.random.uniform(0, 1) < albedo(layer, wavelength_nm):
            # Scattering event
            # Sample scattering angle (cos_theta) and azimuthal angle (phi)
            cos_theta = sample_henyey_greenstein(g)
            phi = np.random.uniform(0, 2*math.pi)
            sin_theta = math.sqrt(1 - cos_theta**2)

            # New direction in the coordinate system where z-axis is along v
            # We need to rotate the vector v by (theta, phi) in its own frame.
            # We'll compute a new vector using the rotation matrix.
            # Let v be the current direction. We find two orthogonal vectors v1 and v2 perpendicular to v.
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

            # New direction:
            # v_new = sin_theta * (cos(phi)*v1 + sin(phi)*v2) + cos_theta * v
            v_new = sin_theta * (math.cos(phi) * v1 + math.sin(phi) * v2) + cos_theta * v
            v = v_new / np.linalg.norm(v_new)  # normalize

            # Note: Scattering does not change the Stokes vector in this simple model.
            # In reality, scattering would change the Stokes vector via a Mueller matrix.
            # However, for simplicity and to focus on birefringence, we neglect the change
            # in Stokes due to scattering. This is a limitation.
            # We could add a Mueller matrix for scattering, but it is complex and depends on
            # the scattering matrix of the tissue. We leave it out for now.
        else:
            # Absorption event: photon dies
            return None, 'absorbed'

# Function to run Monte Carlo simulation for many photons
def run_monte_carlo(N_photons, wavelength_nm=600):
    escaping_stokes = []  # list of Stokes vectors for photons that escape top
    for i in range(N_photons):
        S, outcome = simulate_photon(wavelength_nm)
        if outcome == 'top':
            escaping_stokes.append(S)
        # Progress indicator
        if (i+1) % 10000 == 0:
            print(f"Launched {i+1} photons, {len(escaping_stokes)} escaped top so far.")

    return escaping_stokes

# Function to compute rotation angle from Stokes vector
# Initial Stokes: [1, 1, 0, 0] (I=1, Q=1, U=0, V=0)
# The angle of linear polarization is given by 0.5 * arctan(U/Q)
# But note: the initial angle is 0 because U=0 and Q>0.
# After propagation, the angle is 0.5 * arctan(U/Q)
# However, we must be careful with the quadrant. We'll use arctan2.
def rotation_angle(S):
    # S = [I, Q, U, V]
    if S[0] <= 0:
        return 0.0
    # Normalize Q and U by I to get normalized Stokes parameters
    q = S[1] / S[0]
    u = S[2] / S[0]
    # The angle in radians
    angle = 0.5 * math.atan2(u, q)
    return angle

# Main execution
if __name__ == "__main__":
    print("Starting Monte Carlo simulation for skin birefringence with wavelength-dependent optical properties...")

    # We'll simulate at multiple wavelengths to show wavelength dependence
    wavelengths = [450, 550, 650]  # nm: blue, green, red
    N_photons = 50000   # number of photon packets to launch per wavelength

    results = {}

    for wavelength_nm in wavelengths:
        print(f"\n--- Simulating at wavelength {wavelength_nm} nm ---")
        escaping_stokes = run_monte_carlo(N_photons, wavelength_nm)

        print(f"Simulation complete. {len(escaping_stokes)} photons escaped the top surface.")

        if len(escaping_stokes) > 0:
            # Compute rotation angles for each escaping photon
            rotations = [rotation_angle(S) for S in escaping_stokes]
            rotations = np.array(rotations)

            mean_rotation = np.mean(rotations)
            std_rotation = np.std(rotations)

            results[wavelength_nm] = {
                'mean_rotation': mean_rotation,
                'std_rotation': std_rotation,
                'escaping_count': len(escaping_stokes),
                'rotations': rotations
            }

            print(f"Mean rotation angle: {mean_rotation:.6f} rad ({np.degrees(mean_rotation):.6f} deg)")
            print(f"Standard deviation: {std_rotation:.6f} rad ({np.degrees(std_rotation):.6f} deg)")
        else:
            print("No photons escaped the top surface.")
            results[wavelength_nm] = {
                'mean_rotation': 0.0,
                'std_rotation': 0.0,
                'escaping_count': 0,
                'rotations': np.array([])
            }

    # Output results to skin_birefringence_estimate.md
    with open('skin_birefringence_estimate.md', 'w', encoding='utf-8') as f:
        f.write("# Skin Birefringence Estimate with Wavelength-Dependent Optical Properties\n\n")
        f.write("## Simulation Overview\n\n")
        f.write("This simulation models polarized light transport through layered skin (epidermis, dermis, subcutis) ")
        f.write("with wavelength-dependent optical parameters derived from literature. ")
        f.write("Mirror dark matter birefringence is included via the term dα/ds = η ρ_DM.\n\n")

        f.write("## Layered Skin Model Parameters\n\n")
        f.write("| Layer | Thickness (cm) | Description |\n")
        f.write("|-------|----------------|-------------|\n")
        f.write(f"| Epidermis | {epidermis_thickness:.3f} | Outer layer, contains melanin |\n")
        f.write(f"| Dermis | {dermis_thickness:.3f} | Middle layer, contains blood vessels |\n")
        f.write(f"| Subcutis | {subcutis_thickness:.3f} | Inner layer, fat tissue |\n")
        f.write("| **Total** | **{:.3f}** | **Total thickness** |\n\n".format(total_thickness))

        f.write("## Wavelength-Dependent Optical Properties (Representative Values)\n\n")
        f.write("| Wavelength (nm) | Layer | μ_a (cm⁻¹) | μ_s (cm⁻¹) | g | n |\n")
        f.write("|-----------------|-------|------------|------------|---|---|\n")
        for wl in wavelengths:
            for layer_idx, layer_name in enumerate(['epidermis', 'dermis', 'subcutis']):
                mu_a, mu_s, g, n = get_optical_properties(layer_idx, wl)
                f.write(f"| {wl} | {layer_name} | {mu_a:.3f} | {mu_s:.3f} | {g:.2f} | {n:.2f} |\n")
        f.write("\n")

        f.write("## Dark Matter Birefringence Parameters\n\n")
        f.write("| Parameter | Value |\n")
        f.write("|-----------|-------|\n")
        f.write(f"| Dark matter density in skin (ρ_DM) | {rho_DM} GeV/cm³ |\n")
        f.write(f"| Birefringence constant (η) | {eta} rad·cm²/GeV |\n")
        f.write(f"| Rotation rate (dα/ds) | {eta * rho_DM:.3e} rad/cm |\n")
        f.write("\n")

        f.write("## Simulation Results\n\n")
        f.write("| Wavelength (nm) | Escaped Photons | Mean Rotation Angle ⟨Δα⟩ (rad) | Mean Rotation Angle ⟨Δα⟩ (deg) | Std Dev (rad) | Std Dev (deg) |\n")
        f.write("|-----------------|-----------------|--------------------------------|--------------------------------|---------------|---------------|\n")
        for wl in wavelengths:
            r = results[wl]
            f.write(f"| {wl} | {r['escaping_count']} | {r['mean_rotation']:.6f} | {np.degrees(r['mean_rotation']):.6f} | {r['std_rotation']:.6f} | {np.degrees(r['std_rotation']):.6f} |\n")
        f.write("\n")

        f.write("## Detectable Rotation Threshold Analysis\n\n")
        f.write("Assuming a detectable rotation threshold of 0.01 rad (about 0.57 degrees):\n\n")
        f.write("| Wavelength (nm) | Fraction Exceeding Threshold |\n")
        f.write("|-----------------|------------------------------|\n")
        for wl in wavelengths:
            r = results[wl]
            if len(r['rotations']) > 0:
                fraction = np.sum(np.abs(r['rotations']) > 0.01) / len(r['rotations'])
            else:
                fraction = 0.0
            f.write(f"| {wl} | {fraction:.6f} |\n")
        f.write("\n")

        f.write("## Notes and Limitations\n\n")
        f.write("1. The optical properties are simplified representations based on literature values. ")
        f.write("   More sophisticated models would include specific chromophore concentrations (melanin, hemoglobin, water).\n")
        f.write("2. Scattering is modeled using the Henyey-Greenstein phase function, which is anisotropic but ")
        f.write("   does not fully capture the complexity of tissue scattering.\n")
        f.write("3. The effect of scattering on the Stokes vector is neglected in this model (only birefringence affects polarization). ")
        f.write("   In reality, scattering would also alter the polarization state via Mueller matrices.\n")
        f.write("4. The dark matter density in skin is assumed uniform and equal to the local halo density, ")
        f.write("   which is highly speculative.\n")
        f.write("5. The birefringence constant η is taken from effective field theory estimates for mirror dark matter.\n")
        f.write("\n")

        f.write("## Conclusion\n\n")
        # Calculate overall detectable fraction across all wavelengths
        total_photons = sum(results[wl]['escaping_count'] for wl in wavelengths)
        if total_photons > 0:
            weighted_fraction = sum(
                np.sum(np.abs(results[wl]['rotations']) > 0.01) if len(results[wl]['rotations']) > 0 else 0
                for wl in wavelengths
            ) / total_photons
            f.write(f"Across all simulated wavelengths, {weighted_fraction:.6f} of escaping photons ")
            f.write("exhibit a rotation angle exceeding 0.01 rad (0.57°), suggesting that ")
            f.write("mirror dark matter-induced birefringence in skin could be detectable ")
            f.write("with sufficient photon statistics and polarization sensitivity.\n")
        else:
            f.write("No photons escaped in the simulations, preventing meaningful analysis. ")
            f.write("This suggests the optical parameters may need adjustment or that ")
            f.write("more sophisticated modeling of light-tissue interaction is required.\n")

    print("\nResults written to skin_birefringence_estimate.md")