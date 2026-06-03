import sys
import logging

try:
    from PyQt5.QtWidgets import QApplication, QWidget, QLabel
    from PyQt5.QtCore import Qt, QTimer
    from PyQt5.QtGui import QMovie
    PYQT_AVAILABLE = True
except ImportError:
    PYQT_AVAILABLE = False

logger = logging.getLogger("HolographicPet")

if PYQT_AVAILABLE:
    class HolographicEntity(QWidget):
        """
        A transparent, frameless, always-on-top desktop widget that renders
        the physical visual representation (hologram/pet) of the AI OS.
        """
        def __init__(self, gif_path: str = None):
            super().__init__()
            self.gif_path = gif_path
            self.initUI()

        def initUI(self):
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
            self.setAttribute(Qt.WA_TranslucentBackground)

            self.label = QLabel(self)

            if self.gif_path:
                self.movie = QMovie(self.gif_path)
                self.label.setMovie(self.movie)
                self.movie.start()
            else:
                self.label.setText("🤖 [AI Entity]")
                self.label.setStyleSheet("color: cyan; font-size: 24px; font-weight: bold;")

            self.label.adjustSize()
            self.resize(self.label.width(), self.label.height())
            self.move(100, 100)
            self.show()

        def update_emotion(self, emotion: str):
            logger.info(f"Holographic entity changing emotion to: {emotion}")

        def walk_to(self, x: int, y: int):
            logger.info(f"Entity walking to: {x}, {y}")
            self.move(x, y)

    def launch_hologram(gif_path: str = None):
        app = QApplication(sys.argv)
        ex = HolographicEntity(gif_path)
        sys.exit(app.exec_())
else:
    def launch_hologram(gif_path: str = None):
        logger.warning("PyQt5 not installed. Holographic entity cannot run natively in this environment.")

if __name__ == '__main__':
    launch_hologram()
