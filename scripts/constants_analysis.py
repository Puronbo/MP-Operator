import mpmath as mp
import numpy as np
import matplotlib.pyplot as plt

mp.mp.dps = 50

def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    limit = int(mp.sqrt(n))
    for i in range(3, limit+1, 2):
        if n % i == 0:
            return False
    return True

print("Mathematical constants related to the Riemann zeta function")
print("="*60)

# Euler-Mascheroni gamma
gamma_euler = mp.euler
print("Euler-Mascheroni constant gamma =", gamma_euler)

# Pi
pi = mp.pi
print("pi =", pi)

# Euler's number e
e = mp.e
print("e =", e)

# Glaisher-Kinkelin constant A (approximate via limit definition)
def glaisher_akin(n):
    log_product = 0
    for k in range(1, n+1):
        log_product += k * mp.log(k)
    term = (n**2)/2 + n/2 + mp.mpf(1)/12
    log_den = term * mp.log(n) - n**2/4
    return mp.e**(log_product - log_den)
A_approx = glaisher_akin(10000)
print("Glaisher-Kinkelin constant A ~", A_approx, "(n=10000)")

# Twin prime constant C2 = ∏_{p≥2} (1 - 1/(p-1)^2)
def twin_prime_const(limit=200000):
    prod = mp.mpf(1)
    p = 2
    while p <= limit:
        if is_prime(p):
            prod *= 1 - 1/( (p-1)**2 )
        p += 1 if p==2 else 2
    return prod
C2_approx = twin_prime_const(200000)
print("Twin prime constant C2 ~", C2_approx, "(primes up to 200k)")

# Stieltjes constants gamma_n (coefficients in Laurent expansion of zeta(s) at s=1)
print("\nStieltjes constants gamma_n (from Laurent series ζ(s) = 1/(s-1) + Σ_{n=0}∞ (-1)^n gamma_n (s-1)^n / n!):")
for n in range(0, 6):
    gamma_n = mp.stieltjes(n)
    print("gamma_{} =".format(n), gamma_n)

# Values of zeta and related functions at special points
print("\nSpecial values:")
print("zeta'(0) = -1/2 * ln(2π) =", -0.5 * mp.log(2*mp.pi))
print("xi(0) = 1/2 =", 0.5)
# Define xi(s)
def xi(s):
    return 0.5 * s * (s-1) * mp.pi**(-s/2) * mp.gamma(s/2) * mp.zeta(s)
print("xi(0) via definition =", xi(0))
print("xi(1/2) =", xi(0.5))

# Mertens constant B1 (Meissel-Mertens constant)
def mertens_const(limit=200000):
    total = mp.euler
    p = 2
    while p <= limit:
        if is_prime(p):
            total += mp.log(1 - 1/p) + 1/p
        p += 1 if p==2 else 2
    return total
M_approx = mertens_const(200000)
print("Meissel-Mertens constant M ~", M_approx, "(primes up to 200k)")

# Now create a plot: place constants on a number line
constants = {
    "gamma (Euler-Mascheroni)": gamma_euler,
    "pi": pi,
    "e": e,
    "A (Glaisher–Kinkelin)": A_approx,
    "C2 (Twin prime)": C2_approx,
    "M (Mertens)": M_approx,
    "zeta'(0)": -0.5 * mp.log(2*mp.pi),
    "xi(0)": 0.5,
    "gamma_0": mp.stieltjes(0),
    "gamma_1": mp.stieltjes(1),
    "gamma_2": mp.stieltjes(2),
}
# Filter out any that are not finite
filtered = {}
for k, v in constants.items():
    if mp.isfinite(v):
        filtered[k] = v

# Sort by value
sorted_items = sorted(filtered.items(), key=lambda x: x[1])
labels = [item[0] for item in sorted_items]
values = [float(item[1]) for item in sorted_items]  # convert to float for plotting

plt.figure(figsize=(10, 2))
plt.hlines(1, xmin=min(values)*0.9, xmax=max(values)*1.1, color='gray', linewidth=2)
plt.scatter(values, [1]*len(values), color='red', zorder=5)
for i, (label, val) in enumerate(zip(labels, values)):
    plt.text(val, 1.02, label, rotation=45, ha='left', va='bottom', fontsize=9)
plt.yticks([])
plt.xlabel('Value')
plt.title('Mathematical constants related to the Riemann zeta function')
plt.grid(True, axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig('constants_analysis.png', dpi=150)
print("\nSaved constants_analysis.png")