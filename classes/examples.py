import sys
from spiderPlot import SpiderPlot
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QSpinBox
from resampled_data import wave
from CSVLoader import CSVLoader  # The CSVLoader class we defined earlier

class MainApp(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the layout
        self.layout = QVBoxLayout()

        # Initialize CSVLoader
        self.csv_loader = CSVLoader()

        # Add CSVLoader components (button and label) to the layout
        self.layout.addWidget(self.csv_loader.load_button)
        self.layout.addWidget(self.csv_loader.file_count_label)

        # Example list of CSV files (can later be replaced by actual files loaded through CSVLoader)
        dir_list = ['data1', 'data2']  # List of CSV files (without the .csv extension)
        target_sampling_rate = 10  # The desired sampling rate
        interpolation_order = 'linear'  # Interpolation method, could be 'linear', 'quadratic', etc.

        # Instantiate the wave class to process the data
        self.wave_instance = wave(dir_list, target_sampling_rate, interpolation_order)

        # Instantiate SpiderPlot with the resampled data
        self.spider_plot = SpiderPlot(self.wave_instance.data_samples)
        
        # Add the SpiderPlot widget to the layout
        self.layout.addWidget(self.spider_plot)

        # Set the layout to the main window
        self.setLayout(self.layout)
        self.setWindowTitle("CSV Loader and Spider Plot Viewer")
        self.setGeometry(200, 200, 600, 800)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Instantiate and display the main application window
    main_window = MainApp()
    main_window.show()

    sys.exit(app.exec_())
