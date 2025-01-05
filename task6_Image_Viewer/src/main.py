import sys
import numpy as np
import cv2
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSlider,
                             QPushButton, QGroupBox, QGraphicsView, QGraphicsScene, QStyle, QLabel,
                             QFrame, QSizePolicy, QFileDialog, QMessageBox, QInputDialog, QComboBox)
from PyQt5.QtCore import Qt, QSize, QRect
from PyQt5.QtGui import QPalette, QColor, QFont, QPainter, QImage, QPixmap

# Import the ImageViewer class from viewer.py

def main():
    """Main entry point for the Image Viewer application."""
    app = QApplication(sys.argv)
    viewer = ImageViewer()  # Create an instance of the ImageViewer
    viewer.show()           # Show the main window
    sys.exit(app.exec_())   # Execute the application

if __name__ == "__main__":
    main()