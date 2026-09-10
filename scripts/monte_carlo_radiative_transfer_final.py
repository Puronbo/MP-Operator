import numpy as np
import math

# Constants and parameters
# Halo parameters (NFW profile)
rho0 = 0.1  # GeV/cm^3, characteristic density (convert to appropriate units)
rs = 20.0   # kpc, scale radius
# Convert to consistent units: we'll use kpc for length, and set c=1 for simplicity (photons travel at speed of light)
# We need to convert density to number density: n(r) = rho(r) / m_dm
# Assume dark matter particle mass m_dm = 100 GeV/c^2
m_dm = 100.0  # GeV/c^2
# Cross-section for interaction (mirror-like reflection): we assume a constant cross-section
sigma = 1e-24  # cm^2, example value (very small, as expected for dark matter interactions)
# Convert sigma to kpc^2: 1 kpc = 3.086e21 cm -> 1 kpc^2 = (3.086e21)^2 cm^2
cm_per_kpc = 3.086e21
sigma_kpc2 = sigma / (cm_per_kpc ** 2)

# Function for NFW density profile: rho(r) = rho0 / [(r/rs) * (1 + r/rs)^2]
def rho_nfw(r):
    if r < 1e-10:  # avoid division by zero
        return rho0
    x = r / rs
    return rho0 / (x * (1 + x)**2)

# Number density: n(r) = rho(r) / m_dm
def n_dm(r):
    return rho_nfw(r) / m_dm

# Optical depth differential: dτ = n(r) * sigma * dr
def dtau_dr(r):
    return n_dm(r) * sigma_kpc2

# Function to compute optical depth along a straight line from point r0 in direction v_hat (unit vector)
# until exiting the halo (defined by a maximum radius R_max) or until reaching a target tau.
# We'll use numerical integration (simple Euler) for demonstration.
def compute_optical_depth(r0, v_hat, tau_target=None, R_max=1000.0):
    """
    Compute the optical depth along the ray starting at r0 in direction v_hat.
    If tau_target is provided, stop when accumulated tau >= tau_target.
    Otherwise, integrate until leaving the halo (r > R_max).
    Returns: (tau_accumulated, distance_traveled, point_at_stop)
    """
    r = np.array(r0, dtype=float)
    v = np.array(v_hat, dtype=float)
    # Ensure v is unit vector
    v_norm = np.linalg.norm(v)
    if v_norm > 0:
        v = v / v_norm
    else:
        raise ValueError("Direction vector cannot be zero")

    tau_acc = 0.0
    s = 0.0  # distance traveled
    ds = 0.01  # step size in kpc (adjust for accuracy and speed)

    while True:
        r_mag = np.linalg.norm(r)
        if r_mag > R_max:
            # Left the halo
            break
        # Local dτ/ds
        dtau_ds = dtau_dr(r_mag)
        tau_acc += dtau_ds * ds
        s += ds
        r = r + v * ds

        if tau_target is not None and tau_acc >= tau_target:
            break

    return tau_acc, s, r

# Function to generate a random unit vector for isotropic direction
def random_unit_vector_simple():
    costheta = np.random.uniform(-1, 1)
    phi = np.random.uniform(0, 2*math.pi)
    sintheta = math.sqrt(1 - costheta**2)
    return np.array([sintheta * math.cos(phi), sintheta * math.sin(phi), costheta])

# Function to simulate photons for a given line of sight
def simulate_photon_for_los(N_photons, R_halo, los):
    """
    Simulate N_photons photon packets for a given line of sight.
    los: unit vector indicating the direction of photon travel (from negative to positive infinity along this axis).
    We start each photon far away in the -los direction.
    Impact parameter uniformly distributed in a disk of radius R_halo in the plane perpendicular to los.
    Returns list of escaping photons, each as a tuple:
    (x, y, z, vx, vy, vz, I, Q, U, V)
    where Stokes vector is for unpolarized light and unchanged (placeholder).
    """
    # Ensure los is unit vector
    los = np.array(los, dtype=float)
    los_norm = np.linalg.norm(los)
    if los_norm > 0:
        los = los / los_norm
    else:
        raise ValueError("Line of sight vector cannot be zero")

    # Choose two orthogonal vectors perpendicular to los to define the impact parameter plane.
    # Select an arbitrary vector not parallel to los
    if abs(los[0]) < 0.9:
        arbitrary = np.array([1.0, 0.0, 0.0])
    else:
        arbitrary = np.array([0.0, 1.0, 0.0])
    # Gram-Schmidt to get first basis vector e1
    e1 = arbitrary - np.dot(arbitrary, los) * los
    e1_norm = np.linalg.norm(e1)
    if e1_norm < 1e-10:
        # los was parallel to arbitrary, try another
        arbitrary = np.array([0.0, 0.0, 1.0])
        e1 = arbitrary - np.dot(arbitrary, los) * los
        e1_norm = np.linalg.norm(e1)
    e1 = e1 / e1_norm
    # Second basis vector e2 = los x e1 (orthogonal to both)
    e2 = np.cross(los, e1)
    e2_norm = np.linalg.norm(e2)
    e2 = e2 / e2_norm  # should already be unit if los and e1 are unit and orthogonal

    escapes = []
    for i in range(N_photons):
        # Start point: far away in the -los direction
        start_distance = R_halo + 50.0  # extra distance outside halo
        r0 = -los * start_distance
        # Impact parameter: uniform in disk of radius R_halo
        r_imp = R_halo * math.sqrt(np.random.uniform(0, 1))
        phi = np.random.uniform(0, 2*math.pi)
        offset = r_imp * (math.cos(phi) * e1 + math.sin(phi) * e2)
        r0 = r0 + offset
        # Initial direction: along los
        v0 = los.copy()

        # Initial Stokes vector: unpolarized light
        S = np.array([1.0, 0.0, 0.0, 0.0])  # I, Q, U, V

        r = r0.copy()
        v = v0.copy()
        interactions = 0
        max_interactions = 100  # prevent infinite loops

        while interactions < max_interactions:
            # Draw a random optical depth to next interaction: tau = -ln(ξ)
            xi = np.random.uniform(0, 1)
            tau_target = -math.log(xi) if xi > 0 else float('inf')

            # Compute how far we travel before accumulating tau_target or leaving halo
            tau_acc, ds, r_stop = compute_optical_depth(r, v, tau_target=tau_target, R_max=R_halo)

            # Move to the stop point
            r = r_stop

            # Check if we left the halo during this step
            if np.linalg.norm(r) > R_halo:
                # Escaped without interacting in this step
                escapes.append((r[0], r[1], r[2], v[0], v[1], v[2], S[0], S[1], S[2], S[3]))
                break

            # Otherwise, we had an interaction at point r
            interactions += 1

            # For a mirror-like interaction, we reflect specularly with respect to the local radial direction.
            r_mag = np.linalg.norm(r)
            if r_mag < 1e-10:
                # Avoid division by zero at center; random reflection
                v = random_unit_vector.simple()
                # Stokes vector unchanged (placeholder)
            else:
                r_hat = r / r_mag
                # Specular reflection: v_ref = v - 2*(v·r_hat)*r_hat
                v_dot_rhat = np.dot(v, r_hat)
                v = v - 2 * v_dot_rhat * r_hat
                # Renormalize
                v_norm = np.linalg.norm(v)
                if v_norm > 0:
                    v = v / v_norm
                else:
                    v = random_unit_vector.simple()
                # Stokes vector unchanged (placeholder for polarization evolution)

        # End while (interaction loop)
        # If we exited due to max_interactions, we consider the photon trapped (or absorbed) and do not record escape.

    return escapes

# Function to bin escapes into a surface brightness profile (radial binning) for a given LOS
def surface_brightness_profile(escapes, R_halo, nbins=50):
    """
    Bin escaping photons by their projected radius (impact parameter) in the plane perpendicular to the LOS.
    Assumes that the escapes are already in the coordinate system where the LOS is the z-axis?
    Actually, we need to compute the impact parameter relative to the LOS direction.
    We'll compute the vector from the halo center to the escape point, then subtract the component along LOS.
    The impact parameter vector is the perpendicular component.
    Returns: (bin_centers, counts_per_bin, surface_brightness)
    """
    if not escapes:
        return np.array([]), np.array([]), np.array([])

    # We'll assume the halo center is at origin (0,0,0)
    # For each escape point, compute the impact parameter relative to the LOS used in simulation.
    # However, the escapes list does not store the LOS used. We need to modify the function to accept LOS.
    # Let's change the function signature to include los.
    # We'll do that in a moment. For now, we'll assume the LOS is along the z-axis (as in the original code).
    # To keep things simple, we'll create a separate function for each LOS that assumes we have aligned the LOS with z-axis via rotation.
    # Alternatively, we can compute the impact parameter by subtracting the projection onto los.
    # We'll need the los vector. We'll add it as a parameter.
    pass

# Let's rewrite the surface brightness profile function to take los.
def surface_brightness_profile_general(escapes, R_halo, los, nbins=50):
    """
    Bin escaping photons by their impact parameter relative to the given line of sight.
    los: unit vector indicating the line of sight direction.
    Returns: (bin_centers, counts_per_bin, surface_brightness)
    """
    if not escapes:
        return np.array([]), np.array([]), np.array([])

    los = np.array(los, dtype=float)
    los_norm = np.linalg.norm(los)
    if los_norm > 0:
        los = los / los_norm
    else:
        raise ValueError("Line of sight vector cannot be zero")

    # Compute impact parameter for each escape point
    rhos = []
    for esc in escapes:
        r_vec = np.array(esc[0:3])  # x, y, z
        # Component along los
        parallel = np.dot(r_vec, los) * los
        perp_vec = r_vec - parallel
        rho = np.linalg.norm(perp_vec)
        rhos.append(rho)
    rhos = np.array(rhos)

    # Create bins from 0 to R_halo
    bins = np.linspace(0, R_halo, nbins+1)
    bin_centers = (bins[:-1] + bins[1:]) / 2
    counts, _ = np.histogram(rhos, bins=bins)

    # Surface brightness: counts per unit area per bin
    bin_areas = np.pi * (bins[1:]**2 - bins[:-1]**2)
    # Avoid division by zero
    with np.errstate(divide='ignore', invalid='ignore'):
        sb = counts / bin_areas
        sb[~np.isfinite(sb)] = 0

    return bin_centers, counts, sb

# Function to create an intensity map (2D histogram in the plane perpendicular to LOS)
def intensity_map_general(escapes, R_halo, los, nbins=100):
    """
    Create a 2D histogram of escape points in the plane perpendicular to the line of sight.
    We need to project each escape point onto two orthogonal axes in the plane perpendicular to los.
    Returns: (coord1_edges, coord2_edges, counts_2d)
    where coord1 and coord2 are coordinates along two orthonormal vectors e1, e2 spanning the plane.
    """
    if not escapes:
        return np.array([]), np.array([]), np.array([])

    los = np.array(los, dtype=float)
    los_norm = np.linalg.norm(los)
    if los_norm > 0:
        los = los / los_norm
    else:
        raise ValueError("Line of sight vector cannot be zero")

    # Choose two orthogonal vectors perpendicular to los to define the plane coordinates.
    # Same method as in simulation.
    if abs(los[0]) < 0.9:
        arbitrary = np.array([1.0, 0.0, 0.0])
    else:
        arbitrary = np.array([0.0, 1.0, 0.0])
    e1 = arbitrary - np.dot(arbitrary, los) * los
    e1_norm = np.linalg.norm(e1)
    if e1_norm < 1e-10:
        arbitrary = np.array([0.0, 0.0, 1.0])
        e1 = arbitrary - np.dot(arbitrary, los) * los
        e1_norm = np.linalg.norm(e1)
    e1 = e1 / e1_norm
    e2 = np.cross(los, e1)
    e2_norm = np.linalg.norm(e2)
    e2 = e2 / e2_norm

    # Project each escape point onto e1 and e2
    coords1 = []
    coords2 = []
    for esc in escapes:
        r_vec = np.array(esc[0:3])
        # Subtract the component along los to get the projection onto the plane
        parallel = np.dot(r_vec, los) * los
        perp_vec = r_vec - parallel
        c1 = np.dot(perp_vec, e1)
        c2 = np.dot(perp_vec, e2)
        coords1.append(c1)
        coords2.append(c2)
    coords1 = np.array(coords1)
    coords2 = np.array(coords2)

    # Bin from -R_halo to R_halo in both coordinates
    bins = np.linspace(-R_halo, R_halo, nbins+1)
    counts_2d, x_edges, y_edges = np.histogram2d(coords1, coords2, bins=bins)

    return x_edges, y_edges, counts_2d

# Function to compute average polarization from escapes (placeholder)
def average_polarization(escapes):
    """
    Compute the average Stokes vector from the escaping photons.
    Returns: (I_avg, Q_avg, U_avg, V_avg)
    """
    if not escapes:
        return 0.0, 0.0, 0.0, 0.0
    Stokes = np.array([esc[6:] for esc in escapes])  # columns I, Q, U, V
    avg = np.mean(Stokes, axis=0)
    return avg[0], avg[1], avg[2], avg[3]

# Example usage and simple output
if __name__ == "__main__":
    print("Starting Monte Carlo radiative transfer simulation with multiple lines of sight...")
    R_halo = 200.0  # kpc, halo radius
    N_photons_per_los = 5000

    # Define a few lines of sight: e.g., along z-axis, and some tilted directions
    los_list = [
        np.array([0.0, 0.0, 1.0]),  # along z
        np.array([0.0, 1.0, 0.0]),  # along y
        np.array([1.0, 0.0, 0.0]),  # along x
        np.array([0.5, 0.5, 0.70710678])  # tilted
    ]
    # Normalize each los
    los_list = [los / np.linalg.norm(los) for los in los_list]

    all_results = {}
    for idx, los in enumerate(los_list):
        print(f"\nSimulating for LOS {idx}: {los}")
        escapes = simulate_photon_for_los(N_photons_per_los, R_halo, los)
        print(f"  Number of escaping photons: {len(escapes)}")
        if escapes:
            # Surface brightness profile
            radii, counts, sb = surface_brightness_profile_general(escapes, R_halo, los, nbins=20)
            print(f"  Surface brightness profile (first few bins):")
            for r, c, s in zip(radii[:5], counts[:5], sb[:5]):
                print(f"    rho={r:.2f} kpc, counts={c}, SB={s:.2f}")
            # Intensity map shape
            x_edges, y_edges, counts_2d = intensity_map_general(escapes, R_halo, los, nbins=10)
            print(f"  Intensity map shape: {counts_2d.shape}")
            print(f"  Total counts in map: {np.sum(counts_2d)}")
            # Average polarization
            I_avg, Q_avg, U_avg, V_avg = average_polarization(escapes)
            print(f"  Average Stokes vector: I={I_avg:.3f}, Q={Q_avg:.3f}, U={U_avg:.3f}, V={V_avg:.3f}")
            # Store results for possible later use
            all_results[tuple(los)] = (escapes, radii, counts, sb, x_edges, y_edges, counts_2d)
        else:
            print("  No photons escaped.")

    print("\nSimulation complete.")