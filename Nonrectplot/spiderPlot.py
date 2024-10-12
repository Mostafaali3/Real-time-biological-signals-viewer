# here we try to draw the graph (make an object that could import a CSV file based on the number of columns deside the dimentions of the graph)
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QSpinBox
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt, QPoint, QTimer
from math import cos, sin, pi, radians

import pandas as pd

class SpiderPlot(QWidget):
    def __init__(self, data_samples):
        super().__init__()
        
        # Initial window setup
        
        self.data = data_samples
        self.max_values = self.data.max(axis = 1)
        # Polygon properties
        self.radius = 200  # Radius for the circle in which the polygon is inscribed
        self.data_points, self.num_vertices = self.data.shape
  # Default number of vertices (triangle)
        self.current_row_idx = 0
        self.current_row =  self.data.loc[0, :].values.flatten().tolist()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(50)


    def update_animation(self):      
        self.current_row_idx += 1
        if self.current_row_idx >= self.data_points - 1:
            self.current_row_idx = 0
            
        self.current_row =  self.data.loc[self.current_row_idx, :].values.flatten().tolist()
        self.update()
            
    def paintEvent(self, event):
        # Initialize QPainter object
        painter = QPainter(self)
        
        # Set the pen for the polygon lines
        pen = QPen(Qt.black, 3)
        painter.setPen(pen)
        
        # Calculate the center of the widget
        center_x = self.width() // 2
        center_y = self.height() // 2
        
        print(f'{center_x}, {center_y}')
        
        # Draw the polygon
        self.draw_polygon(painter, center_x, center_y)
        self.draw_spider(painter,center_x, center_y)

    def draw_polygon(self, painter, center_x, center_y):
        # Calculate the angle between each vertex
        angle_step = 2 * pi / self.num_vertices
        
        # List to store vertices
        vertices = []
        
        center = QPoint(center_x, center_y)

        # Calculate the coordinates for each vertex
        for i in range(self.num_vertices):
            angle = i * angle_step
            x = int(center_x + self.radius * cos(angle))
            
            y = int(center_y - self.radius* sin(angle))  # Negative because of Qt's inverted y-axis
            vertices.append(QPoint(x, y))
        # Draw lines between the vertices
        painter.drawPoint(center)
        for i in range(self.num_vertices):
            next_vertex = vertices[(i + 1) % self.num_vertices]  # Wrap around to the first vertex
            painter.drawLine(vertices[i], next_vertex)
            painter.drawLine(center,vertices[i])            
            

    def draw_spider(self, painter, center_x, center_y, max= 20):
        # Calculate the angle between each vertex
        values = self.current_row
        angle_step = 2 * pi / self.num_vertices
        
        # List to store vertices
        vertices = []
        
        # Calculate the coordinates for each vertex
        for i in range(self.num_vertices):
            angle = i * angle_step
        
            x = int(center_x + self.radius*(1 - (values[i]/max)) * cos(angle))
            y = int(center_y - self.radius*(1 - (values[i]/max)) * sin(angle))  # Negative because of Qt's inverted y-axis
            vertices.append(QPoint(x, y))
        # Draw lines between the vertices
        for i in range(self.num_vertices):
            next_vertex = vertices[(i + 1) % self.num_vertices]  # Wrap around to the first vertex
            painter.drawLine(vertices[i], next_vertex)
        


