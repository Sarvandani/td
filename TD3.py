# ============================================================
# TD MODELISATION - INFORMATIQUE
# PARTIE 2 : ANALYSE D IMAGES SENTINEL-2 AVEC PYQT5
# ACTIVITE 3  (contient 1 a 2)
# ============================================================
# Activite 1 : on utilise QApplication et QWidget, on cree la fenetre et on lance PyQt5.
# Activite 2 : on utilise QPushButton, QLabel, QLineEdit et QTextEdit, on cree les widgets.
# Activite 3 : on utilise QGridLayout et addWidget, on organise la fenetre.
# ============================================================
# PyQt5.QtWidgets : les elements visibles de l interface
#   QApplication    : demarre l application PyQt5 (obligatoire)
#   QWidget         : fenetre principale (GuiTiffViewer)
#   QPushButton     : bouton cliquable
#   QLabel          : texte affiche devant un champ
#   QLineEdit       : champ pour saisir ou afficher du texte
#   QTextEdit       : zone pour afficher les informations du TIFF
#   QGridLayout     : place les widgets en lignes et colonnes
# ============================================================

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit, QTextEdit
from PyQt5.QtWidgets import QGridLayout


class GuiTiffViewer(QWidget):
    def __init__(self):
        # ----------------------------------------------------
        # ACTIVITE 1
        # on utilise QWidget : on cree la fenetre et son titre
        # ----------------------------------------------------
        super().__init__()
        self.setWindowTitle("Tiff Viewer")

        # ----------------------------------------------------
        # ACTIVITE 2
        # Puces 1, 4 et 6 : QPushButton pour les boutons
        # Puces 2 et 3 : QLabel et QLineEdit pour fichier et bande
        # Puce 5 : QTextEdit pour les informations du TIFF
        # ----------------------------------------------------
        self.b_charger_ = QPushButton("Charger un fichier TIFF", self)
        self.b_afficher_ = QPushButton("Afficher Bande", self)
        self.b_quitter_ = QPushButton("Quitter", self)
        # Puce 2 : QLabel + QLineEdit pour le chemin du fichier
        self.label_filename_ = QLabel("Nom du fichier :", self)
        self.edit_filename_ = QLineEdit(self)
        self.edit_filename_.setReadOnly(True)
        # Puce 3 : QLineEdit pour choisir le numero de bande
        self.label_band_ = QLabel("Choisir une bande :", self)
        self.edit_band = QLineEdit("1", self)
        self.edit_band.setMaximumWidth(70)
        # Puce 5 : QTextEdit pour afficher les informations
        self.info_label = QTextEdit(self)
        self.info_label.setReadOnly(True)

        # ----------------------------------------------------
        # ACTIVITE 3
        # Puces 1 et 2 : QGridLayout et addWidget placent les widgets
        # Puce 3 : une ligne est reservee aux graphiques (activite 6)
        # ----------------------------------------------------
        monLayout = QGridLayout()
        monLayout.addWidget(self.b_charger_, 0, 0, 1, 2)
        monLayout.addWidget(self.label_filename_, 1, 0)
        monLayout.addWidget(self.edit_filename_, 1, 1)
        monLayout.addWidget(self.label_band_, 2, 0)
        monLayout.addWidget(self.edit_band, 2, 1)
        monLayout.addWidget(self.b_afficher_, 3, 0, 1, 2)
        monLayout.addWidget(self.info_label, 4, 0, 1, 2)
        monLayout.addWidget(self.b_quitter_, 5, 0, 1, 2)
        self.setLayout(monLayout)


def main():
    # ----------------------------------------------------
    # ACTIVITE 1
    # QApplication lance PyQt5, show affiche la fenetre, exec_ demarre
    # ----------------------------------------------------
    app = QApplication([])
    gui = GuiTiffViewer()
    gui.show()
    app.exec_()


if __name__ == "__main__":
    main()
