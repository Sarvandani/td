import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# =============================================================================
# PARTIE 3 – RÉGRESSIONS LINÉAIRES
# =============================================================================

# Chemin vers le fichier de données
fichier = Path(__file__).resolve().parent / "temperatures_38.25_96.75.txt"

# =============================================================================
# Application aux séries temporelles
# Modèle : T(t) = A cos(2πt) + B sin(2πt) + Ct + D
# =============================================================================

# Charger les dates décimales et les températures
dates_decimales, temperatures = np.loadtxt(
    fichier,
    delimiter=",",
    usecols=(1, 2),
    unpack=True
)



