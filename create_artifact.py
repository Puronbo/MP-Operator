import base64
import os

# Paths to the generated plots
sb_plot_path = 'surface_brightness_profiles.png'
intensity_plot_path = 'intensity_maps.png'

# Read and encode images
def encode_image(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode('utf-8')

sb_base64 = encode_image(sb_plot_path)
intensity_base64 = encode_image(intensity_plot_path)

# HTML content
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Monte Carlo Radiative Transfer Results</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }}
        h1 {{ color: #333; text-align: center; }}
        .container {{ display: flex; flex-wrap: wrap; justify-content: center; gap: 20px; }}
        .plot {{ background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); text-align: center; }}
        .plot img {{ max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 4px; }}
        .caption {{ margin-top: 10px; font-size: 0.9em; color: #555; }}
    </style>
</head>
<body>
    <h1>Monte Carlo Radiative Transfer Simulation Results</h1>
    <div class="container">
        <div class="plot">
            <h2>Surface Brightness Profiles</h2>
            <img src="data:image/png;base64,{sb_base64}" alt="Surface Brightness Profiles">
            <div class="caption">Surface brightness profiles for different lines of sight (impact parameter vs. surface brightness).</div>
        </div>
        <div class="plot">
            <h2>Intensity Maps</h2>
            <img src="data:image/png;base64,{intensity_base64}" alt="Intensity Maps">
            <div class="caption">Intensity maps (counts) in the plane perpendicular to each line of sight.</div>
        </div>
    </div>
</body>
</html>
"""

# Write HTML file
artifact_path = 'monte_carlo_results.html'
with open(artifact_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"HTML artifact written to {artifact_path}")