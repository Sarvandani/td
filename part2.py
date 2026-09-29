import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# Chemin vers le fichier de données
# Le fichier .txt est dans le même dossier que part2.py
fichier = Path(__file__).resolve().parent / "temperatures_38.25_96.75.txt"

data = pd.read_csv(
    fichier,
    header=None,
    names=["dates", "dates_decimales", "Temperatures"],
    parse_dates=["dates"]
)

# =============================================================================
# 2. Visualiser l'entête du DataFrame et le type des données
# =============================================================================

print("\n===== ÉTAPE 2 : Visualiser l'entête et le type des données =====")
print(data.head())

print("\nTypes des données :")
print(data.dtypes)

