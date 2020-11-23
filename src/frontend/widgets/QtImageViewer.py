from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtWidgets import QLabel


class QImageviewer(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.imageAnim = QPropertyAnimation(self, b"geometry")
        # super(QImageviewer, parent)

    def show(self, animation=False):
        super().show()
        if animation:
            self.imageAnim.setDuration(350)
            g = self.geometry()
            g.setHeight(0)
            self.imageAnim.setStartValue(g)
            self.imageAnim.setEndValue(self.geometry())
            self.imageAnim.start()
