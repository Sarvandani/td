# td
# ============================================================
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


# Séparation des colonnes
#
# colonne 0 = East
# colonne 1 = North
# colonne 2 = altitude

x1 = data1[:, 0]
y1 = data1[:, 1]
z1 = data1[:, 2]

x2 = data2[:, 0]
y2 = data2[:, 1]
z2 = data2[:, 2]


print("\nBanc 1 :")
print("Nombre de points :", len(x1))

print("\nBanc 2 :")
print("Nombre de points :", len(x2))


# ------------------------------------------------------------
# Lecture du MNT
# ------------------------------------------------------------

ds = gdal.Open("MNT_LiDAR_Ribaute_crop.tif")

if ds is None:
    raise FileNotFoundError("Impossible d'ouvrir le MNT.")


topo = ds.GetRasterBand(1).ReadAsArray()

gt = ds.GetGeoTransform()


ncols = ds.RasterXSize
nlines = ds.RasterYSize


# Limites du raster
xmin = gt[0]
xmax = gt[0] + ncols * gt[1]

ymax = gt[3]
ymin = gt[3] + nlines * gt[5]


# ------------------------------------------------------------
# Création rapide du hillshade
# ------------------------------------------------------------

filtered_topo = gaussian_filter(
    topo,
    sigma=2
)


res_x = gt[1]
res_y = gt[5]


dsm_dy, dsm_dx = np.gradient(
    filtered_topo,
    res_y,
    res_x
)


slope = np.arctan(
    np.sqrt(
        dsm_dx**2 +
        dsm_dy**2
    )
)


aspect = np.arctan2(
    dsm_dx,
    dsm_dy
)


aspect_geo = (
    np.rad2deg(aspect) + 360
) % 360


aspect_rad = np.deg2rad(
    aspect_geo
)


# Position du soleil
azimuth = 315
altitude = 45

azimuth_rad = np.deg2rad(azimuth)
altitude_rad = np.deg2rad(altitude)


hillshade = 255 * (
    np.cos(altitude_rad)
    * np.cos(slope)
    +
    np.sin(altitude_rad)
    * np.sin(slope)
    * np.cos(
        azimuth_rad - aspect_rad
    )
)


hillshade = np.clip(
    hillshade,
    0,
    255
)


# ------------------------------------------------------------
# Affichage des points sur le MNT
# ------------------------------------------------------------

fig, ax = plt.subplots(figsize=(10, 8))


ax.imshow(
    hillshade,
    cmap="gray",
    origin="upper",
    extent=[xmin, xmax, ymin, ymax]
)


# Banc 1
ax.scatter(
    x1,
    y1,
    c="red",
    s=30,
    label="Banc 1"
)


# Banc 2
ax.scatter(
    x2,
    y2,
    c="blue",
    s=30,
    label="Banc 2"
)


ax.set_xlabel("Easting (m)")
ax.set_ylabel("Northing (m)")
ax.set_title("Position des deux bancs")

ax.legend()

plt.show()


# ============================================================
# ETAPE 2 - AJUSTEMENT D'UN PLAN
# ============================================================


def fit_plane(x, y, z):
    """
    Ajuste le plan :

        z = a*x + b*y + c

    par la méthode des moindres carrés.
    """

    # Matrice A
    A = np.column_stack(
        (
            x,
            y,
            np.ones(len(x))
        )
    )

    # Résolution par moindres carrés
    coefficients, residuals, rank, s = np.linalg.lstsq(
        A,
        z,
        rcond=None
    )

    a = coefficients[0]
    b = coefficients[1]
    c = coefficients[2]

    return a, b, c


# Ajustement du banc 1
a1, b1, c1 = fit_plane(
    x1,
    y1,
    z1
)


# Ajustement du banc 2
a2, b2, c2 = fit_plane(
    x2,
    y2,
    z2
)


print("\n--------------------------------")
print("PLAN DU BANC 1")
print("--------------------------------")

print(
    "z =",
    a1,
    "* x +",
    b1,
    "* y +",
    c1
)


print("\n--------------------------------")
print("PLAN DU BANC 2")
print("--------------------------------")

print(
    "z =",
    a2,
    "* x +",
    b2,
    "* y +",
    c2
)


# ------------------------------------------------------------
# Calcul du strike et du pendage
# ------------------------------------------------------------


def orientation_plane(a, b):

    # Vecteur normal au plan :
    #
    # n = (a, b, -1)

    normal = np.array(
        [a, b, -1]
    )


    # Strike selon la formule donnée dans le TD
    strike = np.arctan2(
        b,
        a
    )

    strike_deg = (
        np.rad2deg(strike) + 360
    ) % 360


    # Pendage selon la formule donnée dans le TD
    dip = np.arccos(
        1 /
        np.sqrt(
            a**2 +
            b**2 +
            1
        )
    )


    dip_deg = np.rad2deg(dip)


    return normal, strike_deg, dip_deg


# Banc 1
normal1, strike1, dip1 = orientation_plane(
    a1,
    b1
)


# Banc 2
normal2, strike2, dip2 = orientation_plane(
    a2,
    b2
)


print("\n================================")
print("ORIENTATION DU BANC 1")
print("================================")

print("Vecteur normal :", normal1)
print("Strike / azimut :", strike1, "°")
print("Pendage :", dip1, "°")


print("\n================================")
print("ORIENTATION DU BANC 2")
print("================================")

print("Vecteur normal :", normal2)
print("Strike / azimut :", strike2, "°")
print("Pendage :", dip2, "°")


# ============================================================
# ETAPE 3 - VISUALISATION 3D
# ============================================================

fig = plt.figure(
    figsize=(12, 9)
)

ax = fig.add_subplot(
    111,
    projection="3d"
)


# ------------------------------------------------------------
# Points du banc 1
# ------------------------------------------------------------

ax.scatter(
    x1,
    y1,
    z1,
    c="red",
    s=30,
    label="Banc 1"
)


# ------------------------------------------------------------
# Points du banc 2
# ------------------------------------------------------------

ax.scatter(
    x2,
    y2,
    z2,
    c="blue",
    s=30,
    label="Banc 2"
)


# ------------------------------------------------------------
# Grille pour le plan du banc 1
# ------------------------------------------------------------

X1, Y1 = np.meshgrid(
    np.linspace(
        x1.min(),
        x1.max(),
        20
    ),
    np.linspace(
        y1.min(),
        y1.max(),
        20
    )
)


# Equation du plan
Z1 = (
    a1 * X1
    +
    b1 * Y1
    +
    c1
)


# Affichage du plan
ax.plot_surface(
    X1,
    Y1,
    Z1,
    alpha=0.4
)


# ------------------------------------------------------------
# Grille pour le plan du banc 2
# ------------------------------------------------------------

X2, Y2 = np.meshgrid(
    np.linspace(
        x2.min(),
        x2.max(),
        20
    ),
    np.linspace(
        y2.min(),
        y2.max(),
        20
    )
)


Z2 = (
    a2 * X2
    +
    b2 * Y2
    +
    c2
)


ax.plot_surface(
    X2,
    Y2,
    Z2,
    alpha=0.4
)


# ------------------------------------------------------------
# Configuration du graphique
# ------------------------------------------------------------

ax.set_xlabel(
    "Easting (m)"
)

ax.set_ylabel(
    "Northing (m)"
)

ax.set_zlabel(
    "Altitude (m)"
)

ax.set_title(
    "Plans ajustés aux deux bancs"
)

ax.legend()

plt.show()


# ============================================================
# ETAPE 4 - POUR ALLER PLUS LOIN
# ============================================================

# A partir de la carte géologique :
#
# 1. Identifier des points appartenant aux failles.
#
# 2. Extraire leurs coordonnées X, Y et Z.
#
# 3. Utiliser la même fonction fit_plane().
#
# 4. Calculer le strike et le pendage avec
#    orientation_plane().
#
# 5. Utiliser ces informations pour construire
#    une coupe structurale.


# Fermeture du MNT
ds = None
