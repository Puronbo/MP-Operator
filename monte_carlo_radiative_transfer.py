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
def random_unit_vector():
    # Marsaglia method
    while True:
        x = np.random.uniform(-1, 1)
        y = np.random.uniform(-1, 1)
        s = x*x + y*y
        if 0 < s <= 1:
            break
    z = 1 - 2*s
    r = 2 * math.sqrt(s)
    return np.array([x*z/r, y*z/r, (z*z - s)/r])  # Actually, let's use a simpler method

# Simpler method: sample cos(theta) uniformly in [-1,1] and phi uniformly in [0, 2π]
def random_unit_vector_simple():
    costheta = np.random.uniform(-1, 1)
    phi = np.random.uniform(0, 2*math.pi)
    sintheta = math.sqrt(1 - costheta**2)
    return np.array([sintheta * math.cos(phi), sintheta * math.sin(phi), costheta])

# Main Monte Carlo simulation
def simulate_photon(N_photons=10000, R_halo=200.0):
    """
    Simulate N_photons photon packets.
    We assume a parallel beam incident along the +z direction from z = -infinity.
    We start each photon at a point (x, y, z_start) where z_start = -R_halo - 10.0 (outside the halo)
    and (x,y) uniformly distributed in a disk of radius R_halo (to cover the halo).
    The initial direction is +z (0,0,1).
    We track each photon until it escapes the halo (r > R_halo) or until we have too many interactions (set a max).
    We record the escape point and direction for binning.
    """
    # We'll store escape data: each escape is a tuple (x_esc, y_esc, z_esc, vx_esc, vy_esc, vz_esc)
    escapes = []

    for i in range(N_photons):
        # Start point: outside the halo along the z-axis
        z_start = -R_halo - 10.0
        # Impact parameter: uniform in disk of radius R_halo
        r_imp = R_halo * math.sqrt(np.random.uniform(0, 1))
        phi = np.random.uniform(0, 2*math.pi)
        x_start = r_imp * math.cos(phi)
        y_start = r_imp * math.sin(phi)
        r0 = np.array([x_start, y_start, z_start])
        v0 = np.array([0.0, 0.0, 1.0])  # incident along +z

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
                escapes.append((r[0], r[1], r[2], v[0], v[1], v[2]))
                break

            # Otherwise, we had an interaction at point r
            interactions += 1

            # For a mirror-like interaction, we reflect specularly with respect to the local radial direction.
            # The radial unit vector at point r:
            r_mag = np.linalg.norm(r)
            if r_mag < 1e-10:
                # Avoid division by zero at center; random reflection
                v = random_unit_vector_simple()
            else:
                r_hat = r / r_mag
                # Specular reflection: v_ref = v - 2*(v·r_hat)*r_hat
                v_dot_rhat = np.dot(v, r_hat)
                v = v - 2 * v_dot_rhat * r_hat
                # Renormalize (should already be unit, but just in case)
                v_norm = np.linalg.norm(v)
                if v_norm > 0:
                    v = v / v_norm
                else:
                    v = random_unit_vector_simple()

        # End while (interaction loop)
        # If we exited due to max_interactions, we consider the photon trapped (or absorbed) and do not record escape.

    return escapes

# Function to bin escapes into a surface brightness profile (radial binning)
def surface_brightness_profile(escapes, R_halo, nbins=50):
    """
    Bin escaping photons by their projected radius (impact parameter) in the xy-plane.
    We assume observation along the z-axis, so the impact parameter is sqrt(x^2+y^2).
    Returns: (bin_centers, counts_per_bin, surface_brightness)
    """
    if not escapes:
        return np.array([]), np.array([]), np.array([])

    # Extract impact parameters
    rhos = np.array([math.sqrt(e[0]**2 + e[1]**2) for e in escapes])

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

# Function to create an intensity map (2D histogram in x-y)
def intensity_map(escapes, R_halo, nbins=100):
    """
    Create a 2D histogram of escape points in the xy-plane (impact parameter plane).
    Returns: (x_edges, y_edges, counts_2d)
    """
    if not escapes:
        return np.array([]), np.array([]), np.array([])

    xs = np.array([e[0] for e in escapes])
    ys = np.array([e[1] for e in escapes])

    # Bin from -R_halo to R_halo in both x and y
    bins = np.linspace(-R_halo, R_halo, nbins+1)
    counts_2d, x_edges, y_edges = np.histogram2d(xs, ys, bins=bins)

    return x_edges, y_edges, counts_2d

# Example usage and simple output
if __name__ == "__main__":
    print("Starting Monte Carlo radiative transfer simulation...")
    R_halo = 200.0  # kpc, halo radius
    escapes = simulate_photon(N_photons=5000, R_halo=R_halo)
    print(f"Number of escaping photons: {len(escapes)}")

    if escapes:
        # Surface brightness profile
        radii, counts, sb = surface_brightness_profile(escapes, R_halo, nbins=20)
        print("\nSurface brightness profile (radius [kpc], counts, surface brightness [counts/kpc^2]):")
        for r, c, s in zip(radii, counts, sb):
            print(f"{r:.2f} {c} {s:.2f}")

        # Intensity map (we'll just print the shape)
        x_edges, y_edges, counts_2d = intensity_map(escapes, R_halo, nbins=10)
        print(f"\nIntensity map shape: {counts_2d.shape}")
        print("Total counts in map:", np.sum(counts_2d))
    else:
        print("No photons escaped. Try increasing the number of photons or decreasing the cross-section.")

    print("\nSimulation complete.")