import pyqtgraph as pg
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication , QMainWindow , QVBoxLayout , QWidget, QPushButton
import sys
import pandas as pd

class MainWindow(QMainWindow):
    def __init__(self ,x , y):
        super().__init__()
        self.custom_central_widget = QWidget()
        self.custom_layout = QVBoxLayout()
        self.custom_central_widget.setLayout(self.custom_layout)
        self.setCentralWidget(self.custom_central_widget)
        self.button = QPushButton("Pause")
        self.pause_state = False
        self.button.clicked.connect(self.toogle_graph)
        self.x_axis = x
        self.y_axis = y
        self.current_index = 0
        self.graph_widget = pg.PlotWidget()
        self.custom_layout.addWidget(self.graph_widget)
        self.custom_layout.addWidget(self.button)
        self.graph = self.graph_widget.plot(self.x_axis , self.y_axis)
        self.graph_widget.setXRange(0, 10)
        self.plotGraph()
        
    def plotGraph(self):
        # pg.PlotDataItem()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_plot_real_time)
        self.timer.start(10)        
    def update_plot_real_time(self):
        if self.current_index < len(self.x_axis):
            # current_x_chunck = self.x_axis[:self.current_index]
            # current_y_chunck = self.y_axis[:self.current_index]
            current_view_range = self.graph_widget.viewRange()
            print(current_view_range)
            self.graph_widget.setXRange(max(0, self.x_axis[self.current_index] - 1000), self.x_axis[self.current_index])
            # self.graph.setData(current_x_chunck, current_y_chunck)
            self.current_index += 1000
        else:
            self.timer.stop()
    def toogle_graph(self):
        if self.timer.isActive():
            self.timer.stop()
            self.button.setText("Resume")
        else:
            self.timer.start(1000)
            self.button.setText("Pause")

def main():
    data = pd.read_csv("100.csv")
    x_axis= data["sample #"]
    y_axis = data["MLII"]
    app = QApplication(sys.argv)
    window = MainWindow(x_axis , y_axis)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()