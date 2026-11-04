# ============================================================
# TD MODELISATION - INFORMATIQUE
# PARTIE 2 : ANALYSE D IMAGES SENTINEL-2 AVEC PYQT5
# ACTIVITE 1
# ============================================================
# Activite 1 : on utilise QApplication et QWidget, on cree la fenetre et on lance PyQt5.
# ============================================================
# PyQt5.QtWidgets : les elements visibles de l interface
#   QApplication    : demarre l application PyQt5 (obligatoire)
#   QWidget         : fenetre principale (GuiTiffViewer)
# ============================================================

from PyQt5.QtWidgets import QApplication, QWidget


class GuiTiffViewer(QWidget):
    def __init__(self):
        # ----------------------------------------------------
        # ACTIVITE 1
        # on utilise QWidget : on cree la fenetre et son titre
        # ----------------------------------------------------
        super().__init__()
        self.setWindowTitle("Tiff Viewer")


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

