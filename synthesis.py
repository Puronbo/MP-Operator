import mpmath as mp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

mp.mp.dps = 30

# ---------- Helper functions ----------
def chi_minus4(n):
    if n % 2 == 0:
        return 0
    elif n % 4 == 1:
        return 1
    elif n % 4 == 3:
        return -1
    else:
        return 0

def L_chi_minus4(t):
    N = int(np.sqrt(2 * abs(t) / np.pi))
    if N < 1:
        N = 1
    sum1 = mp.mpc(0,0)
    sum2 = mp.mpc(0,0)
    for n in range(1, N+1):
        chi = chi_minus4(n)
        if chi == 0:
            continue
        term1 = chi * (n ** (-0.5 - 1j * t))
        term2 = chi * (n ** (-0.5 + 1j * t))
        sum1 += term1
        sum2 += term2
    epsilon = -1j
    factor = (4 / (2 * np.pi)) ** (-0.5 + 1j * t)
    return sum1 + epsilon * factor * sum2

def theta_chi_minus4(t):
    return - (t/2) * mp.log(mp.pi/4) + mp.im(mp.loggamma(mp.mpc(0.75, 0.5*t)))

def Z_chi_minus4(t):
    return mp.e**(1j * theta_chi_minus4(t)) * L_chi_minus4(t)

def find_zeros(func, t_start, t_end, step=0.1):
    zeros = []
    t_prev = t_start
    f_prev = func(t_prev)
    for t in np.arange(t_start + step, t_end + step, step):
        f_curr = func(t)
        if np.real(f_prev) * np.real(f_curr) <= 0:
            t_zero = t_prev - (t - t_prev) * np.real(f_prev) / (np.real(f_curr) - np.real(f_prev))
            zeros.append(t_zero)
        t_prev = t
        f_prev = f_curr
    return zeros

def zeta_Z(t):
    theta = mp.im(mp.loggamma(mp.mpc(0.25, 0.5*t))) - (t/2)*mp.log(mp.pi)
    return mp.e**(1j * theta) * mp.zeta(0.5 + 1j*t)

# ---------- Compute zeros ----------
print("Computing zeros...")
# Zeta zeros
zeta_zeros_raw = find_zeros(zeta_Z, 0, 50, step=0.2)
refined = []
for z in zeta_zeros_raw:
    refined.extend(find_zeros(zeta_Z, z-0.5, z+0.5, step=0.01))
zeta_zeros = []
for z in refined:
    if not any(abs(z - uz) < 0.1 for uz in zeta_zeros):
        zeta_zeros.append(z)
zeta_zeros = sorted(zeta_zeros)[:20]

# L(s, chi_{-4}) zeros
chi_zeros_raw = find_zeros(Z_chi_minus4, 0, 50, step=0.2)
refined = []
for z in chi_zeros_raw:
    refined.extend(find_zeros(Z_chi_minus4, z-0.5, z+0.5, step=0.01))
chi_zeros = []
for z in refined:
    if not any(abs(z - uz) < 0.1 for uz in chi_zeros):
        chi_zeros.append(z)
chi_zeros = sorted(chi_zeros)[:20]

# ---------- Build explicit formula transform ----------
def build_F(zeros, M=12):
    N = len(zeros)
    x_vals = [10**i for i in np.linspace(1.0, 3.0, M)]  # 10^1 to 10^3
    F = np.zeros((M, N), dtype=complex)
    for k, x in enumerate(x_vals):
        for n, gamma in enumerate(zeros):
            rho = mp.mpc(0.5, gamma)
            x_rho = x ** rho
            F[k, n] = -x_rho / rho
    return F, x_vals

F_zeta, x_zeta = build_F(zeta_zeros)
F_chi, x_chi = build_F(chi_zeros)

# Adjoint and F*F
F_zeta_adj = F_zeta.conj().T
F_chi_adj = F_chi.conj().T
FtF_zeta = F_zeta_adj @ F_zeta
FtF_chi = F_chi_adj @ F_chi

# Eigenvalues
evals_zeta = np.linalg.eigvals(FtF_zeta)
evals_chi = np.linalg.eigvals(FtF_chi)
evals_zeta_real = np.real(evals_zeta)
evals_chi_real = np.real(evals_chi)

# ---------- Create synthesis figure ----------
fig = plt.figure(figsize=(16, 10))
gs = fig.add_gridspec(2, 4, hspace=0.3, wspace=0.3)

# Panel A: Folding visualization
axA = fig.add_subplot(gs[0, 0])
# Draw integer line [0,1]
axA.axhline(y=0, xmin=-0.5, xmax=1.5, color='black', linewidth=2)
axA.axvspan(0, 1, alpha=0.15, color='blue')
axA.axvline(x=0.5, color='red', linestyle='--', linewidth=2)
# Sample point folding
sample_x = 0.2
mirror_x = 1 - sample_x
axA.plot([sample_x, mirror_x], [0,0], 'o', color='green', markersize=8)
axA.annotate('', xy=(mirror_x, 0.1), xytext=(sample_x, 0.1),
             arrowprops=dict(arrowstyle='<->', color='green', lw=1.5))
axA.text((sample_x+mirror_x)/2, 0.15, 'x ↔ 1-x', ha='center', color='green', fontsize=9)
# Zeta zeros on fold line
axA.scatter([0.5]*len([g for g in zeta_zeros if g>0]), [g for g in zeta_zeros if g>0],
            color='purple', s=40, zorder=3)
axA.scatter([0.5]*len([g for g in zeta_zeros if g<0]), [g for g in zeta_zeros if g<0],
            color='purple', s=40, zorder=3)
axA.set_xlabel('Real part')
axA.set_ylabel('Imaginary part')
axA.set_title('A. Folding at Re(s)=1/2')
axA.set_xlim(-0.5, 1.5)
axA.set_ylim(-25, 25)
axA.grid(True, alpha=0.3)

# Panel B: F matrix heatmap (zeta)
axB = fig.add_subplot(gs[0, 1])
imB = axB.imshow(np.real(F_zeta), aspect='auto', cmap='RdBu')
axB.set_title('B. Re(F) for ζ(s)')
axB.set_xlabel('Zero index')
axB.set_ylabel('Test point index (log x)')
plt.colorbar(imB, ax=axB, fraction=0.046, pad=0.04)

# Panel C: F*F heatmap (zeta)
axC = fig.add_subplot(gs[0, 2])
imC = axC.imshow(np.real(FtF_zeta), aspect='auto', cmap='viridis')
axC.set_title('C. Re(F*F) for ζ(s)')
axC.set_xlabel('Zero index')
axC.set_ylabel('Zero index')
plt.colorbar(imC, ax=axC, fraction=0.046, pad=0.04)

# Panel D: Eigenvalue decay
axD = fig.add_subplot(gs[0, 3])
axD.semilogy(evals_zeta_real, 'bo-', label='ζ(s)')
axD.semilogy(evals_chi_real, 'rs--', label='L(s,χ₋₄)')
axD.set_xlabel('Eigenvalue index')
axD.set_ylabel('Eigenvalue (log scale)')
axD.set_title('D. Eigenvalue decay of F*F')
axD.legend()
axD.grid(True, alpha=0.3)

# Panel E: Schematic of adjunction
axE = fig.add_subplot(gs[1, :2])
axE.set_xlim(0, 10)
axE.set_ylim(0, 5)
axE.axis('off')
# Draw two boxes
boxP = FancyBboxPatch((1, 2), 3, 1.5, boxstyle="round,pad=0.3",
                      edgecolor='navy', facecolor='lightblue', linewidth=2)
boxZ = FancyBboxPatch((6, 2), 3, 1.5, boxstyle="round,pad=0.3",
                      edgecolor='darkgreen', facecolor='lightgreen', linewidth=2)
axE.add_patch(boxP)
axE.add_patch(boxZ)
axE.text(2.5, 2.75, 'Prime fluctuation\nspace $P$', ha='center', va='center', fontsize=12, weight='bold')
axE.text(7.5, 2.75, 'Zero contribution\nspace $Z$', ha='center', va='center', fontsize=12, weight='bold')
# Arrows for adjunction F: Z -> P and F*: P -> Z
axE.annotate('', xy=(4, 2.75), xytext=(6, 2.75),
             arrowprops=dict(arrowstyle='<-', color='red', lw=2, connectionstyle='arc3'))
axE.text(5, 3.1, '$F$', ha='center', va='bottom', color='red', fontsize=12)
axE.annotate('', xy=(6, 2.75), xytext=(4, 2.75),
             arrowprops=dict(arrowstyle='->', color='blue', lw=2, connectionstyle='arc3'))
axE.text(5, 2.3, '$F^*$', ha='center', va='top', color='blue', fontsize=12)
# Label adjunction
axE.text(5, 0.5, '$F \\dashv F^*$ (adjunction)', ha='center', va='center', fontsize=14, style='italic')
axE.set_title('E. Categorical adjunction from explicit formula')

# Panel F: Unification across L-functions (zero locations)
axF = fig.add_subplot(gs[1, 2:])
axF.scatter([0.5]*len(zeta_zeros), zeta_zeros, c='blue', s=40, label=r'$\zeta(s)$ zeros')
axF.scatter([0.5]*len(chi_zeros), chi_zeros, c='red', s=40, label=r'$L(s,\chi_{-4})$ zeros')
axF.axhline(y=0, color='black', linewidth=0.5)
axF.set_xlabel('Real part (fixed at 1/2)')
axF.set_ylabel('Imaginary part')
axF.set_title('F. Zeros on the critical line (fold)')
axF.set_xlim(0.4, 0.6)
axF.set_ylim(-50, 50)
axF.legend()
axF.grid(True, alpha=0.3)

plt.suptitle('Synthesis: Folding, Duality, and Unification in the Zeta Function', fontsize=16, y=0.98)
plt.savefig('synthesis.png', dpi=150, bbox_inches='tight')
print("Saved synthesis.png")