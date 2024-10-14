import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel

class CSVLoader(QWidget):
    def __init__(self):
        super().__init__()

        self.csv_files = []
        
        self.load_button = QPushButton('Load CSV Files')
        self.load_button.clicked.connect(self.load_csv_files)
        self.file_count_label = QLabel("No files loaded.")
        
        
        
    def load_csv_files(self):
        """
        Open a file dialog to select CSV files and save the file paths to the list.
        """
        # Open the file dialog to select multiple CSV files
        files, _ = QFileDialog.getOpenFileNames(self, "Open CSV Files", "", "CSV Files (*.csv)")
        
        # If files are selected, store the file paths
        if files:
            self.csv_files.extend(files)
            self.update_file_count_label()
            
    def update_file_count_label(self):
        """
        Update the label to show the number of CSV files loaded.
        """
        file_count = len(self.csv_files)
        self.file_count_label.setText(f"{file_count} file(s) loaded.")
    
    def get_csv_files(self):
        """
        Return the list of CSV file paths.
        """
        return self.csv_files
