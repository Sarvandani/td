"""TD — Construction d'un cône de scories : questions 1 et 2.

Exécution dans PyCharm : lancer ce fichier.
Cinq figures s'affichent, dont une animation de la croissance.
Aucun fichier n'est enregistré automatiquement.
"""

# ============================================================
# QUESTION 1 — PRÉSENTATION DU PROBLÈME
# ============================================================

# 1. Équations générales du mouvement :
#    x(t) = x0 + vx0*t + ax*t**2/2
#    y(t) = y0 + vy0*t + ay*t**2/2
#    Sous l'effet de la gravité : ax = 0 et ay = -g.

# 2. Conditions initiales :
#    Position initiale : (x0, y0)
#    Vitesse initiale : v0 ; angle d'éjection : theta.
#    vx0 = v0*cos(theta) et vy0 = v0*sin(theta)

# 3. Substitution des conditions initiales :
#    x(t) = x0 + v0*cos(theta)*t
#    y(t) = y0 + v0*sin(theta)*t - g*t**2/2

# 4. Élimination du temps t :
#    t = (x-x0)/(v0*cos(theta))
#    y(x) = y0 + (x-x0)*tan(theta)
#           - g*(x-x0)**2/(2*v0**2*cos(theta)**2)

# ============================================================
# QUESTION 2 — PROGRAMMATION INITIALE
# ============================================================
import random
import numpy as np
import matplotlib.pyplot as plt

# Étape 1 — Construire le maillage et initialiser la topographie (numpy).
xmax = 400.0
dx = 2.0
x = np.arange(0, xmax, dx)
h = np.zeros(len(x))
print(f"Étape 1 : {len(x)} points sur le maillage.")

# Étape 2 — Définir les paramètres initiaux.
dh = 0.8                  # Épaisseur ajoutée par éjecta (m).
v0 = 51.0                 # Vitesse moyenne choisie (m/s).
dv0 = 7.0                 # Dispersion illustrative (m/s).
theta_min = 75.0          # Angle minimal (degrés).
theta_max = 89.0          # Éviter exactement 90°.
g = 9.81                  # Gravité terrestre (m/s²).
n_iter = 10000            # Tester d'abord avec 10, puis augmenter.
n_plots = 10              # Nombre approximatif d'états pour l'animation.

# Étape 3 — Calculer la trajectoire d'un éjecta (numpy).
def trajectoire(x, angle0, vitesse0, h0, gravite=g):
    angle = np.deg2rad(angle0)
    return h0 + x * np.tan(angle) - gravite * x**2 / (2 * vitesse0**2 * np.cos(angle)**2)


# Étape 3 — Vérifier la trajectoire dans la figure 1 (matplotlib).
plt.figure(1, figsize=(9, 5))
y_test = trajectoire(x, 80, v0, 0, g)
y_test[y_test < 0] = np.nan       # Masquer la partie sous le sol.
plt.plot(x, y_test, label="Angle = 80°")
plt.axhline(0, color="black", linewidth=1)
plt.xlabel("Distance x (m)")
plt.ylabel("Hauteur y (m)")
plt.title("Figure 1 — Étape 3 : Trajectoire balistique")
plt.legend()
plt.grid(alpha=0.3)

# Étape 4 — Tirer une vitesse et un angle aléatoires (random).
def ejecta_aleatoire():
    vitesse = max(1.0, random.gauss(v0, dv0))
    angle = random.uniform(theta_min, theta_max)
    return vitesse, angle


# Étape 5 — # S1 — Déterminer le premier point d'impact.
# Trouver le premier point d'impact (numpy).
def point_impact(y, h):
    contacts = y[1:] <= h[1:]    # Ignorer x = 0 : point de départ.
    if not np.any(contacts):
        return None              # Aucun impact dans le maillage.
    return int(np.argmax(contacts) + 1)


# Étape 5 (répétée dans le PDF) —
# # S2 — Préparer la simulation.
etats = [h.copy()]               # Sol plat avant le premier éjecta.
intervalle = max(1, n_iter // n_plots)
random.seed(42)                  # Résultats identiques à chaque exécution.

# S3 — Construire le cône avec plusieurs éjectas.
for iteration in range(n_iter):

    # Choisir une vitesse et un angle.
    vitesse, angle = ejecta_aleatoire()

    # Calculer la trajectoire.
    y = trajectoire(x, angle, vitesse, 0, g)

    # Trouver le point d'impact.
    indice = point_impact(y, h)

    # Ajouter de la matière au sol.
    if indice is not None:
        h[indice] += dh

    # Garder le centre du cratère à zéro.
    h[0] = 0.0

    # Mémoriser  le sol pour le montrer dans l'étape 6.
    if (iteration + 1) % intervalle == 0 or iteration == n_iter - 1:
        etats.append(h.copy())

# S4 — Construire le profil complet par symétrie.
x_total = np.concatenate((-x[:0:-1], x))
h_total = np.concatenate((h[:0:-1], h))

# S5 — Afficher la topographie finale (figure 3).
# Étape 5 — Montrer le cône terminé dans la figure 3 (matplotlib).
plt.figure(3, figsize=(9, 5))
plt.fill_between(x_total, 0, h_total, color="red", alpha=0.3)
plt.plot(x_total, h_total, color="black")
plt.xlabel("Distance au conduit (m)")
plt.ylabel("Hauteur (m)")
plt.title("Figure 3 — Étape 5 : Topographie finale sans pente critique")
plt.grid(alpha=0.3)


# ============================================================
# ÉTAPE 6 — ANIMATION DE LA CROISSANCE DU CÔNE
# ============================================================

# S1 — Préparer la figure d'animation.
plt.ion()  # Activer le mode interactif.

fig_animation = plt.figure(2, figsize=(9, 5))
axe = fig_animation.gca()  # Récupérer les axes de la figure.

# Générateur aléatoire réservé aux trajectoires rouges.
rng_affichage = random.Random(123)


# S2 — Parcourir les topographies sauvegardées.
#Recall that etats contains the saved versions of the ground from Étape 5.
#numero is the snapshot number, and profil contains the ground heights in that snapshot.
for numero, profil in enumerate(etats):

    # Effacer le dessin précédent.
    axe.clear()

    # S3 - Dessiner la topographie du cône
    # The black line shows the surface of the volcano.
    # The shaded area underneath represents the accumulated volcanic material.
    # Reproduire la partie gauche par symétrie.
    #The first line creates the left side using symmetry, just like Étape 5.
    h_animation = np.concatenate((profil[:0:-1], profil))

    # Colorier le cône en rouge
    axe.fill_between(
        x_total, 0, h_animation,
        color="red", alpha=0.5
    )

    # Dessiner la surface du cône en noir.
    axe.plot(x_total, h_animation, color="black", linewidth=1.5)

    # S4 — Dessiner les trajectoires rouges
    # The light-red parabolic curves show illustrative paths of particles ejected from the crater.
    #S3 shows the actual topography calculated in Étape 5. S4 adds illustrative trajectories only; they do not change the cone.
    #For every animation frame, we draw five illustrative trajectories.
    for j in range(5):

        # Choisir une vitesse et un angle aléatoires.
        vitesse = max(1.0, rng_affichage.gauss(v0, dv0))
        angle = rng_affichage.uniform(theta_min, theta_max)

        # Calculer la trajectoire.
        y_rouge = trajectoire(x, angle, vitesse, 0, g)

        # Masquer la trajectoire sous le cône.
        y_rouge[y_rouge < profil] = np.nan

        # Afficher la trajectoire à droite et à gauche.
        axe.plot(x, y_rouge, color="red", alpha=0.25)
        axe.plot(-x, y_rouge, color="red", alpha=0.25)

    # S5 — Configurer et actualiser la figure.
    axe.set_xlim(-xmax, xmax)
    axe.set_ylim(0, max(100, h.max() * 1.1))
    axe.set_xlabel("Distance au conduit (m)")
    axe.set_ylabel("Hauteur (m)")
    axe.set_title(
        f"Figure 2 — Étape 6 : Croissance "
        f"({numero}/{len(etats) - 1})"
    )
    axe.grid(alpha=0.3)

    # Montrer la nouvelle image.
    fig_animation.canvas.draw_idle()
    plt.pause(0.05)


# S6 — Terminer l'animation.
plt.ioff()




# Afficher ensemble les cinq figures ; aucune sauvegarde automatique.
plt.show()
