import mpmath as mp
import numpy as np
import matplotlib.pyplot as plt

mp.mp.dps = 30

def xi(s):
    return 0.5 * s * (s-1) * mp.pi**(-s/2) * mp.gamma(s/2) * mp.zeta(s)

# Search for sigma where Im(xi)=0 for a range of t
sigmas = np.linspace(0, 1, 21)  # 0 to 1 inclusive
t_max = 50
t_step = 0.5
ts = np.arange(0, t_max + t_step, t_step)

# We'll look for points where |Im(xi)| is small relative to |xi|
candidates = []
for sigma in sigmas:
    for t in ts:
        s = mp.mpc(sigma, t)
        # Avoid gamma pole at s=0, -2, -4,... (only s=0 in our range)
        if abs(s) < 1e-12:
            continue
        # Avoid zeta pole at s=1
        if abs(s - 1) < 1e-12:
            continue
        val = xi(s)
        if abs(val) < 1e-12:  # near zero, skip (these are zeros on critical line maybe)
            continue
        rel_im = abs(val.imag) / abs(val)
        if rel_im < 1e-3:  # relatively small imaginary part
            candidates.append((sigma, t, val))

print("Number of candidate points where xi is nearly real:", len(candidates))
if candidates:
    # Group by sigma to see if any sigma != 0.5 appears frequently
    sigma_counts = {}
    for sigma, t, val in candidates:
        key = round(sigma, 2)
        sigma_counts[key] = sigma_counts.get(key, 0) + 1
    print("Counts per sigma (rounded to 0.01):")
    for sigma in sorted(sigma_counts):
        print(f"  sigma={sigma}: {sigma_counts[sigma]} points")
    # Show some examples
    print("\nExample candidates (sigma, t, xi):")
    for sigma, t, val in candidates[:10]:
        print(f"  sigma={sigma:.3f}, t={t:.3f}, xi={val}")
else:
    print("No candidates found with the given threshold.")

# Also check where derivative of xi w.r.t s is zero? Might be heavy.
# Instead, let's plot xi along a few vertical lines to see its phase.
sigmas_to_plot = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
plt.figure(figsize=(12, 8))
for i, sigma in enumerate(sigmas_to_plot):
    plt.subplot(3, 3, i+1)
    vals = []
    for t in ts:
        s = mp.mpc(sigma, t)
        vals.append(xi(s))
    reals = [v.real for v in vals]
    imags = [v.imag for v in vals]
    plt.plot(ts, reals, label='Re(xi)')
    plt.plot(ts, imags, label='Im(xi)')
    plt.axhline(y=0, color='k', linewidth=0.5, alpha=0.5)
    plt.xlabel('t')
    plt.ylabel('xi')
    plt.title(f'xi(s) for sigma={sigma}')
    plt.legend(fontsize=8)
    plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('xi_vertical_lines.png', dpi=150)
print("\nSaved xi_vertical_lines.png")