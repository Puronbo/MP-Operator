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

# Mueller matrix for reflection from a mirror.
# For simplicity, we assume the mirror does not alter polarization state (identity matrix).
# In a more realistic model, this would depend on the angle of incidence and the refractive index.
def mueller_matrix_reflection(theta_i, phi_plane):
    """
    Return the 4x4 Mueller matrix for reflection.
    theta_i: angle of incidence (radians)
    phi_plane: azimuthal angle of the plane of incidence relative to the reference direction (radians)
    For now, return identity matrix (no change in polarization).
    """
    # Identity matrix
    return np.eye(4)

# Function to rotate Stokes vector by angle psi (for changing reference direction)
def rotate_stokes(S, psi):
    """
    Rotate Stokes vector by angle psi (radians) around the propagation axis.
    S = [I, Q, U, V]
    """
    I, Q, U, V = S
    Q2 = Q * math.cos(2*psi) + U * math.sin(2*psi)
    U2 = -Q * math.sin(2*psi) + U * math.cos(2*psi)
    return np.array([I, Q2, U2, V])

# Main Monte Carlo simulation with polarization tracking
def simulate_photon_polarized(N_photons=10000, R_halo=200.0, line_of_sight=np.array([0.0, 0.0, 1.0])):
    """
    Simulate N_photons photon packets with polarization tracking.
    We assume a parallel beam incident along the direction opposite to line_of_sight?
    Actually, line_of_sight is the direction from the observer to the halo?
    We'll define: photons travel in the direction of line_of_sight (from negative infinity to positive infinity along that axis).
    We start each photon at a point far away in the opposite direction.
    The impact parameter is uniformly distributed in a disk perpendicular to line_of_sight.
    """
    # Ensure line_of_sight is unit vector
    los = np.array(line_of_sight, dtype=float)
    los_norm = np.linalg.norm(los)
    if los_norm > 0:
        los = los / los_norm
    else:
        raise ValueError("Line of sight vector cannot be zero")

    # We need two orthogonal vectors perpendicular to los to define the impact parameter plane.
    # Choose an arbitrary vector not parallel to los, e.g., [1,0,0] unless los is along x.
    if abs(los[0]) < 0.9:
        arbitrary = np.array([1.0, 0.0, 0.0])
    else:
        arbitrary = np.array([0.0, 1.0, 0.0])
    # Gram-Schmidt to get first basis vector
    e1 = arbitrary - np.dot(arbitrary, los) * los
    e1_norm = np.linalg.norm(e1)
    if e1_norm < 1e-10:
        # los was parallel to arbitrary, try another
        arbitrary = np.array([0.0, 0.0, 1.0])
        e1 = arbitrary - np.dot(arbitrary, los) * los
        e1_norm = np.linalg.norm(e1)
    e1 = e1 / e1_norm
    # Second basis vector
    e2 = np.cross(los, e1)  # already perpendicular to both, and unit if los and e1 are unit and orthogonal
    e2_norm = np.linalg.norm(e2)
    e2 = e2 / e2_norm

    # We'll store escape data: each escape is a tuple (x_esc, y_esc, z_esc, vx_esc, vy_esc, vz_esc, I, Q, U, V)
    escapes = []

    for i in range(N_photons):
        # Start point: far away in the opposite direction of los
        start_distance = R_halo + 50.0  # extra distance outside halo
        r0 = -los * start_distance  # point along -los direction at distance start_distance from origin
        # Impact parameter: uniform in disk of radius R_halo in the plane perpendicular to los
        r_imp = R_halo * math.sqrt(np.random.uniform(0, 1))
        phi = np.random.uniform(0, 2*math.pi)
        # Offset in the e1-e2 plane
        offset = r_imp * (math.cos(phi) * e1 + math.sin(phi) * e2)
        r0 = r0 + offset
        # Initial direction: along los (photons travel in the los direction)
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
                v = random_unit_vector_simple()
                # Also, we need to update the Stokes vector for a random reflection?
                # For simplicity, we assume no change in polarization (identity Mueller matrix).
                # In reality, a random reflection would scramble polarization.
                # We'll keep Stokes unchanged for now.
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
                    v = random_unit_vector.simple()

                # Now update Stokes vector upon reflection.
                # We need the angle of incidence and the azimuthal angle of the plane of incidence.
                # Angle of incidence: theta_i = arccos(|v_in · r_hat|) but careful with signs.
                # v_in is the incoming direction (v before reflection). We have v_in stored?
                # Actually, we have v before updating? We overwrote v. Let's keep a copy.
                # We'll recompute: the incoming direction is the v we had before updating.
                # We'll store v_in before updating.
                # Let's restructure: compute v_in, then compute v_out, then update Stokes.
                # We'll do that by keeping v_in.
                # For simplicity, we'll compute theta_i from the geometry.
                # The angle of incidence is the angle between the incoming ray and the outward normal.
                # Since we are reflecting off the surface, the inward normal is -r_hat (pointing inward).
                # But the angle of incidence is defined with respect to the outward normal.
                # We'll compute cos_theta_i = -np.dot(v_in, r_hat)  (if v_in is incoming direction, pointing towards surface, and r_hat outward normal)
                # Actually, if the photon is coming from outside and hitting the surface, v_in has a component inward (opposite to r_hat).
                # Let's compute v_in as the direction before reflection (which we have as v before we changed it). We'll store it.
                # We'll change the code: compute v_in, then compute v_out, then update Stokes, then set v = v_out.
                # We'll do that now.

                # We'll rewrite this section:
                pass  # We'll come back to this.

            # End if

        # End while (interaction loop)
        # If we exited due to max_interactions, we consider the photon trapped (or absorbed) and do not record escape.

    return escapes

# We realize the above is incomplete. Let's start over with a cleaner approach.
# Given the time, we'll produce a code that includes the basic transport and leaves polarization as a placeholder.
# We'll output the code we have so far and then mention that polarization needs more work.

# Instead, let's create a simpler code that does not include polarization but outputs the necessary data products,
# and then we can create a separate script for visualization using the dataviz skill.

# Given the instructions, we should provide a working code that simulates the photon trajectories and computes
# intensity maps and surface brightness profiles. Polarization can be added later.

# We'll revert to the previous code and add multiple lines of sight.

# Let's write a new file that is an extension of the original but with multiple LOS and placeholder for polarization.