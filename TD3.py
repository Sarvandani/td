# ============================================================
# TD MODELISATION - INFORMATIQUE
# PARTIE 2 : ANALYSE D IMAGES SENTINEL-2 AVEC PYQT5
# ACTIVITE 6  (contient 1 a 5)
# ============================================================
# Activite 1 : on utilise QApplication et QWidget, on cree la fenetre et on lance PyQt5.
# Activite 2 : on utilise QPushButton, QLabel, QLineEdit et QTextEdit, on cree les widgets.
# Activite 3 : on utilise QGridLayout et addWidget, on organise la fenetre.
# Activite 4 : on utilise clicked.connect et qApp.quit, on relie les boutons aux actions.
# Activite 5 : on utilise QFileDialog et GDAL, on charge un TIFF et on affiche ses informations.
# Activite 6 : on utilise NumPy, Matplotlib et FigureCanvas, on affiche une bande et son histogramme.
# ============================================================
# PyQt5.QtWidgets : les elements visibles de l interface
#   QApplication    : demarre l application PyQt5 (obligatoire)
#   QWidget         : fenetre principale (GuiTiffViewer)
#   QPushButton     : bouton cliquable
#   QLabel          : texte affiche devant un champ
#   QLineEdit       : champ pour saisir ou afficher du texte
#   QTextEdit       : zone pour afficher les informations du TIFF
#   QGridLayout     : place les widgets en lignes et colonnes
#   qApp            : application en cours (pour Quitter)
#   QFileDialog     : boite de dialogue pour choisir un fichier TIFF
#   QMessageBox     : affiche un message en cas d erreur
# osgeo.gdal       : ouvre un TIFF et lit les metadonnees des bandes
# numpy            : filtre les pixels et les valeurs invalides
# matplotlib.pyplot : cree l image et l histogramme
# FigureCanvas     : affiche la figure Matplotlib dans PyQt5
# ============================================================

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit, QTextEdit
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import qApp
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


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
        self.b_charger_ = self.create_button("Charger un fichier TIFF", self.charger_fichier)
        self.b_afficher_ = self.create_button("Afficher Bande", self.afficher_bande)
        self.b_quitter_ = self.create_button("Quitter", qApp.quit)
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
        self.ds = None

        # ----------------------------------------------------
        # ACTIVITE 6
        # Integration : plt.figure cree la figure
        # FigureCanvas integre Matplotlib dans la fenetre PyQt5
        # ----------------------------------------------------
        self.figure = plt.figure(figsize=(8, 4))
        self.canvas = FigureCanvas(self.figure)

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
        monLayout.addWidget(self.canvas, 5, 0, 1, 2)
        monLayout.addWidget(self.b_quitter_, 6, 0, 1, 2)
        self.setLayout(monLayout)

    # ----------------------------------------------------
    # ACTIVITE 4
    # Puces 1 a 3 : QPushButton et clicked.connect relient les actions
    # qApp.quit ferme la fenetre
    # ----------------------------------------------------
    def create_button(self, libelle, method):
        button = QPushButton(libelle, self)
        button.clicked.connect(method)
        return button

    # ----------------------------------------------------
    # ACTIVITE 5
    # Puce 1 : QFileDialog.getOpenFileName selectionne un fichier
    # Puce 2 : QLineEdit.setText affiche le chemin
    # Puce 3 : gdal.Open lit le TIFF et ses informations
    # ----------------------------------------------------
    def charger_fichier(self):
        filename, filetype = QFileDialog.getOpenFileName(
            self, "Choisir un fichier TIFF", "", "Images TIFF (*.tif *.tiff)"
        )
        if not filename:
            return
        # Puce 3 : GDAL ouvre le fichier TIFF
        ds = gdal.Open(filename)
        if ds is None:
            QMessageBox.warning(self, "Erreur", "Impossible d'ouvrir ce fichier TIFF.")
            return

        self.ds = ds
        self.edit_filename_.setText(filename)
        # Puce 3 : dimensions, bandes, projection et resolution
        geo = ds.GetGeoTransform()
        info = f"Taille: {ds.RasterXSize} x {ds.RasterYSize}\n"
        info += f"Bandes: {ds.RasterCount}\n"
        info += f"Projection: {ds.GetProjection()}\n"
        info += f"Resolution pixel: {geo[1]} x {abs(geo[5])}"
        self.info_label.setText(info)

    # ----------------------------------------------------
    # ACTIVITE 6
    # Puce 1 : QLineEdit.text et int lisent le numero de bande
    # Puce 2 : GDAL GetRasterBand et ReadAsArray lisent les pixels
    # Puce 3 : Matplotlib affiche l image et l histogramme
    # Puce 4 : FigureCanvas.draw actualise l affichage
    # ----------------------------------------------------
    def afficher_bande(self):
        if self.ds is None:
            QMessageBox.warning(self, "Erreur", "Charger d'abord un fichier TIFF.")
            return
        try:
            band_num = int(self.edit_band.text())
        except ValueError:
            QMessageBox.warning(self, "Erreur", "Saisir un numero de bande entier.")
            return
        if not 1 <= band_num <= self.ds.RasterCount:
            QMessageBox.warning(self, "Erreur", f"Choisir une bande entre 1 et {self.ds.RasterCount}.")
            return

        # Puce 2 : GDAL lit la bande choisie dans un tableau NumPy
        band = self.ds.GetRasterBand(band_num)
        image = band.ReadAsArray()
        nodata = band.GetNoDataValue()
        valeurs = image[np.isfinite(image)]
        if nodata is not None:
            valeurs = valeurs[valeurs != nodata]

        # Puce 3 : subplots Matplotlib pour image et histogramme
        self.figure.clear()
        ax1 = self.figure.add_subplot(1, 2, 1)
        ax1.imshow(image, cmap="gray")
        ax1.set_title(f"Bande {band_num}")

        ax2 = self.figure.add_subplot(1, 2, 2)
        ax2.hist(valeurs.ravel(), bins=100, color="gray")
        ax2.set_title("Histogramme")
        self.figure.tight_layout()
        # Puce 4 : actualiser la figure dans PyQt5
        self.canvas.draw()


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
