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

# data cleaning: Supprimer les éventuelles valeurs invalides
valides = np.isfinite(dates_decimales) & np.isfinite(temperatures)

dates_decimales = dates_decimales[valides]
temperatures = temperatures[valides]

# Temps en années depuis 2000
t = dates_decimales - 2000.0

# Vecteur des données expérimentales
d = temperatures

# =============================================================================
# Construire la matrice du modèle G
# =============================================================================

# Nombre de mesures de température
N = len(t)

# Le modèle contient 4 coefficients inconnus :
# T(t) = A*cos(2πt) + B*sin(2πt) + C*t + D
#          saisonnier     saisonnier    tendance  constante
M = 4

# Création de la matrice G : N mesures × 4 coefficients
G = np.zeros((N, M))

# Chaque colonne de G correspond à un coefficient du modèle
G[:, 0] = np.cos(2 * np.pi * t)  # coefficient A
G[:, 1] = np.sin(2 * np.pi * t)  # coefficient B
G[:, 2] = t                       # coefficient C : tendance linéaire
G[:, 3] = 1.0                     # coefficient D : constante

# =============================================================================
# Estimer A, B, C et D par la méthode des moindres carrés
# =============================================================================

# On cherche les coefficients qui ajustent au mieux
# le modèle aux températures mesurées : G @ m ≈ d
m, residuals, rank, s = np.linalg.lstsq(
    G,
    d,
    rcond=None
)

# Récupération des 4 coefficients estimés
A, B, C, D = m

print("Coefficients du modèle :")
print(f"A = {A:.6f}")
print(f"B = {B:.6f}")
print(f"C = {C:.6f}")
print(f"D = {D:.6f}")
# Calculer les températures modélisées
temperatures_modele = G @ m

# =============================================================================
# 1. Afficher les températures
# =============================================================================

plt.plot(
    dates_decimales,
    temperatures,
    linewidth=0.5,
    label="Températures"
)

# =============================================================================
# 2. Déterminer l'amplitude pic-à-pic
# =============================================================================

amplitude = np.sqrt(A**2 + B**2)

amplitude_pic_a_pic = 2 * amplitude

print(f"\nAmplitude pic-à-pic : {amplitude_pic_a_pic:.1f} °C")

# =============================================================================
# 3. Identifier la date des maximums de température (phase)
# =============================================================================

phase = np.arctan2(B, A)

date_maximum = np.mod(
    phase / (2 * np.pi),
    1
)

print(f"Date du maximum : {date_maximum:.2f}")








