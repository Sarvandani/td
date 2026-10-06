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

# -----------------------------------------------------------------------------
# Question : Calculer et afficher son histogramme avec plt.hist().
# -----------------------------------------------------------------------------

plt.figure()

plt.hist(array.ravel(), bins=100)

plt.xlabel("Valeur du pixel")
plt.ylabel("Nombre de pixels")
plt.title("Histogramme de la bande rouge")

plt.show()

# -----------------------------------------------------------------------------
# Question : Écrire une fonction d'étirement linéaire des contrastes
# entre percentiles prenant en entrée un tableau NumPy et retournant
# le tableau étiré.
# -----------------------------------------------------------------------------

def stretch(image):

  
    valeur_min, valeur_max = np.percentile(image, (2, 98))

    image_stretch = np.clip(image_stretch, 0, 1)

    return image_stretch

# Appliquer la fonction à la bande rouge.
array_stretch = stretch(array)


# Afficher le résultat.
plt.figure()

plt.imshow(
    array_stretch,
    cmap="gray",
    vmin=0,
    vmax=1
)

plt.title("Bande rouge après correction du contraste")
plt.colorbar()

plt.show()

# -----------------------------------------------------------------------------
# Question : Choisir un seuil radiométrique
# (seuil simple = moyenne - 0.5 × écart-type).
# -----------------------------------------------------------------------------

# Moyenne de toutes les valeurs des pixels.
moyenne = np.mean(array)

# L'écart-type indique à quel point les valeurs sont dispersées
# autour de la moyenne.
ecart_type = np.std(array)

# Le seuil est la valeur utilisée pour séparer deux classes.
seuil = moyenne - 0.5 * ecart_type

print("\nMoyenne :", moyenne)
print("Écart-type :", ecart_type)
print("Seuil :", seuil)


image_binaire = np.zeros(array.shape)

# array > seuil crée une condition pour tous les pixels.
#
# Si la valeur d'un pixel est supérieure au seuil,
# la valeur correspondante dans image_binaire devient 1.
#
# Les autres pixels restent à 0.
image_binaire[array > seuil] = 1

# Afficher l'image binaire.
plt.figure()

# 0 apparaît en noir et 1 en blanc.
plt.imshow(image_binaire, cmap="gray")

plt.title("Image binaire : Eau = 0, Terre = 1")
plt.colorbar()

plt.show()


# -----------------------------------------------------------------------------
# Question : Écrire une fonction set_mirror qui retourne
# une image miroir avec la commande np.flipud().
# -----------------------------------------------------------------------------

def set_mirror(image):

    # np.flipud() signifie "flip up-down".
    # Il inverse l'ordre des lignes :
    #
    # haut ↔ bas
    image_miroir = np.flipud(image)

    return image_miroir


# Appliquer la fonction à la bande rouge.
array_miroir = set_mirror(array)

# Afficher le résultat.
plt.figure()

plt.imshow(array_miroir, cmap="gray")

plt.title("Image miroir")

plt.show()

# Les 4 bandes sont enregistrées dans le fichier dans cet ordre :
#
# Bande 1 = B4 = Rouge
# Bande 2 = B3 = Vert
# Bande 3 = B2 = Bleu
# Bande 4 = B8 = Proche infrarouge

# Charger chaque bande dans un tableau NumPy.
red = ds.GetRasterBand(1).ReadAsArray()
green = ds.GetRasterBand(2).ReadAsArray()
blue = ds.GetRasterBand(3).ReadAsArray()
infrared = ds.GetRasterBand(4).ReadAsArray()








