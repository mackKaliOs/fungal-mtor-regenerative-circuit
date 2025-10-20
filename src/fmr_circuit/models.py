"""
models.py — Core simulation engine for the Fungal–mTOR Regenerative Circuit (FMRC)
Author: Kayleighy Mackintosh
License: MIT

This module defines mathematical models linking mTOR, AMPK, and TP53 signaling
inspired by ergothioneine-rich Basidiomycete pathways and long-lived species' redundancy logic.
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt


def fmrc_dynamics(t, y, params):
    """
    Differential equations for the FMRC pathway.
    y = [mTOR, AMPK, TP53]
    params = dict of rate constants and feedback coefficients
    """
    mtor, ampk, tp53 = y
    k_mtor, k_ampk, k_tp53 = params["k_mtor"], params["k_ampk"], params["k_tp53"]

    # Feedback and inhibition
    d_mtor = k_mtor * (1 - ampk) - 0.3 * tp53
    d_ampk = k_ampk * (1 - mtor)
    d_tp53 = k_tp53 * (ampk - 0.2 * mtor)

    return [d_mtor, d_ampk, d_tp53]


def simulate_fmrc(t_max=100, y0=[1, 0.5, 0.2], params=None):
    if params is None:
        params = {"k_mtor": 0.8, "k_ampk": 0.6, "k_tp53": 0.4}
    t_span = (0, t_max)
    t_eval = np.linspace(0, t_max, 300)
    sol = solve_ivp(fmrc_dynamics, t_span, y0, args=(params,), t_eval=t_eval)
    return sol.t, sol.y


def plot_results(t, y):
    plt.figure(figsize=(8, 5))
    plt.plot(t, y[0], label="mTOR", linewidth=2)
    plt.plot(t, y[1], label="AMPK", linewidth=2)
    plt.plot(t, y[2], label="TP53", linewidth=2)
    plt.xlabel("Time")
    plt.ylabel("Activity")
    plt.legend()
    plt.title("Fungal–mTOR Regenerative Circuit Dynamics")
    plt.tight_layout()
    plt.show()
