# TD MODELISATION - INFORMATIQUE
# PARTIE 2 : GEOLOGIE STRUCTURALE
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from osgeo import gdal
from scipy.ndimage import gaussian_filter


# ============================================================
# ETAPE 1 - LECTURE DES DONNEES
# ============================================================

# Lecture des deux fichiers CSV
#
# Les fichiers contiennent 4 lignes avant les données numériques.
# On utilise donc skiprows=4.

data1 = np.loadtxt(
    "besson_banc1.csv",
    delimiter=",",
    skiprows=4
)

data2 = np.loadtxt(
    "besson_banc2.csv",
    delimiter=",",
    skiprows=4
)


print("Dimensions banc 1 :", data1.shape)
print("Dimensions banc 2 :", data2.shape)
