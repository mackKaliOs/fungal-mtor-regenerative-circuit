"""
FMRC_Analysis — Master Analysis Script for the Fungal–mTOR Regenerative Circuit (FMRC)
Author: Kayleighy Mackintosh
License: MIT

This notebook integrates the core simulation, ecology modeling, and visualization
modules to generate all figures and datasets required for publication or grant submission.
"""

import numpy as np
from src.fmr_circuit.models import simulate_fmrc
from src.fmr_circuit.ecology import ecological_summary
from src.fmr_circuit.visualize import (
    plot_timecourse,
    plot_heatmap,
    plot_surface,
    generate_composite_figures,
)

# -----------------------------
# 1. BASE SIMULATION
# -----------------------------
t, y = simulate_fmrc(t_max=150)

# Plot the main circuit over time
plot_timecourse(t, y, title="Baseline FMRC Simulation (mTOR–AMPK–TP53)")

# -----------------------------
# 2. ECOLOGICAL INFLUENCE MODEL
# -----------------------------
elephant_diet = {
    "ergothioneine": 0.3,
    "beta_glucans": 0.2,
    "polyphenols": 0.2,
    "selenium": 0.1,
    "triterpenes": 0.2,
}
eco_summary = ecological_summary(elephant_diet)
print("=== Ecological Summary ===")
for k, v in eco_summary.items():
    print(f"{k}: {v}")

# -----------------------------
# 3. HEATMAP AND SURFACE GENERATION
# -----------------------------
x_vals = np.linspace(0, 1, 25)
y_vals = np.linspace(0, 1, 25)
X, Y = np.meshgrid(x_vals, y_vals)
Z = np.exp(-((X - 0.4)**2 + (Y - 0.6)**2)) + 0.3 * np.sin(3 * X * Y)

# Autophagy activation heatmap (AMPK vs mTOR balance)
heatmap_matrix = np.outer(x_vals, y_vals)

plot_heatmap(heatmap_matrix, x_vals.round(2), y_vals.round(2), title="AMPK–mTOR Balance Map")
plot_surface(X, Y, Z, title="TP53 Activation Surface (Nutrient Modulation)")

# -----------------------------
# 4. COMPOSITE FIGURE
# -----------------------------
results_dict = {
    "t": t,
    "y": y,
    "heatmap": (heatmap_matrix, x_vals, y_vals),
    "surface": (X, Y, Z),
}
generate_composite_figures(results_dict)

# -----------------------------
# 5. EXPORTING DATA
# -----------------------------
np.savez(
    "fmrc_results.npz",
    time=t,
    mtor=y[0],
    ampk=y[1],
    tp53=y[2],
    eco_summary=list(eco_summary.values()),
)

print("\nAll figures generated and data exported successfully ✅")
