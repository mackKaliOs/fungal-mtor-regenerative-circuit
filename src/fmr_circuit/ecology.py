"""
ecology.py — Ecological and biochemical modeling for the Fungal–mTOR Regenerative Circuit (FMRC)
Author: Kayleighy Mackintosh
License: MIT

This module simulates how environmental metabolites (ergothioneine, polyphenols, etc.)
modulate cellular equilibrium across ecological and physiological scales.
"""

import numpy as np

# Define the core ecological compounds relevant to FMRC
COMPOUNDS = {
    "ergothioneine": {"antioxidant_power": 0.9, "mTOR_mod": -0.3, "AMPK_mod": 0.5},
    "beta_glucans": {"antioxidant_power": 0.7, "mTOR_mod": -0.2, "AMPK_mod": 0.4},
    "polyphenols": {"antioxidant_power": 0.6, "mTOR_mod": -0.15, "AMPK_mod": 0.3},
    "selenium": {"antioxidant_power": 0.5, "mTOR_mod": -0.1, "AMPK_mod": 0.25},
    "triterpenes": {"antioxidant_power": 0.8, "mTOR_mod": -0.25, "AMPK_mod": 0.35},
}


def compute_antioxidant_index(diet_profile):
    """
    Computes an ecological antioxidant index from a given diet profile.
    diet_profile = dict of {compound_name: intake_fraction}
    Returns weighted antioxidant score (0-1)
    """
    total = 0
    for compound, frac in diet_profile.items():
        if compound in COMPOUNDS:
            total += frac * COMPOUNDS[compound]["antioxidant_power"]
    return np.clip(total, 0, 1)


def compute_mtor_ampk_shift(diet_profile):
    """
    Estimates overall mTOR and AMPK modulation based on dietary metabolites.
    Returns (mTOR_shift, AMPK_shift)
    """
    mtor_shift, ampk_shift = 0, 0
    for compound, frac in diet_profile.items():
        if compound in COMPOUNDS:
            mtor_shift += frac * COMPOUNDS[compound]["mTOR_mod"]
            ampk_shift += frac * COMPOUNDS[compound]["AMPK_mod"]
    return mtor_shift, ampk_shift


def ecological_summary(diet_profile):
    """
    Generate an ecological summary dictionary with key parameters.
    """
    antioxidant = compute_antioxidant_index(diet_profile)
    mtor_shift, ampk_shift = compute_mtor_ampk_shift(diet_profile)
    resilience = np.clip((antioxidant + ampk_shift - abs(mtor_shift)) / 2, 0, 1)

    return {
        "Antioxidant_Index": round(antioxidant, 3),
        "mTOR_Modulation": round(mtor_shift, 3),
        "AMPK_Modulation": round(ampk_shift, 3),
        "Cellular_Resilience": round(resilience, 3),
    }


if __name__ == "__main__":
    # Example simulation — elephant-inspired plant diet
    elephant_diet = {
        "ergothioneine": 0.3,
        "beta_glucans": 0.2,
        "polyphenols": 0.2,
        "selenium": 0.1,
        "triterpenes": 0.2,
    }

    print("Ecological Summary (Elephant Diet Analogue):")
    print(ecological_summary(elephant_diet))
