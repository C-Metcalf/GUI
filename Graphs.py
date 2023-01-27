from pyqtgraph import PlotWidget
from PyQt6.QtCore import QTimer
import pyqtgraph
from random import randint
from PyQt6.QtWidgets import QMainWindow, QWidget
from datetime import datetime


class GraphWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.graphWidget = PlotWidget()
        self.start_graph = False
        self.spot = 0

        self.setCentralWidget(self.graphWidget)
        self.graphWidget.setTitle("Motor Data", color='b', size='30')

        self.x = list(range(100))
        self.x1 = list(range(100))
        self.y = [randint(0, 100) for _ in range(100)]
        self.y1 = [randint(0, 100) for _ in range(100)]

        pen = pyqtgraph.mkPen(color=(255, 0, 0))
        pen1 = pyqtgraph.mkPen(color=(0, 255, 0))

        #  draws data onto the graph from X-axis 0 - 100
        self.data_line = self.graphWidget.plot(self.x, self.y, pen=pen)
        self.data_line1 = self.graphWidget.plot(self.x1, self.y1, pen=pen1)

        self.graphWidget.setLabel('left', 'Volts(V)')
        self.graphWidget.setLabel('right', 'Amps(A)')
        self.graphWidget.setLabel('bottom', 'Milliseconds(50)')
        self.graphWidget.showGrid(x=True, y=True)

        self.timer = QTimer()
        self.timer.setInterval(500)  # this is milliseconds
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

        self.log_timer = QTimer()
        self.log_timer.setInterval(500)  # this is milliseconds
        self.log_timer.timeout.connect(self.log_file)
        self.log_timer.start()

    def update_plot_data(self):
        self.x = self.x[1:]
        self.x1 = self.x1[1:]

        self.x.append(self.x[-1] + 1)
        self.x1.append(self.x1[-1] + 1)

        self.y = self.y[1:]
        self.y1 = self.y1[1:]

        self.y.append(randint(0, 100))
        self.y1.append(randint(0, 100))

        self.data_line.setData(self.x, self.y)
        self.data_line1.setData(self.x1, self.y1)

    def log_file(self):
        file = open("MotorData.txt", 'a')
        if not self.start_graph:
            file.write('\n' + str(datetime.now()) + '\n')
            self.start_graph = True
        if self.spot != 99:
            while self.spot != 99:
                # file_input = ("X-axis(ms): " + str(self.x[self.spot]) + " Y-axis: " + str(self.y[self.spot]) + '\n')
                file_input = f"X-axis(ms): {self.x[self.spot]} Y-axis: {self.y[self.spot]} \n"
                self.spot = self.spot + 1
                file.write(file_input)


class GraphSettings(QMainWindow):
    def __init__(self):
        super().__init__()

        # select what params you want to see on the graph
        # Create two lists
        # One with the selected params that will be viewed on the graph
        # One with all possibilities to be shown on the graph
        # Have a limit of four variable per graph.
        # Allow the user to choose what gets put to the output log file
        # Have it be what the graph sees, all variables, or custome


# ToDo: Create a paramater class that would be whats used in the graph example: Volts, Amps


class Params(QMainWindow):
    def __init__(self):
        super().__init__()
        self.volts = 10
        # in this class it will have the properties for the params
        # if they want to see volts they will select volts in the GS and then this class will do the
        # calculations to get the right number to the graph


