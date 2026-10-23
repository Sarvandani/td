# ============================================================
# TD MODELISATION - INFORMATIQUE
# PARTIE 1 : INTERFACE GRAPHIQUE AVEC PYQT5
# ACTIVITE 1
# ============================================================
# Activite 1 : on utilise QWidget, on cree la fenetre et on lui donne un titre.
#              on utilise QApplication, show, exec_, on lance et on affiche.
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


def main():
    # ACTIVITE 1
    # on utilise QApplication, show, exec_ : on lance PyQt et on affiche
    app = QApplication([])
    gui = GUI_Main()
    gui.show()
    r = app.exec_()


if __name__ == "__main__":
    main()
