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

# Résolution spatiale
# -----------------------------------------------------------------------------

geo = ds.GetGeoTransform()

resolution_x = geo[1]
resolution_y = abs(geo[5])  
print("\nRésolution spatiale :")
print("Taille d'un pixel en X :", resolution_x, "m")
print("Taille d'un pixel en Y :", resolution_y, "m")

# La bande 1 du fichier correspond à Sentinel-2 B4 = Rouge.
band1 = ds.GetRasterBand(1)

# Le type de données indique comment les valeurs des pixels sont stockées.
# Par exemple :
# Byte   → 8 bits
print("\nType de données :")
print(gdal.GetDataTypeName(band1.DataType))

# ReadAsArray() transforme la bande raster en tableau NumPy 2D.
array = band1.ReadAsArray()

# array.shape donne :
# (nombre de lignes, nombre de colonnes)
print("\nDimensions du tableau :", array.shape)


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

plt.figure()

plt.imshow(array, cmap="gray", vmin=0, vmax=255)

plt.title("Bande rouge B4")
plt.colorbar()

plt.show()

plt.figure()

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

# bins=100 regroupe les valeurs dans 100 intervalles.
plt.hist(array.ravel(), bins=100)

plt.xlabel("Valeur du pixel")
plt.ylabel("Nombre de pixels")
plt.title("Histogramme de la bande rouge")

plt.show()

 -----------------------------------------------------------------------------
# etap 2:  -------------------------------------------------------------------

def stretch(image):

    valeur_min, valeur_max = np.percentile(image, (2, 98))

    # Normaliser les valeurs :
    #
    # valeur_min → 0
    # valeur_max → 1
 
    image_stretch = (
        (image - valeur_min) /
        (valeur_max - valeur_min)
    )

    # Certaines valeurs peuvent être < 0 ou > 1.
    #
    # np.clip() les force à rester entre 0 et 1 :
    # valeur < 0 → 0
    # valeur > 1 → 1
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

# =============================================================================
# ÉTAPE 3 – BINARISATION ET SEUILLAGE
# =============================================================================
# -----------------------------------------------------------------------------
# Question : Choisir un seuil 
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

# -----------------------------------------------------------------------------
# Question : Créer une image binaire :
# -----------------------------------------------------------------------------

# Au départ, tous les pixels sont donc considérés comme de l'eau.
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

# =============================================================================
# ÉTAPE 4 – IMAGE MIROIR
# =============================================================================
# -----------------------------------------------------------------------------
# Question : Écrire une fonction set_mirror qui retourne
# une image miroir avec la commande np.flipud().
# -----------------------------------------------------------------------------

def set_mirror(image):

    # np.flipud() signifie "flip up-down"
    image_miroir = np.flipud(image)
    return image_miroir

# Appliquer la fonction à la bande rouge.
array_miroir = set_mirror(array)


# Afficher le résultat.
plt.figure()

plt.imshow(array_miroir, cmap="gray")

plt.title("Image miroir")

plt.show()

# =============================================================================
# ÉTAPE 5 – COMPOSITION COLORÉE
# =============================================================================

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

# Améliorer le contraste de chaque bande avec la fonction stretch().
red_stretch = stretch(red)
green_stretch = stretch(green)
blue_stretch = stretch(blue)
infrared_stretch = stretch(infrared)

image_rgb = np.dstack((
    red_stretch,
    green_stretch,
    blue_stretch
))

# Afficher la composition en couleurs naturelles.
plt.figure()

plt.imshow(image_rgb)

plt.title("Composition en couleurs naturelles (B4, B3, B2)")

plt.show()

image_infrarouge = np.dstack((
    infrared_stretch,
    red_stretch,
    green_stretch
))

# Afficher la composition infrarouge.
plt.figure()

plt.imshow(image_infrarouge)

plt.title("Composition infrarouge couleur (B8, B4, B3)")

plt.show()






