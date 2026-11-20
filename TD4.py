
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

    # --------------------------------------------------------
    # Lecture de l'ombrage du MNT
    # --------------------------------------------------------
    # L'ombrage a déjà été calculé et sauvegardé dans
    # hillshade.tif lors de la Partie 1 (Étape 5).
    #
    # On réutilise ce fichier
    # Ouvrir le raster d'ombrage avec GDAL.
    ds = gdal.Open(str(dossier / "hillshade.tif"))

    if ds is None:
        raise FileNotFoundError("hillshade.tif introuvable")

    # Lire la bande unique du raster.
    bande = ds.GetRasterBand(1)
    ombrage = bande.ReadAsArray().astype(float)

    # Remplacer les éventuelles valeurs NoData par NaN.
    nodata = bande.GetNoDataValue()

    if nodata is not None:
        ombrage[ombrage == nodata] = np.nan

    # Géoréférencement et limites du MNT ombré
    # --------------------------------------------------------
    # Un raster est une image composée de pixels organisés
    # en lignes et en colonnes. Chaque pixel de notre ombrage
    # contient une valeur de luminosité du relief.
    #
    # Le géoréférencement permet de connaître la position
    # réelle des pixels sur une carte.

    # Récupérer les informations de géoréférencement :
    # gt[0] : coordonnée X du coin supérieur gauche.
    # gt[1] : largeur d'un pixel (en mètres).
    # gt[3] : coordonnée Y du coin supérieur gauche.
    # gt[5] : hauteur d'un pixel (généralement négative).
    gt = ds.GetGeoTransform()

    # Nombre de lignes et de colonnes de l'image.
    lignes, colonnes = ombrage.shape

    limites = [
        gt[0],  # xmin : limite gauche (ouest) du raster
        gt[0] + colonnes * gt[1],  # xmax : limite droite (est) du raster
        gt[3] + lignes * gt[5],  # ymin : limite inférieure (sud) du raster
        gt[3]  # ymax : limite supérieure (nord) du raster
    ]

    # Fermer le fichier GDAL après lecture.
    ds = None

    # --------------------------------------------------------
    # FIGURE 1 – Position des bancs sur le MNT ombré
    # --------------------------------------------------------
    # plt.subplots() : créer une figure et ses axes.
    # imshow() : afficher le raster en arrière-plan.
    # origin="upper" : premier pixel en haut à gauche.
    # extent : positionner le raster en coordonnées spatiales.
    # scatter() : afficher les points de mesure.

    fig1, ax1 = plt.subplots(figsize=(10, 7))

    # Afficher le MNT ombré en niveaux de gris.
    ax1.imshow(
        ombrage,
        cmap="gray",
        origin="upper",
        extent=limites
    )

    # Afficher les points du banc 1 en rouge.
    ax1.scatter(
        x1, y1,
        color="red",
        s=35,
        label="Banc 1"
    )

    # Afficher les points du banc 2 en bleu.
    ax1.scatter(
        x2, y2,
        color="blue",
        s=35,
        label="Banc 2"
    )

    # Configurer les axes et la légende.
    ax1.set_title(
        "Étape 1 – Position des deux bancs sur le MNT ombré"
    )
    ax1.set_xlabel("Est (m)")
    ax1.set_ylabel("Nord (m)")
    ax1.set_aspect("equal")
    ax1.legend()

    fig1.tight_layout()

 

    plt.show()


if __name__ == "__main__":
    main()
