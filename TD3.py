# ============================================================
# TD MODELISATION - INFORMATIQUE
# PARTIE 1 : INTERFACE GRAPHIQUE AVEC PYQT5
# ACTIVITE 7  (contient 1, 2, 3, 4, 5, 6)
# ============================================================
# Activite 1 : on utilise QWidget, on cree la fenetre et on lui donne un titre.
# Activite 2 : on utilise QPushButton et QFont, on cree les boutons.
# Activite 3 : on utilise QGridLayout, on place les widgets dans une grille.
# Activite 4 : on utilise create_button et clicked.connect, on relie le clic a une action.
# Activite 5 : on utilise QLabel et QLineEdit, on affiche un titre et une zone pour ecrire.
# Activite 6 : on utilise QFileDialog.getOpenFileName et setText, on choisit un fichier.
# Activite 7 : on utilise QGraphicsScene et QGraphicsView, on cree la zone de dessin.
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
        # ACTIVITE 4
        # on utilise create_button : on cree les 3 boutons ET on connecte le clic
        # (a l'activite 2 c'etait QPushButton tout seul)
        # ----------------------------------------------------
        self.b_charger_fichier_ = self.create_button("Charger un fichier", self.charger_fichier)
        self.b_tracer_donnees_ = self.create_button("Tracer les donnees", self.tracer_donnees)
        self.b_quitter_ = self.create_button("Quitter", qApp.quit)
        self.b_quitter_.setFont(QFont("Comic Sans MS", 16))

        # ----------------------------------------------------
        # ACTIVITE 5
        # on utilise QLabel : titre (on ne tape pas)
        # on utilise QLineEdit : zone pour ecrire
        # ----------------------------------------------------
        self.label_filename_ = QLabel("Nom du fichier de donnees", self)
        self.label_filename_.setAlignment(Qt.AlignCenter)
        self.edit_filename_ = QLineEdit(self)

        self.label_coord_ = QLabel("Coordonnees x1 y1 x2 y2", self)
        self.label_coord_.setAlignment(Qt.AlignCenter)
        self.edit_coord_ = QLineEdit(self)
        self.edit_coord_.setMaximumWidth(90)
        self.edit_coord_.setPlaceholderText("100 200 300 400")

        self.b_effacer_ = self.create_button("Effacer", self.reset)

        # ----------------------------------------------------
        # ACTIVITE 7
        # on utilise QGraphicsScene : ou on ajoute les traits
        # on utilise QGraphicsView : le cadre sous Effacer (vide au debut)
        # English:
        #   QGraphicsScene = the paper (we draw lines ON it with addLine)
        #   QGraphicsView  = the frame you SEE under Effacer
        #   It starts empty. After Tracer, the line appears in this frame.
        # ----------------------------------------------------
        wid, hgt = 600, 400
        self.scene_ = QGraphicsScene(0, 0, wid, hgt, self)
        self.scene_.addRect(0, 0, wid, hgt)
        self.view_ = QGraphicsView(self.scene_, self)
        self.view_.setMinimumSize(wid + 100, hgt + 100)

        # ----------------------------------------------------
        # ACTIVITE 3
        # on utilise QGridLayout : on place tous les widgets
        # ----------------------------------------------------
        monLayout = QGridLayout()
        monLayout.addWidget(self.b_charger_fichier_, 0, 0, 1, 2)
        monLayout.addWidget(self.label_filename_, 1, 0)
        monLayout.addWidget(self.edit_filename_, 1, 1)
        monLayout.addWidget(self.label_coord_, 2, 0)
        monLayout.addWidget(self.edit_coord_, 2, 1)
        monLayout.addWidget(self.b_tracer_donnees_, 3, 0, 1, 2)
        monLayout.addWidget(self.b_effacer_, 4, 0, 1, 2)
        monLayout.addWidget(self.view_, 5, 0, 1, 2)
        monLayout.addWidget(self.b_quitter_, 6, 0, 1, 2)
        self.setLayout(monLayout)

    # ----------------------------------------------------
    # ACTIVITE 4
    # on utilise clicked.connect : un clic lance une methode
    # ----------------------------------------------------
    def create_button(self, libelle, method):
        button = QPushButton(libelle, self)
        button.clicked.connect(method)
        return button

    # ----------------------------------------------------
    # ACTIVITE 6
    # on utilise QFileDialog.getOpenFileName : fenetre pour choisir un fichier
    # setText(filename) : montre le chemin DANS LA FENETRE (le champ blanc)
    # print(...)         : montre le chemin DANS LE TERMINAL (console)
    # English:
    #   setText = write in the INTERFACE box (Nom du fichier de donnees)
    #   print   = write in the TERMINAL (not in the window)
    # ----------------------------------------------------
    def charger_fichier(self):
        filename, filetype = QFileDialog.getOpenFileName(
            self, "Choisir un fichier", "", "Tous les fichiers (*)"
        )
        if filename:
            self.edit_filename_.setText(filename)
            print("Nom du fichier de donnees :", filename)

    # ----------------------------------------------------
    # ACTIVITE 7
    # on utilise addLine : on lit x1 y1 x2 y2 et on dessine le segment
    # Exemple : 100 200 300 400
    # ----------------------------------------------------
    def tracer_donnees(self):
        valeurs = self.edit_coord_.text().split()
        if len(valeurs) != 4:
            print("Saisir 4 nombres : x1 y1 x2 y2  (ex: 100 200 300 400)")
            return
        x1, y1, x2, y2 = [float(v) for v in valeurs]
        self.scene_.addLine(x1, y1, x2, y2)

    # on utilise clear : on efface le dessin (bouton Effacer)
    def reset(self):
        self.scene_.clear()
        self.scene_.addRect(self.scene_.sceneRect())


def main():
    # ACTIVITE 1
    # on utilise QApplication, show, exec_ : on lance PyQt et on affiche
    app = QApplication([])
    gui = GUI_Main()
    gui.show()
    r = app.exec_()


if __name__ == "__main__":
    main()
