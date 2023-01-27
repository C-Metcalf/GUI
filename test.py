import pyqtgraph
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
from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtGui import QIcon, QAction, QFont
from enum import Enum, auto
import sys
from WidgetGraph import GraphWindow
from PresetFunctions import PresetWindow
# import serial


"""
ser = serial.Serial(
  port='/dev/ttyS0', # Change this according to connection methods, e.g. /dev/ttyUSB0
  baudrate = 115200,
  parity=serial.PARITY_NONE,
  stopbits=serial.STOPBITS_ONE,
  bytesize=serial.EIGHTBITS,
  timeout=1
)
"""

font = QFont('Arial', 30)


class Commands(Enum):
    FORWARD = 1
    BACKWARD = 2
    DUTY_CYCLE = 3
    STOP = auto()  # Always have this be the last value


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(500, 350)
        self.setCentralWidget(Window())
        self.t = SubWindow()
        self.p = PresetWindow()

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&File')
        edit_menu = menu_bar.addMenu('&Edit')
        help_menu = menu_bar.addMenu('&Help')

        file_menu.addAction('New', self.t.show)  # Get the menu to open a new window
        file_menu.addAction('Open', lambda: print('Open'))
        file_menu.addAction('Presets', self.p.show)
        file_menu.addAction('Exit', self.close)  # Stop and Close the program

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage('NAI MC v1.0')


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Motor Control")

        layout = QVBoxLayout()
        layout1 = QHBoxLayout()
        layout2 = QGridLayout()
        self.setLayout(layout)
        layout.addLayout(layout2)

        self.graph = GraphWindow()
        layout2.addWidget(self.graph.graphWidget, 1, 1)

        self.f_limit = QLabel('Front limit switch not hit')
        self.f_limit.setFont(font)
        self.f_limit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.f_limit.adjustSize()
        layout2.addWidget(self.f_limit, 0, 0)

        self.label = QLabel("Motors Are Not Moving")
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.adjustSize()
        # To change the layout change the order in which you add the widgets to the layout
        layout2.addWidget(self.label, 0, 1)

        self.duty_Cycle = QLabel('Duty Cycle: 0')
        self.duty_Cycle.setFont(font)
        self.duty_Cycle.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.duty_Cycle.adjustSize()
        layout2.addWidget(self.duty_Cycle, 1, 1)

        self.r_limit = QLabel('Rear limit switch not hit')
        self.r_limit.setFont(font)
        self.r_limit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.r_limit.adjustSize()
        layout2.addWidget(self.r_limit, 0, 2)

        forward_btn = QPushButton("Move Motors Forwards", self)
        forward_btn.clicked.connect(self.moveForward)
        layout.addWidget(forward_btn)

        backward_btn = QPushButton("Move Motors Backwards", self)
        backward_btn.clicked.connect(self.moveBackward)
        layout.addWidget(backward_btn)

        duty_cycle_btn = QPushButton("Change Duty Cycle", self)
        duty_cycle_btn.clicked.connect(self.dutyCycle)
        layout.addWidget(duty_cycle_btn)

        stop_btn = QPushButton("Stop the Motors", self)
        stop_btn.clicked.connect(self.stop)
        layout.addWidget(stop_btn)

    def moveForward(self):
        # tell the Pico to spin the Motor CW
        # ser.write(Commands.FORWARD.encode('utf-8'))
        self.label.setText("Motors Moving Forward")

    def moveBackward(self):
        # Tell the Pico to spin the Motor CCW
        # ser.write(Commands.BACKWARD.encode('utf-8'))
        self.label.setText("Motors Moving Backward")

    def dutyCycle(self):
        # Stop the motors then Change the duty cycle the motors run at
        self.stop()
        duty_cycle, ok = QInputDialog.getInt(self, "Duty Cycle", "New Duty Cycle:")
        if ok and duty_cycle:
            if duty_cycle > 95:
                QMessageBox.warning(
                    self,
                    'Warning',
                    'The duty cycle can not be set higher than 95 and therefor will be clamped to 95'
                )
                duty_cycle = 95
            elif duty_cycle < 10:
                QMessageBox.warning(
                    self,
                    'Warning',
                    'The duty cycle can not be set lower than 10 and therefor will be clamped to 10'
                )
                duty_cycle = 10
            self.duty_Cycle.setText('Duty Cycle: ' + str(duty_cycle))
            print(duty_cycle)
            # ser.write(Commands.DUTY_CYCLE + (the number the user inputs).encode('utf-8'))

    def stop(self):
        # Tell the Pico to stop the motors
        # ser.write(Commands.STOP.encode('utf-8'))
        self.label.setText("Motors Are Now Stopped")


class SubWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(200, 200)
        self.setWindowTitle('Testing testing')


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
