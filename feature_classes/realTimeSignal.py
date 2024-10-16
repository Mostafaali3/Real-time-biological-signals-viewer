import requests
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
import pyqtgraph as pg

class RealTimeSignal:
    def __init__(self):
        self.PlayImage = QIcon(':/Images/playW.png')
        self.PauseImage = QIcon(':/Images/pauseW.png')

        self.is_playing = True
        self.setDisabled = False

        self.x = list(range(1))  
        self.y = [0] * 1

        self.timer = QTimer()
        self.timer.setInterval(500) 
        self.timer.timeout.connect(self.update_plot_data)

    def initialize(self, RealTimeSignalInput, RealTimeViewSignalButton, PlayPauseButtonRealTime, RealTimeScroll, graphWidget):
        self.RealTimeSignalInput = RealTimeSignalInput
        self.RealTimeViewSignalButton = RealTimeViewSignalButton
        self.PlayPauseButtonRealTime = PlayPauseButtonRealTime
        self.RealTimeScroll = RealTimeScroll
        self.graphWidget = graphWidget

        self.data_line = self.graphWidget.plot(self.x, self.y)
        self.PlayPauseButtonRealTime.setIcon(self.PauseImage)

    def show_real_time_graph(self):
        self.timer.start()

    def update_plot_data(self):
        api_link = self.RealTimeSignalInput.text()
        if not api_link:
            return

        try:
            response = requests.get(api_link)
            data = response.json()
            price = float(data['bpi']['USD']['rate'].replace(',', ''))

            self.y.append(price)

            if len(self.x) < len(self.y):
                self.x.append(self.x[-1] + 1)

            self.data_line.setData(self.x, self.y)    
            self.RealTimeScroll.setRange(0, len(self.y) - 20)
            self.RealTimeScroll.setRange(0, max(0, len(self.y) - 20))
            self.RealTimeScroll.setValue(len(self.y) - 20)

        except Exception as e:
            print(f"Error fetching data: {e}")   

    def toggle_play_pause_real_time(self):
        if self.is_playing:
            self.timer.stop()
            self.PlayPauseButtonRealTime.setIcon(self.PlayImage)
        else:
            self.timer.start()
            self.PlayPauseButtonRealTime.setIcon(self.PauseImage)
        self.is_playing = not self.is_playing

    def scroll_graph(self, value):
        self.graphWidget.setXRange(value, value + 20)

    def disable_view_button(self):
        self.RealTimeViewSignalButton.setDisabled(True)

    def enable_view_button(self):
        self.RealTimeViewSignalButton.setDisabled(False)