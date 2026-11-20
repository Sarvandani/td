"""
TD MODÉLISATION – INFORMATIQUE
PARTIE 2 : EXERCICE DE GÉOLOGIE STRUCTURALE

Énoncé : analyse-MNT.pdf, pages 4 et 5.
"""

# ============================================================
# BIBLIOTHÈQUES UTILISÉES
# ============================================================
# pathlib.Path : localiser les fichiers dans le dossier du script.
#
# NumPy (np) :
#   loadtxt()      : lire les fichiers CSV.
#   column_stack() : construire une matrice pour la régression.
#   linalg.lstsq() : ajuster un plan par les moindres carrés.
#   arctan2()      : calculer un angle d'orientation.
#   hypot()        : calculer la norme de deux composantes.
#   meshgrid()     : créer une grille de coordonnées.
#
# GDAL :
#   Open()         : ouvrir un fichier raster GeoTIFF.
#   ReadAsArray()  : lire la bande du raster dans un tableau NumPy.
#   GetGeoTransform() : récupérer les coordonnées spatiales.
#
# Matplotlib :
#   imshow()       : afficher le MNT ombré.
#   scatter()      : afficher les points des bancs.
#   plot_surface() : afficher les plans en 3D.
#   show()         : afficher les figures dans des fenêtres séparées.

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from osgeo import gdal


def main():

    # ========================================================
    # ÉTAPE 1 – LECTURE DES DONNÉES (énoncé, page 4)
    # ========================================================
    # Objectifs :
    # - Charger les deux fichiers CSV avec NumPy.
    # - Ignorer les premières lignes avec skiprows.
    # - Extraire les coordonnées Est, Nord et altitude.
    # - Afficher les mesures sur le MNT ombré.
    #
    # Path(__file__).resolve().parent :
    #   trouver le dossier où se trouve ce programme.
    #
    # np.loadtxt() :
    #   lire les valeurs numériques des fichiers CSV.
    #
    # delimiter="," :
    #   indiquer que les colonnes sont séparées par des virgules.
    #
    # skiprows=4 :
    #   ignorer les quatre lignes de métadonnées au début des CSV.

    # Dossier contenant le programme et les fichiers.
    dossier = Path(__file__).resolve().parent

    # Lire les deux fichiers CSV.
    banc1 = np.loadtxt(
        dossier / "besson_banc1.csv",
        delimiter=",",
        skiprows=4
    )

    banc2 = np.loadtxt(
        dossier / "besson_banc2.csv",
        delimiter=",",
        skiprows=4
    )

    # Extraire les trois colonnes :
    # colonne 0 : Est (X)
    # colonne 1 : Nord (Y)
    # colonne 2 : altitude (Z)
    #
    # .T permet de transposer le tableau.
    x1, y1, z1 = banc1.T
    x2, y2, z2 = banc2.T

    # Afficher le nombre de points de chaque banc.
    print(f"Banc 1 : {len(x1)} points")
    print(f"Banc 2 : {len(x2)} points")

    

if __name__ == "__main__":
    main()

