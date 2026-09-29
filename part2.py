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


# =============================================================================
# 3. Afficher la colonne Temperatures, la 3ème ligne
#    et le 4ème élément de la 3ème colonne
# =============================================================================

print("\n===== ÉTAPE 3 : =====")

# Colonne Temperatures
print("\nColonne Temperatures :")
print(data["Temperatures"])

# Troisième ligne
print("\n3ème ligne :")
print(data.iloc[2])

# Quatrième élément de la troisième colonne
print("\n4ème élément de la 3ème colonne :")
print(data.iloc[3, 2])


