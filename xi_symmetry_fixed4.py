import mpmath as mp
import numpy as np
import matplotlib.pyplot as plt

mp.mp.dps = 30

def xi(s):
    return 0.5 * s * (s-1) * mp.pi**(-s/2) * mp.gamma(s/2) * mp.zeta(s)

# Create a grid in the critical strip
sigma_min, sigma_max = 0, 1
t_min, t_max = 0, 30
resolution = 300

sigma_vals = np.linspace(sigma_min, sigma_max, resolution)
t_vals = np.linspace(t_min, t_max, resolution)
Sigma, T = np.meshgrid(sigma_vals, t_vals)

mag = np.zeros((resolution, resolution))
phase = np.zeros((resolution, resolution))
real_part = np.zeros((resolution, resolution))
imag_part = np.zeros((resolution, resolution))

for i in range(resolution):
    for j in range(resolution):
        s = mp.mpc(Sigma[i,j], T[i,j])
        if abs(s) < 1e-12 or abs(s-1) < 1e-12:
            mag[i,j] = np.nan
            phase[i,j] = np.nan
            real_part[i,j] = np.nan
            imag_part[i,j] = np.nan
        else:
            val = xi(s)
            mag[i,j] = abs(val)
            phase[i,j] = mp.atan2(val.imag, val.real)
            real_part[i,j] = val.real
            imag_part[i,j] = val.imag

# Plot
fig = plt.figure(figsize=(16, 12))

# Panel 1: |xi(s)|
ax1 = plt.subplot(2, 3, 1)
mag_masked = np.ma.masked_invalid(mag)
im1 = ax1.imshow(mag_masked.T, extent=[sigma_min, sigma_max, t_min, t_max],
                 origin='lower', aspect='auto', cmap='viridis')
ax1.set_xlabel('$\\sigma = \\Re(s)$')
ax1.set_ylabel('$t = \\Im(s)$')
ax1.set_title('$|\\xi(s)|$')
plt.colorbar(im1, ax=ax1)

# Panel 2: Phase
ax2 = plt.subplot(2, 3, 2)
phase_masked = np.ma.masked_invalid(phase)
im2 = ax2.imshow(phase_masked.T, extent=[sigma_min, sigma_max, t_min, t_max],
                 origin='lower', aspect='auto', cmap='hsv')
ax2.set_xlabel('$\\sigma = \\Re(s)$')
ax2.set_ylabel('$t = \\Im(s)$')
ax2.set_title('$\\arg\\xi(s)$')
plt.colorbar(im2, ax=ax2)

# Panel 3: Real part
ax3 = plt.subplot(2, 3, 3)
real_masked = np.ma.masked_invalid(real_part)
im3 = ax3.imshow(real_masked.T, extent=[sigma_min, sigma_max, t_min, t_max],
                 origin='lower', aspect='auto', cmap='RdBu')
ax3.set_xlabel('$\\sigma = \\Re(s)$')
ax3.set_ylabel('$t = \\Im(s)$')
ax3.set_title('$\\Re\\xi(s)$')
plt.colorbar(im3, ax=ax3)

# Panel 4: Imaginary part
ax4 = plt.subplot(2, 3, 4)
imag_masked = np.ma.masked_invalid(imag_part)
im4 = ax4.imshow(imag_masked.T, extent=[sigma_min, sigma_max, t_min, t_max],
                 origin='lower', aspect='auto', cmap='RdBu')
ax4.set_xlabel('$\\sigma = \\Re(s)$')
ax4.set_ylabel('$t = \\Im(s)$')
ax4.set_title('$\\Im\\xi(s)$')
plt.colorbar(im4, ax=ax4)
ax4.axvline(x=0.5, color='yellow', linestyle='--', linewidth=2)

# Panel 5: xi(s) on critical line
ax5 = plt.subplot(2, 3, 5)
t_critical = np.linspace(t_min, t_max, 1000)
xi_crit_real = []
xi_crit_imag = []
for t in t_critical:
    s = mp.mpc(0.5, t)
    val = xi(s)
    xi_crit_real.append(val.real)
    xi_crit_imag.append(val.imag)
ax5.plot(t_critical, xi_crit_real, 'b-', label='Re')
ax5.plot(t_critical, xi_crit_imag, 'r--', label='Im')
ax5.axhline(y=0, color='k', linewidth=0.5)
ax5.set_xlabel('$t$')
ax5.set_ylabel('$\\xi(1/2+it)$')
ax5.set_title('$\\xi(s)$ on $\\sigma=1/2$')
ax5.legend()
ax5.grid(True, alpha=0.3)

# Panel 6: Symmetry xi(s) vs xi(1-s)
ax6 = plt.subplot(2, 3, 6)
test_sigmas = [0.3, 0.4, 0.6, 0.7]
test_t = [10, 20, 30]
errors = []
for sigma in test_sigmas:
    for t in test_t:
        s = mp.mpc(sigma, t)
        s_ref = mp.mpc(1-sigma, t)
        val_s = xi(s)
        val_ref = xi(s_ref)
        err = abs(val_s - val_ref)
        errors.append(err)
        ax6.plot([sigma, 1-sigma], [t, t], 'k-', alpha=0.2)
        ax6.plot(sigma, t, 'bo', markersize=4)
        ax6.plot(1-sigma, t, 'ro', markersize=4)
ax6.set_xlabel('$\\sigma$')
ax6.set_ylabel('$t$')
ax6.set_title('Symmetry $\\xi(s)=\\xi(1-s)$')
ax6.set_xlim(0,1)
ax6.set_ylim(t_min, t_max)
ax6.grid(True, alpha=0.3)
if errors:
    # convert to float for formatting
    errors_float = [float(e) for e in errors]
    mean_err = np.mean(errors_float)
    max_err = np.max(errors_float)
    ax6.text(0.02, 0.98, f'Mean err: {mean_err:.2e}\\nMax err: {max_err:.2e}',
             transform=ax6.transAxes, va='top',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.suptitle('Symmetry of Completed Zeta Function $\\xi(s)$', fontsize=16)
plt.tight_layout()
plt.savefig('xi_symmetry_fixed4.png', dpi=150)
print("Saved xi_symmetry_fixed4.png")

# Print symmetry stats
print("\nSymmetry check ξ(s)=ξ(1-s):")
test_points = [(0.3,10),(0.4,20),(0.6,30),(0.7,40),(0.2,5),(0.8,15)]
errs = []
for sigma,t in test_points:
    s = mp.mpc(sigma,t)
    sref = mp.mpc(1-sigma,t)
    err = abs(xi(s)-xi(sref))
    errs.append(err)
    print(f"  s={sigma}+{t}i: err={err:.2e}")
errs_float = [float(e) for e in errs]
print(f"Mean: {np.mean(errs_float):.2e}, Max: {np.max(errs_float):.2e}")

# Conjugation symmetry
print("\nConjugation check ξ(s)=conj(ξ(conj(s))):")
conj_errs = []
for sigma,t in test_points:
    s = mp.mpc(sigma,t)
    sconj = mp.mpc(sigma,-t)
    err = abs(xi(s)-xi(sconj).conjugate())
    conj_errs.append(err)
    print(f"  s={sigma}+{t}i: err={err:.2e}")
conj_errs_float = [float(e) for e in conj_errs]
print(f"Mean: {np.mean(conj_errs_float):.2e}, Max: {np.max(conj_errs_float):.2e}")