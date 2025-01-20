from PyQt6.QtWidgets import QSplashScreen, QApplication
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer
import sys

def show_splash_screen():
    app = QApplication(sys.argv)
    pixmap = QPixmap("splash.png")
    splash = QSplashScreen(pixmap)
    splash.showMessage("Loading...", Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter, Qt.GlobalColor.white)
    splash.show()

    QTimer.singleShot(3000, splash.close)

    return app, splash
