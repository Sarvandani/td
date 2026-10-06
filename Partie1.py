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

# Le système de coordonnées permet de positionner l'image sur la Terre.
print("\nProjection :")
print(ds.GetProjection())

# -----------------------------------------------------------------------------
# Résolution spatiale
# -----------------------------------------------------------------------------

# Ici, un pixel représente donc une zone de 10 m × 10 m au sol.

geo = ds.GetGeoTransform()

resolution_x = geo[1]
resolution_y = abs(geo[5])  # abs() transforme -10 en 10

print("\nRésolution spatiale :")
print("Taille d'un pixel en X :", resolution_x, "m")
print("Taille d'un pixel en Y :", resolution_y, "m")

# La bande 1 du fichier correspond à Sentinel-2 B4 = Rouge.
band1 = ds.GetRasterBand(1)

# Le type de données indique comment les valeurs des pixels sont stockées.
# Par exemple :
# Byte   → 8 bits
# UInt16 → 16 bits
print("\nType de données :")
print(gdal.GetDataTypeName(band1.DataType))

# -----------------------------------------------------------------------------
# Question : Charger la bande 1 (Sentinel-2 B4 – Rouge)
# dans un tableau NumPy appelé array.
# -----------------------------------------------------------------------------

# ReadAsArray() transforme la bande raster en tableau NumPy 2D.
# Chaque case du tableau correspond à la valeur d'un pixel.
array = band1.ReadAsArray()

# array.shape donne :
# (nombre de lignes, nombre de colonnes)
print("\nDimensions du tableau :", array.shape)


# -----------------------------------------------------------------------------
# Question : Afficher cette bande en niveaux de gris avec plt.imshow().
# Tester différentes valeurs min et max pour améliorer les contrastes.
# -----------------------------------------------------------------------------

plt.figure()

# cmap="gray" affiche l'image en niveaux de gris.
#
# vmin = valeur affichée en noir
# vmax = valeur affichée en blanc
#
# Les valeurs intermédiaires apparaissent en différents niveaux de gris.
plt.imshow(array, cmap="gray", vmin=0, vmax=255)

plt.title("Bande rouge B4")
plt.colorbar()

plt.show()



