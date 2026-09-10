import mpmath as mp
import numpy as np
import matplotlib.pyplot as plt

mp.mp.dps = 30

def xi(s):
    return 0.5 * s * (s-1) * mp.pi**(-s/2) * mp.gamma(s/2) * mp.zeta(s)

# Create a grid in the critical strip
sigma_min, sigma_max = 0, 1
t_min, t_max = 0, 50
resolution = 400  # points in each direction

sigma_vals = np.linspace(sigma_min, sigma_max, resolution)
t_vals = np.linspace(t_min, t_max, resolution)
Sigma, T = np.meshgrid(sigma_vals, t_vals)

# Compute xi(s) on the grid
X = np.zeros_like(Sigma, dtype=complex)
Y = np.zeros_like(Sigma, dtype=complex)
for i in range(resolution):
    for j in range(resolution):
        s = mp.mpc(Sigma[i,j], T[i,j])
        # Avoid poles
        if abs(s) < 1e-12 or abs(s-1) < 1e-12:
            X[i,j] = np.nan
            Y[i,j] = np.nan
        else:
            val = xi(s)
            X[i,j] = val.real
            Y[i,j] = val.imag

# Plot 1: |xi(s)| and arg(xi(s)) to see symmetry
fig = plt.figure(figsize=(16, 12))

# Panel 1: |xi(s)| in the critical strip
ax1 = plt.subplot(2, 3, 1)
# Use log scale for magnitude
magnitude = np.sqrt(X**2 + Y**2)
# Mask poles
magnitude_masked = np.ma.masked_invalid(magnitude)
im1 = ax1.imshow(magnitude_masked.T, extent=[sigma_min, sigma_max, t_min, t_max],
                 origin='lower', aspect='auto', cmap='viridis')
ax1.set_xlabel('$\\sigma = \\Re(s)$')
ax1.set_ylabel('$t = \\Im(s)$')
ax1.set_title('$|\\xi(s)|$ in the critical strip')
plt.colorbar(im1, ax=ax1)

# Panel 2: Phase of xi(s) (argument)
ax2 = plt.subplot(2, 3, 2)
phase = np.angle(X + 1j*Y)
# Mask poles
phase_masked = np.ma.masked_invalid(phase)
im2 = ax2.imshow(phase_masked.T, extent=[sigma_min, sigma_max, t_min, t_max],
                 origin='lower', aspect='auto', cmap='hsv')
ax2.set_xlabel('$\\sigma = \\Re(s)$')
ax2.set_ylabel('$t = \\Im(s)$')
ax2.set_title('$\arg\\xi(s)$ (phase)')
plt.colorbar(im2, ax=ax2)

# Panel 3: Real part of xi(s)
ax3 = plt.subplot(2, 3, 3)
real_masked = np.ma.masked_invalid(X)
im3 = ax3.imshow(real_masked.T, extent=[sigma_min, sigma_max, t_min, t_max],
                 origin='lower', aspect='auto', cmap='RdBu')
ax3.set_xlabel('$\\sigma = \\Re(s)$')
ax3.set_ylabel('$t = \\Im(s)$')
ax3.set_title('$\\Re\\xi(s)$')
plt.colorbar(im3, ax=ax3)

# Panel 4: Imaginary part of xi(s) - this should vanish on critical line
ax4 = plt.subplot(2, 3, 4)
imag_masked = np.ma.masked_invalid(Y)
im4 = ax4.imshow(imag_masked.T, extent=[sigma_min, sigma_max, t_min, t_max],
                 origin='lower', aspect='auto', cmap='RdBu')
ax4.set_xlabel('$\\sigma = \\Re(s)$')
ax4.set_ylabel('$t = \\Im(s)$')
ax4.set_title('$\\Im\\xi(s)$ (should be zero on $\\sigma=1/2$)')
plt.colorbar(im4, ax=ax4)
# Add a line at sigma=0.5
ax4.axvline(x=0.5, color='yellow', linestyle='--', linewidth=2)

# Panel 5: xi(s) on the critical line (sigma=0.5)
ax5 = plt.subplot(2, 3, 5)
t_critical = np.linspace(t_min, t_max, 1000)
xi_critical = []
for t in t_critical:
    s = mp.mpc(0.5, t)
    val = xi(s)
    xi_critical.append(val)
xi_critical = np.array(xi_critical)
ax5.plot(t_critical, xi_critical.real, 'b-', label='Re($\\xi(1/2+it)$)')
ax5.plot(t_critical, xi_critical.imag, 'r--', label='Im($\\xi(1/2+it)$)')
ax5.axhline(y=0, color='k', linewidth=0.5)
ax5.set_xlabel('$t$')
ax5.set_ylabel('$\\xi(1/2+it)$')
ax5.set_title('$\\xi(s)$ on the critical line $\\sigma=1/2$')
ax5.legend()
ax5.grid(True, alpha=0.3)

# Panel 6: Symmetry demonstration: xi(s) vs xi(1-s)
ax6 = plt.subplot(2, 3, 6)
# Pick a few points off the critical line
test_sigmas = [0.3, 0.4, 0.6, 0.7]
test_t = [10, 20, 30]
symmetry_errors = []
for sigma in test_sigmas:
    for t in test_t:
        s = mp.mpc(sigma, t)
        s_reflected = mp.mpc(1-sigma, t)  # 1-s
        val_s = xi(s)
        val_reflected = xi(s_reflected)
        # xi(s) should equal xi(1-s)
        error = abs(val_s - val_reflected)
        symmetry_errors.append(error)
        # Plot the pair
        ax6.plot([sigma, 1-sigma], [t, t], 'k-', alpha=0.3)
        ax6.plot(sigma, t, 'bo', markersize=4)
        ax6.plot(1-sigma, t, 'ro', markersize=4)
ax6.set_xlabel('$\\sigma$')
ax6.set_ylabel('$t$')
ax6.set_title('Symmetry $\\xi(s) = \\xi(1-s)$\\nBlue: s, Red: 1-s')
ax6.set_xlim(0, 1)
ax6.set_ylim(t_min, t_max)
ax6.grid(True, alpha=0.3)

# Add text about symmetry error
if symmetry_errors:
    mean_error = np.mean(symmetry_errors)
    max_error = np.max(symmetry_errors)
    ax6.text(0.02, 0.98, f'Mean |ξ(s)-ξ(1-s)|: {mean_error:.2e}\\nMax: {max_error:.2e}',
             transform=ax6.transAxes, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.suptitle('Symmetry Properties of the Completed Zeta Function $\\xi(s)$', fontsize=16)
plt.tight_layout()
plt.savefig('xi_symmetry.png', dpi=150)
print("Saved xi_symmetry.png")

# Print some symmetry statistics
print("\nSymmetry check: ξ(s) = ξ(1-s)")
test_points = [(0.3, 10), (0.4, 20), (0.6, 30), (0.7, 40), (0.2, 5), (0.8, 15)]
errors = []
for sigma, t in test_points:
    s = mp.mpc(sigma, t)
    s_ref = mp.mpc(1-sigma, t)
    val_s = xi(s)
    val_ref = xi(s_ref)
    error = abs(val_s - val_ref)
    errors.append(error)
    print(f"  s={sigma}+{t}i: |ξ(s)-ξ(1-s)| = {error:.2e}")
print(f"  Mean error: {np.mean(errors):.2e}")
print(f"  Max error:  {np.max(errors):.2e}")

# Also check the other symmetry: ξ(s) = conjugate of ξ(conjugate(s))
print("\nConjugation symmetry: ξ(s) = conjugate(ξ(conjugate(s)))")
conj_errors = []
for sigma, t in test_points:
    s = mp.mpc(sigma, t)
    s_conj = mp.mpc(sigma, -t)
    val_s = xi(s)
    val_conj = xi(s_conj)
    error = abs(val_s - val_conj.conjugate())
    conj_errors.append(error)
    print(f"  s={sigma}+{t}i: |ξ(s)-conj(ξ(conj(s)))| = {error:.2e}")
print(f"  Mean error: {np.mean(conj_errors):.2e}")
print(f"  Max error:  {np.max(conj_errors):.2e}")