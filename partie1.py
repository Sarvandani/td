from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt


# =============================================================================
# ÉTAPE 1 – EXPLORATION DES MÉTADONNÉES ET AFFICHAGE D'UNE BANDE
# =============================================================================


# -----------------------------------------------------------------------------
# Question : Ouvrir le fichier TIFF avec GDAL.
# -----------------------------------------------------------------------------

fichier = "2025-07-25-00_Sentinel-2_L2A_B4B3B2B8.tiff"

# Ouvrir le fichier raster.
ds = gdal.Open(fichier)

# RasterXSize = nombre de colonnes (largeur en pixels)
# RasterYSize = nombre de lignes (hauteur en pixels)
# RasterCount = nombre de bandes
print("Nombre de colonnes :", ds.RasterXSize)
print("Nombre de lignes :", ds.RasterYSize)
print("Nombre de bandes :", ds.RasterCount)
