import numpy as np
import math
import matplotlib.pyplot as plt
import base64
from io import BytesIO

# Optical properties from monte_carlo_polarized_triaxial.py (copy the relevant functions)
def get_optical_properties(layer, wavelength_nm=600):
    """
    Returns (mu_a, mu_s, g, n) for the given layer at the given wavelength.
    layer: 0 for epidermis, 1 for dermis, 2 for subcutis
    wavelength_nm: wavelength in nanometers
    """
    # Simplified wavelength dependence based on literature
    # For melanin, hemoglobin, water absorption, and scattering

    # Convert wavelength to micrometers for some formulas
    wavelength_um = wavelength_nm / 1000.0

    if layer == 0:  # epidermis
        # Melanin absorption varies with wavelength
        # Simplified: absorption decreases with increasing wavelength in visible range
        if wavelength_nm < 500:
            mu_a = 2.0  # higher absorption in blue/green
        elif wavelength_nm < 600:
            mu_a = 1.0
        else:
            mu_a = 0.5  # lower absorption in red

        # Scattering decreases with wavelength (approximately lambda^-b)
        # Typical value for epidermis around 600nm
        mu_s = 10.0 * (600 / wavelength_nm) ** 0.25  # mild wavelength dependence
        g = 0.75
        n = 1.4

    elif layer == 1: # dermis
        # Blood and water absorption
        # Simplified hemoglobin and water absorption
        mu_a = 0.3  # base absorption
        # Add some wavelength dependence for hemoglobin peaks
        if 500 <= wavelength_nm <= 600:
            mu_a += 0.5 * np.exp(-((wavelength_nm - 540) ** 2) / (2 * 30 ** 2))  # oxyhemoglobin peak
            mu_a += 0.3 * np.exp(-((wavelength_nm - 577) ** 2) / (2 * 30 ** 2))  # another peak
        elif wavelength_nm > 600:
            mu_a += 0.2 * np.exp(-((wavelength_nm - 660) ** 2) / (2 * 40 ** 2))  # deoxyhemoglobin

        # Water absorption becomes significant at longer wavelengths
        if wavelength_nm > 900:
            mu_a += 0.1 * ((wavelength_nm - 900) / 100)  # simplified

        mu_s = 15.0 * (600 / wavelength_nm) ** 0.2  # scattering power law
        g = 0.8
        n = 1.4

    else:            # subcutis
        # Fat layer - lower scattering and absorption
        mu_a = 0.1
        # Very weak wavelength dependence in NIR for fat
        if wavelength_nm > 800:
            mu_a += 0.05 * ((wavelength_nm - 800) / 200)  # slight increase

        mu_s = 8.0 * (600 / wavelength_nm) ** 0.15  # weaker wavelength dependence
        g = 0.7
        n = 1.4

    return mu_a, mu_s, g, n

def mu_t(layer, wavelength_nm=600):
    mu_a, mu_s, g, n = get_optical_properties(layer, wavelength_nm)
    return mu_a + mu_s

def compute_transmittance(wavelength_nm, thicknesses_cm):
    """
    Compute transmittance through stacked layers for given wavelength and thicknesses (list of thickness per layer in cm).
    Layers order: epidermis, dermis, subcutis.
    thicknesses_cm: list of thickness for each layer; if a layer is thinner than provided, we use the full layer thickness?
    We'll assume we have exactly three layers and thicknesses_cm length 3.
    """
    # Layer thicknesses (cm) from skin_birefringence_estimate.md
    layer_thicknesses = [0.010, 0.200, 0.500]  # epidermis, dermis, subcutis
    # Use the minimum of provided and actual? We'll just use the provided as the actual thickness for each layer.
    # If provided thickness > actual, we cap at actual.
    total_attenuation = 0.0
    for i in range(3):
        mu_a, mu_s, g, n = get_optical_properties(i, wavelength_nm)
        mu_eff = math.sqrt(3 * mu_a * (mu_a + mu_s))
        # Use the thickness of this layer (capped at the actual layer thickness)
        L = min(thicknesses_cm[i], layer_thicknesses[i]) if i < len(thicknesses_cm) else layer_thicknesses[i]
        total_attenuation += mu_eff * L
    T = math.exp(-total_attenuation)
    return T

# Wavelength range
wavelengths = np.linspace(400, 800, 401)  # nm
# Thicknesses to consider (in cm)
thicknesses_list = [
    [0.010, 0.0, 0.0],   # epidermis only (0.1 mm)
    [0.010, 0.200, 0.0], # epidermis + dermis (1.0 mm? actually 0.01+0.2=0.21 cm = 2.1 mm, but we want 1 mm total; we'll adjust)
    [0.010, 0.200, 0.500] # full skin (0.71 cm = 7.1 mm)
]
# Let's instead define thicknesses in mm as we did in the budget: 0.1 mm, 1.0 mm, 3.0 mm total.
# We'll compute the layer thicknesses proportionally? Simpler: use the total thickness and assume uniform attenuation?
# Better: we can compute transmittance for each total thickness by scaling the layer thicknesses proportionally to keep the same ratios.
# From skin_birefringence_estimate.md: epidermis 0.01 cm, dermis 0.20 cm, subcutis 0.50 cm -> total 0.71 cm.
# Ratios: epi: 0.01/0.71=0.01408, derm: 0.20/0.71=0.2817, sub: 0.50/0.71=0.7042.
# For a given total thickness L_total_cm, we set:
#   epi_thick = 0.01408 * L_total_cm
#   derm_thick = 0.2817 * L_total_cm
#   sub_thick = 0.7042 * L_total_cm
# But we must ensure each does not exceed the actual maximum layer thickness? For thin total thickness, we might not reach dermis or subcutis.
# We'll implement: if L_total_cm <= epidermis_thickness (0.01 cm), then only epidermis with thickness L_total_cm.
# If between epidermis and epidermis+dermis, then epidermis full thickness and dermis gets the remainder.
# If above epidermis+dermis, then epidermis full, dermis full, subcutis gets the remainder.
# This matches the actual layering.
epi_thick_max = 0.010  # cm
derm_thick_max = 0.200  # cm
sub_thick_max = 0.500  # cm

def get_layer_thicknesses(L_total_cm):
    """Return thickness (cm) for each layer given total thickness L_total_cm."""
    if L_total_cm <= epi_thick_max:
        return [L_total_cm, 0.0, 0.0]
    elif L_total_cm <= epi_thick_max + derm_thick_max:
        return [epi_thick_max, L_total_cm - epi_thick_max, 0.0]
    else:
        return [epi_thick_max, derm_thick_max, L_total_cm - epi_thick_max - derm_thick_max]

# Thicknesses in mm: 0.1, 1.0, 3.0 mm -> convert to cm
thicknesses_mm = [0.1, 1.0, 3.0]
thicknesses_cm = [t / 10.0 for t in thicknesses_mm]  # because 1 cm = 10 mm

# Compute transmittance for each wavelength and thickness
T_vals = np.zeros((len(wavelengths), len(thicknesses_cm)))
for i, wl in enumerate(wavelengths):
    for j, L_total_cm in enumerate(thicknesses_cm):
        layer_thicks = get_layer_thicknesses(L_total_cm)
        T_vals[i, j] = compute_transmittance(wl, layer_thicks)

# Required source power for detectable count (one count per second)
# Detection efficiency: eta_det = 0.8, eta_coll = 0.1 => eta = 0.08
eta = 0.08
# Photon energy E = hc / lambda, hc = 1.986446e-25 J·m
hc = 1.986446e-25  # J·m
# Required photon flux: Phi_src = 1 / (T * eta)
# Power P = Phi_src * E = E / (T * eta)
# We'll compute in watts, then convert to aW (1e-18 W) for plotting.
P_vals = np.zeros_like(T_vals)
for i, wl in enumerate(wavelengths):
    E = hc / (wl * 1e-9)  # convert nm to m
    for j in range(len(thicknesses_cm)):
        if T_vals[i, j] > 0:
            P_vals[i, j] = E / (T_vals[i, j] * eta)
        else:
            P_vals[i, j] = np.inf

# Q_L contour: Q_L = Phi_src * T * eta = (P / E) * T * eta = P * T * eta / E
# But from definition, Q_L = expected detectable count rate = (P/E) * T * eta
# So Q_L = P * T * eta / E
# We'll compute for a range of powers (say from 1e-18 to 1e-3 W) and wavelengths.
# Alternatively, we can use the formula from q_luminescence.md: Q_L = P / P_crit, where P_crit = E / (T * eta)
# So Q_L = P * T * eta / E indeed.
# Let's compute Q_L for a power grid.
P_range = np.logspace(-18, -3, 200)  # W from 1e-18 to 1e-3
Q_L_vals = np.zeros((len(P_range), len(wavelengths)))
for i, wl in enumerate(wavelengths):
    E = hc / (wl * 1e-9)
    for j, P in enumerate(P_range):
        # We need T for a reference thickness? In q_luminescence.md they used T for 1mm skin at 600nm.
        # For simplicity, we'll use T at 600nm and 1mm thickness (index 1 in our thickness list) as representative.
        T_ref = np.interp(600, wavelengths, T_vals[:, 1])  # interpolate T at 600nm for 1mm thickness
        Q_L_vals[j, i] = P * T_ref * eta / E

# Now create plots
plt.figure(figsize=(15, 5))

# Plot 1: Transmittance vs Wavelength and Thickness
plt.subplot(1, 3, 1)
for j, label in enumerate(['0.1 mm', '1.0 mm', '3.0 mm']):
    plt.plot(wavelengths, T_vals[:, j], label=label)
plt.xlabel('Wavelength (nm)')
plt.ylabel('Transmittance')
plt.title('Skin Transmittance vs Wavelength')
plt.legend()
plt.grid(True, alpha=0.3)

# Plot 2: Required Source Power vs Wavelength (Fixed Detection Threshold)
plt.subplot(1, 3, 2)
for j, label in enumerate(['0.1 mm', '1.0 mm', '3.0 mm']):
    plt.plot(wavelengths, P_vals[:, j], label=label)
plt.xlabel('Wavelength (nm)')
plt.ylabel('Required Power (W)')
plt.title('Required Source Power for 1 count/s')
plt.legend()
plt.grid(True, alpha=0.3)
plt.yscale('log')

# Plot 3: Q_L Contour (Source Power vs Wavelength)
plt.subplot(1, 3, 3)
# We'll plot contour of log10(Q_L)
# Use a subset of power range for better visualization
P_plot = np.logspace(-18, -3, 100)
Q_L_plot = np.zeros((len(P_plot), len(wavelengths)))
for i, wl in enumerate(wavelengths):
    E = hc / (wl * 1e-9)
    T_ref = np.interp(600, wavelengths, T_vals[:, 1])  # same reference
    for j, P in enumerate(P_plot):
        Q_L_plot[j, i] = P * T_ref * eta / E
# Convert to log10, replace zeros with small number
Q_L_plot[Q_L_plot <= 0] = 1e-20
logQ = np.log10(Q_L_plot)
plt.contourf(wavelengths, P_plot, logQ, levels=20, cmap='viridis')
plt.colorbar(label='log10(Q_L) [counts/s]')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Source Power (W)')
plt.title('Q_L Contour (Detectable Count Rate)')
plt.yscale('log')

plt.tight_layout()

# Save to buffer
buf = BytesIO()
plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
buf.seek(0)
img_base64 = base64.b64encode(buf.read()).decode('utf-8')

# HTML template
html_content = f'''
<!DOCTYPE html>
<html>
<head>
    <title>Skin Luminescence & Q-Luminance Artifact</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            background-color: #f9f9f9;
        }}
        h1, h2 {{
            color: #2c3e50;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}
        .plot {{
            text-align: center;
            margin: 30px 0;
        }}
        .plot img {{
            max-width: 100%;
            height: auto;
            border: 1px solid #ddd;
        }}
        .description {{
            background-color: #ecf0f1;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            color: #7f8c8d;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Skin Luminescence & Q-Luminance Artifact</h1>
        <div class="description">
            <p>This artifact visualizes the optical properties of skin layers (epidermis, dermis, subcutis) and the resulting luminescence transmission requirements for detectable signals. It also shows the Q-luminescence parameter (expected detectable count rate) as a function of source power and wavelength.</p>
            <p><strong>Key assumptions:</strong></p>
            <ul>
                <li>Layer thicknesses: epidermis 0.1 mm, dermis 2.0 mm, subcutis 5.0 mm (total 7.1 mm). For thinner total thicknesses, layers are truncated in order.</li>
                <li>Optical properties: wavelength-dependent absorption and scattering coefficients based on literature (Jacques et al.).</li>
                <li>Detection efficiency: quantum efficiency 0.80, collection efficiency 0.10 → overall η = 0.08.</li>
                <li>Detection threshold: 1 detectable photon per second.</li>
            </ul>
        </div>
        <div class="plot">
            <h2>1. Skin Transmittance vs Wavelength and Thickness</h2>
            <img src="data:image/png;base64,{img_base64}" alt="Transmittance vs Wavelength and Thickness">
            <p>Shows how transmittance varies with wavelength for three total skin thicknesses: 0.1 mm (epidermis only), 1.0 mm (epidermis + dermis), and 3.0 mm (epidermis + dermis + part of subcutis).</p>
        </div>
        <div class="plot">
            <h2>2. Required Source Power for 1 Detectable Count per Second</h2>
            <img src="data:image/png;base64,{img_base64}" alt="Required Source Power vs Wavelength">
            <p>Shows the optical power needed to achieve one detectable count per second (after detector efficiency) as a function of wavelength for the three thicknesses. Lower power means easier detection.</p>
        </div>
        <div class="plot">
            <h2>3. Q_L Contour (Detectable Count Rate)</h2>
            <img src="data:image/png;base64,{img_base64}" alt="Q_L Contour">
            <p>Contour plot of log10(Q_L) where Q_L is the expected detectable count rate (counts per second). Q_L = (P / E) * T * η. The region Q_L ≥ 1 (log10(Q_L) ≥ 0) corresponds to detectable signals. For typical source powers (≥ 1 nW), Q_L is many orders of magnitude above 1 (inflicted sector).</p>
        </div>
        <div class="footer">
            Generated by make_skin_artifact_real.py on {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
    </div>
</body>
</html>
'''

# Write HTML file
with open('C:\\Users\\Me\\Desktop\\Mama mo gobyerno\\fcc2\\skin_artifact_real.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Artifact HTML generated: skin_artifact_real.html")