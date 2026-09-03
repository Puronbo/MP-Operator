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

# Optical properties as functions of wavelength (we'll use a single wavelength for simplicity, e.g., 600 nm)
# Values are representative averages for skin in the visible range.
# Units: per cm (cm^-1)

# We'll define a function to get optical properties for a given layer and wavelength
# For simplicity, we'll use fixed values for a wavelength of 600 nm.
# Source: Various literature (e.g., Jacques, "Optical properties of biological tissues: a review")

def get_optical_properties(layer, wavelength_nm=600):
    """
    Returns (mu_a, mu_s, g, n) for the given layer at the given wavelength.
    layer: 0 for epidermis, 1 for dermis, 2 for subcutis
    wavelength_nm: wavelength in nanometers
    """
    # We'll ignore wavelength dependence for now and use fixed values at 600 nm
    if layer == 0:  # epidermis
        mu_a = 0.5   # absorption coefficient
        mu_s = 10.0  # scattering coefficient
        g = 0.75     # anisotropy
        n = 1.4      # refractive index
    elif layer == 1: # dermis
        mu_a = 0.3
        mu_s = 15.0
        g = 0.8
        n = 1.4
    else:            # subcutis
        mu_a = 0.1
        mu_s = 8.0
        g = 0.7
        n = 1.4
    return mu_a, mu_s, g, n

# Dark matter density in the skin (assumed constant for simplicity)
# We'll use a constant value (in GeV/cm^3) for the entire skin.
# This is a placeholder; in reality, we don't know the DM density in skin.
rho_DM = 0.1  # GeV/cm^3, same as the original halo characteristic density

# Birefringence parameter: rotation per unit length per density
# eta such that dalpha/ds = eta * rho_DM (radians per cm)
# We'll use a small value to get detectable rotations for demonstration
eta = 1e-24  # rad * cm^2 / GeV (since rho in GeV/cm^3)
# So dalpha/ds = eta * rho_DM (in radians per cm)

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
    print("Starting Monte Carlo simulation for skin birefringence...")
    wavelength_nm = 600  # nm, red light
    N_photons = 50000   # number of photon packets to launch

    escaping_stokes = run_monte_carlo(N_photons, wavelength_nm)

    print(f"\nSimulation complete. {len(escaping_stokes)} photons escaped the top surface.")

    if len(escaping_stokes) > 0:
        # Compute rotation angles for each escaping photon
        rotations = [rotation_angle(S) for S in escaping_stokes]
        rotations = np.array(rotations)

        mean_rotation = np.mean(rotations)
        std_rotation = np.std(rotations)

        print(f"Mean rotation angle: {mean_rotation:.6f} rad ({np.degrees(mean_rotation):.6f} deg)")
        print(f"Standard deviation: {std_rotation:.6f} rad ({np.degrees(std_rotation):.6f} deg)")

        # Also compute the distribution (we can output to a file for plotting)
        # We'll write the results to a markdown file as requested.
        with open('skin_birefringence_estimate.md', 'w') as f:
            f.write("# Skin Birefringence Estimate\n\n")
            f.write(f"**Wavelength**: {wavelength_nm} nm\n")
            f.write(f"**Number of photon packets launched**: {N_photons}\n")
            f.write(f"**Number of photons escaping top surface**: {len(escaping_stokes)}\n")
            f.write(f"**Mean rotation angle ⟨Δα⟩**: {mean_rotation:.6f} rad ({np.degrees(mean_rotation):.6f} deg)\n")
            f.write(f"**Standard deviation of rotation angle**: {std_rotation:.6f} rad ({np.degrees(std_rotation):.6f} deg)\n\n")
            f.write("## Detectable Rotation Threshold\n\n")
            f.write("Assuming a detectable rotation threshold of 0.01 rad (about 0.57 degrees), ")
            f.write(f"the fraction of photons exceeding this threshold is: ")
            f.write(f"{np.sum(np.abs(rotations) > 0.01) / len(rotations):.6f}\n")
            f.write("\n## Layered Skin Model Parameters\n\n")
            f.write("| Layer | Thickness (cm) | μ_a (cm⁻¹) | μ_s (cm⁻¹) | g | n |\n")
            f.write("|-------|----------------|------------|------------|---|---|\n")
            f.write(f"| Epidermis | {epidermis_thickness:.3f} | {get_optical_properties(0)[0]:.3f} | {get_optical_properties(0)[1]:.3f} | {get_optical_properties(0)[2]:.2f} | {get_optical_properties(0)[3]:.2f} |\n")
            f.write(f"| Dermis | {dermis_thickness:.3f} | {get_optical_properties(1)[0]:.3f} | {get_optical_properties(1)[1]:.3f} | {get_optical_properties(1)[2]:.2f} | {get_optical_properties(1)[3]:.2f} |\n")
            f.write(f"| Subcutis | {subcutis_thickness:.3f} | {get_optical_properties(2)[0]:.3f} | {get_optical_properties(2)[1]:.3f} | {get_optical_properties(2)[2]:.2f} | {get_optical_properties(2)[3]:.2f} |\n")
            f.write("\n## Dark Matter Birefringence Parameters\n\n")
            f.write(f"| Parameter | Value |\n")
            f.write(f"|-----------|-------|\n")
            f.write(f"| Dark matter density in skin (ρ_DM) | {rho_DM} GeV/cm³ |\n")
            f.write(f"| Birefringence constant (η) | {eta} rad·cm²/GeV |\n")
            f.write(f"| Rotation rate (dα/ds) | {eta * rho_DM:.3e} rad/cm |\n")

        print("Results written to skin_birefringence_estimate.md")
    else:
        print("No photons escaped the top surface. Cannot compute rotation angle.")