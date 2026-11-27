"""TD — Construction d'un cône de scories : questions 1 et 2.
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
