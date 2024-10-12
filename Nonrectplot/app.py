import sys
from spiderPlot import SpiderPlot
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QSpinBox
from resampled_data import wave
from CSVLoader import CSVLoader  # The CSVLoader class we defined earlier

'''
We still need to:
    set labels (column names) to the vertices 
    make the movement smoother
    plot a time series data not jest values
    some ui tools:
        upload file
        start
        stop
        time frame showed as a timer stop watch
'''
if __name__ == "__main__":
    # Example usage
    
    app = QApplication(sys.argv)

    csv_loader = CSVLoader()

    dir_list = ['data1', 'data2']  # List of CSV files (without the .csv extension)
    target_sampling_rate = 10  # The desired sampling rate
    interpolation_order = 'linear'  # Interpolation method, could be 'linear', 'quadratic', etc.

    # Instantiate the wave class
    wave_instance = wave(dir_list, target_sampling_rate, interpolation_order)
    
    # Print the resampled data
    print(wave_instance.data_samples)

    dirs = []
    layout = QVBoxLayout()

    window = SpiderPlot(wave_instance.data_samples)
    window.setWindowTitle("Spider Plot")
    window.setGeometry(200, 200, 600, 800)
    layout.addWidget(csv_loader.load_button)
    layout.addWidget(csv_loader.file_count_label)
    layout.addWidget(window)
    window.show()
    sys.exit(app.exec_())
