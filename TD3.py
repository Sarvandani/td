# ============================================================
# TD MODELISATION - INFORMATIQUE
# PARTIE 1 : INTERFACE GRAPHIQUE AVEC PYQT5
# ACTIVITE 3  (contient 1 et 2)
# ============================================================
# Activite 1 : on utilise QWidget, on cree la fenetre et on lui donne un titre.
# Activite 2 : on utilise QPushButton et QFont, on cree les 3 boutons.
# Activite 3 : on utilise QGridLayout, on place les widgets dans une grille.
# ============================================================
# PyQt5.QtWidgets : les elements visibles de l'interface
#   QApplication    : lance le programme PyQt (obligatoire)
#   QWidget         : fenetre principale (GUI_Main)
#   QPushButton     : bouton cliquable
#   QLabel          : texte affiche (titre d'un champ)
#   QLineEdit       : zone pour ecrire du texte
#   QGridLayout     : place les widgets en lignes / colonnes
#   QFileDialog     : fenetre pour choisir un fichier
#   QGraphicsScene  : zone ou on dessine (les segments)
#   QGraphicsView   : affiche la scene a l'ecran
#   qApp            : l'application en cours (pour Quitter)
# PyQt5.QtGui.QFont : changer la police d'un widget
# PyQt5.QtCore.Qt   : alignement du texte (AlignCenter)
# ============================================================

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLabel,
    QLineEdit,
    QGridLayout,
    QFileDialog,
    QGraphicsScene,
    QGraphicsView,
    qApp
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class GUI_Main(QWidget):
    def __init__(self):

        # ----------------------------------------------------
        # ACTIVITE 1
        # on utilise QWidget : on cree la fenetre et on lui donne un titre
        # ----------------------------------------------------
        QWidget.__init__(self)
        self.setWindowTitle("Ma premiere interface")

        # ----------------------------------------------------
        # ACTIVITE 2
        # on utilise QPushButton : on cree les 3 boutons
        # on utilise QFont : police de Quitter (Comic Sans MS 16)
        # ----------------------------------------------------
        self.b_charger_fichier_ = QPushButton("Charger un fichier", self)
        self.b_tracer_donnees_ = QPushButton("Tracer les donnees", self)
        self.b_quitter_ = QPushButton("Quitter", self)
        self.b_quitter_.setFont(QFont("Comic Sans MS", 16))

        # ----------------------------------------------------
        # ACTIVITE 3
        # on utilise QGridLayout : on place les boutons (sinon ils se recouvrent)
        # PDF : charger ligne 0, tracer ligne 3, quitter ligne 5
        # ----------------------------------------------------
        monLayout = QGridLayout()
        monLayout.addWidget(self.b_charger_fichier_, 0, 0, 1, 2)
        monLayout.addWidget(self.b_tracer_donnees_, 3, 0, 1, 2)
        monLayout.addWidget(self.b_quitter_, 5, 0, 1, 2)
        self.setLayout(monLayout)


def main():
    # ACTIVITE 1
    # on utilise QApplication, show, exec_ : on lance PyQt et on affiche
    app = QApplication([])
    gui = GUI_Main()
    gui.show()
    r = app.exec_()


if __name__ == "__main__":
    main()
