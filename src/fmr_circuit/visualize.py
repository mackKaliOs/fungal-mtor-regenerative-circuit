"""
visualize.py — Visualization utilities for the Fungal–mTOR Regenerative Circuit (FMRC)
Author: Kayleighy Mackintosh
License: MIT

This module generates figures and data visualizations for publications,
including time-course plots, heatmaps, and 3D surfaces that represent
metabolic balance and regenerative potential.
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D


def plot_timecourse(t, y, title="Fungal–mTOR Regenerative Circuit Dynamics"):
    """
    Plots time-series data for mTOR, AMPK, and TP53 activity.
    """
    plt.figure(figsize=(8, 5))
    plt.plot(t, y[0], label="mTOR", lw=2)
    plt.plot(t, y[1], label="AMPK", lw=2)
    plt.plot(t, y[2], label="TP53", lw=2)
    plt.xlabel("Time (arbitrary units)")
    plt.ylabel("Relative Activity")
    plt.title(title)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_heatmap(matrix, x_labels, y_labels, title="Autophagy Activation Heatmap"):
    """
    Creates a heatmap of autophagy activation or resilience scores.
    """
    plt.figure(figsize=(8, 6))
    sns.heatmap(matrix, cmap="viridis", xticklabels=x_labels, yticklabels=y_labels, cbar_kws={"label": "Activity"})
    plt.title(title)
    plt.xlabel("Parameter 1")
    plt.ylabel("Parameter 2")
    plt.tight_layout()
    plt.show()


def plot_surface(X, Y, Z, title="TP53 Activation Surface"):
    """
    Generates a 3D surface plot.
    """
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")
    surf = ax.plot_surface(X, Y, Z, cmap="plasma", linewidth=0, antialiased=True)
    ax.set_xlabel("Ergothioneine (mg/day)")
    ax.set_ylabel("Triterpenes (mg/day)")
    ax.set_zlabel("TP53 Activation (a.u.)")
    ax.set_title(title)
    fig.colorbar(surf, shrink=0.5, aspect=10, label="Activity")
    plt.tight_layout()
    plt.show()


def generate_composite_figures(results_dict):
    """
    Generates multi-panel composite of key FMRC relationships.
    results_dict = {"t": t, "y": y, "heatmap": (matrix, x, y), "surface": (X, Y, Z)}
    """
    t, y = results_dict["t"], results_dict["y"]
    heat_matrix, xlabels, ylabels = results_dict["heatmap"]
    X, Y, Z = results_dict["surface"]

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # (A) mTOR vs time
    axes[0, 0].plot(t, y[0], color="red")
    axes[0, 0].set_title("mTOR over Time")
    axes[0, 0].set_xlabel("Time")
    axes[0, 0].set_ylabel("Activity")

    # (B) Autophagy heatmap
    sns.heatmap(heat_matrix, ax=axes[0, 1], cmap="viridis")
    axes[0, 1].set_title("Autophagy Activation")

    # (C) 3D surface projected (TP53)
    surf_proj = axes[1, 0].imshow(Z, origin="lower", cmap="plasma", aspect="auto")
    axes[1, 0].set_title("TP53 Surface Projection")
    fig.colorbar(surf_proj, ax=axes[1, 0], orientation="vertical")

    # (D) Composite resilience plot
    composite_signal = np.mean(y, axis=0)
    axes[1, 1].plot(t, composite_signal, color="green")
    axes[1, 1].set_title("Composite Resilience Index")
    axes[1, 1].set_xlabel("Time")

    plt.tight_layout()
    plt.show()
