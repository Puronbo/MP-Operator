import numpy as np
import matplotlib.pyplot as plt
# Import simulation functions from our final code
from monte_carlo_radiative_transfer_final import (
    simulate_photon_for_los,
    surface_brightness_profile_general,
    intensity_map_general,
    average_polarization
)

# Constants
R_halo = 200.0  # kpc
N_photons = 5000

# Define a few lines of sight
los_list = [
    np.array([0.0, 0.0, 1.0]),  # along z
    np.array([0.0, 1.0, 0.0]),  # along y
    np.array([1.0, 0.0, 0.0]),  # along x
]

# Normalize
los_list = [los / np.linalg.norm(los) for los in los_list]

# Store results for plotting
sb_profiles = []  # each element: (los_label, radii, sb)
intensity_maps = []  # each element: (los_label, extent, counts_2d)

for idx, los in enumerate(los_list):
    los_label = f'LOS{idx}'
    print(f"Simulating for {los_label}: {los}")
    escapes = simulate_photon_for_los(N_photons, R_halo, los)
    print(f"  Escaping photons: {len(escapes)}")
    if escapes:
        # Surface brightness profile
        radii, counts, sb = surface_brightness_profile_general(escapes, R_halo, los, nbins=30)
        sb_profiles.append((los_label, radii, sb))
        # Intensity map
        x_edges, y_edges, counts_2d = intensity_map_general(escapes, R_halo, los, nbins=50)
        extent = [-R_halo, R_halo, -R_halo, R_halo]  # [xmin, xmax, ymin, ymax]
        intensity_maps.append((los_label, extent, counts_2d))
        # Average polarization
        I_avg, Q_avg, U_avg, V_avg = average_polarization(escapes)
        print(f"  Avg Stokes: I={I_avg:.3f}, Q={Q_avg:.3f}, U={U_avg:.3f}, V={V_avg:.3f}")
    else:
        print("  No photons escaped.")

# Now create visualizations
# We'll follow the dataviz skill guidelines: use a neutral color palette, etc.
# For simplicity, we'll use matplotlib's default but we can adjust.

# 1. Surface brightness profiles for each LOS
plt.figure(figsize=(10, 6))
for los_label, radii, sb in sb_profiles:
    plt.plot(radii, sb, marker='o', linestyle='-', label=los_label)
plt.xlabel('Impact parameter $\\rho$ (kpc)')
plt.ylabel('Surface Brightness (arb. units)')
plt.title('Surface Brightness Profiles for Different Lines of Sight')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('surface_brightness_profiles.png', dpi=150)
plt.close()

# 2. Intensity maps for each LOS (show as images)
n_los = len(intensity_maps)
if n_los > 0:
    fig, axes = plt.subplots(1, n_los, figsize=(5*n_los, 5))
    if n_los == 1:
        axes = [axes]
    for ax, (los_label, extent, counts_2d) in zip(axes, intensity_maps):
        im = ax.imshow(counts_2d.T, origin='lower', extent=extent, aspect='auto')
        ax.set_xlabel('$x_1$ (kpc)')
        ax.set_ylabel('$x_2$ (kpc)')
        ax.set_title(f'Intensity Map: {los_label}')
        plt.colorbar(im, ax=ax, label='Counts')
    plt.tight_layout()
    plt.savefig('intensity_maps.png', dpi=150)
    plt.close()

print("Visualizations saved as surface_brightness_profiles.png and intensity_maps.png")