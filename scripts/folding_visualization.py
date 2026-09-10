import mpmath as mp
import numpy as np
import matplotlib.pyplot as plt

mp.mp.dps = 30

# Compute first 10 non-trivial zeta zeros (imaginary parts)
gamma_vals = []
for n in range(1, 11):
    # Use mpmath zetazero to get the n-th zero
    gamma = mp.zetazero(n).imag
    gamma_vals.append(gamma)
    gamma_vals.append(-gamma)  # include negative for symmetry

# Create figure
fig, ax = plt.subplots(figsize=(8, 4))

# Draw the integer line (real axis) from -0.5 to 1.5
ax.axhline(y=0, xmin=-0.5, xmax=1.5, color='black', linewidth=2, zorder=1)

# Highlight the interval [0,1]
ax.axvspan(0, 1, alpha=0.2, color='blue', label='Interval [0,1]')

# Draw the fold line at x=0.5
ax.axvline(x=0.5, color='red', linestyle='--', linewidth=2, label='Fold at x=0.5 (Re(s)=1/2)')

# Show folding: for a sample point, show its mirror
sample_x = 0.2
mirror_x = 1 - sample_x
ax.plot([sample_x, mirror_x], [0, 0], 'o', color='green', markersize=8, label=f'Point {sample_x} and its mirror {mirror_x:.2f}')
ax.annotate('', xy=(mirror_x, 0.1), xytext=(sample_x, 0.1),
            arrowprops=dict(arrowstyle='<->', color='green', lw=1.5))
ax.text((sample_x+mirror_x)/2, 0.15, 'folding maps x ↔ 1-x', ha='center', color='green')

# Plot zeta zeros on the fold line (x=0.5)
# Positive gammas
ax.scatter([0.5]*len([g for g in gamma_vals if g>0]), [g for g in gamma_vals if g>0],
           color='purple', s=50, zorder=3, label=r'Zeta zeros ($\rho = 1/2 + i\gamma$)')
# Negative gammas (mirror)
ax.scatter([0.5]*len([g for g in gamma_vals if g<0]), [g for g in gamma_vals if g<0],
           color='purple', s=50, zorder=3)

# Set labels and title
ax.set_xlabel('Real part')
ax.set_ylabel('Imaginary part')
ax.set_title('Folding the Integer Line: Where 0 and 1 Meet at the Zeta Zeros')
ax.set_xlim(-0.5, 1.5)
ax.set_ylim(-30, 30)
ax.legend(loc='upper left')
ax.grid(True, alpha=0.3)

# Add text explaining
ax.text(0.02, 0.95, r'Folding at $x=\frac{1}{2}$ identifies $x$ with $1-x$',
        transform=ax.transAxes, fontsize=10, verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig('folding_visualization.png', dpi=150)
print("Saved folding_visualization.png")