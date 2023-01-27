from PyQt6.QtWidgets import (
    QWidget,
    QApplication,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
    QLabel,
    QMainWindow,
    QStatusBar,
    QInputDialog,
    QMessageBox,
    QToolBar)


class PresetWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(500, 500)
        self.setWindowTitle("Motor Presets")

        layout = QVBoxLayout()
        self.setLayout(layout)

        auto_home_btn = QPushButton("Auto Home", self)
        auto_home_btn.clicked.connect(self.auto_home)
        layout.addWidget(auto_home_btn)

    def auto_home(self):
        print("motors now homing")