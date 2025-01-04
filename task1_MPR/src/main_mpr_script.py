import sys
import numpy as np
import SimpleITK as sitk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QSlider,
    QHBoxLayout, QPushButton, QLabel, QFileDialog)
from PyQt5.QtCore import Qt

class MultiViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize parameters
        self.data = None
        self.z_dim = 0
        self.y_dim = 0
        self.x_dim = 0
        self.axial_idx = 0
        self.coronal_idx = 0
        self.sagittal_idx = 0
        self.selected_point = [0, 0, 0]

        # Separate brightness and contrast for each view
        self.axial_brightness = 0
        self.axial_contrast = 0
        self.coronal_brightness = 0
        self.coronal_contrast = 0
        self.sagittal_brightness = 0
        self.sagittal_contrast = 0

        # Set up the UI
        self.initUI()

    def initUI(self):
        # Create the main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Button for loading .nii file
        load_button = QPushButton("Load NIfTI File")
        load_button.clicked.connect(self.load_nii_file)
        main_layout.addWidget(load_button)

        # Create control panel for views
        views_layout = QHBoxLayout()
        self.create_view(views_layout, "Axial")
        self.create_view(views_layout, "Coronal")
        self.create_view(views_layout, "Sagittal")
        main_layout.addLayout(views_layout)

        # Create a separate layout for sliders
        sliders_layout = QHBoxLayout()
        self.create_slice_sliders(sliders_layout)
        main_layout.addLayout(sliders_layout)  # Add sliders layout to the main layout

        # Add reset button
        reset_button = QPushButton("Reset View")
        reset_button.clicked.connect(self.reset_view)
        main_layout.addWidget(reset_button)

        # Set the stylesheet for the application
        self.setStyleSheet(self.main_style())

        # Initial view update
        self.update_views()

    def load_nii_file(self):
        """ Open a file dialog to select a NIfTI file. """
        options = QFileDialog.Options()
        nii_file, _ = QFileDialog.getOpenFileName(self, "Open NIfTI File", "", "NIfTI Files (*.nii *.nii.gz);;All Files (*)", options=options)

        if nii_file:
            self.data = sitk.GetArrayFromImage(sitk.ReadImage(nii_file))
            self.z_dim, self.y_dim, self.x_dim = self.data.shape

            # Reinitialize slice indices and selected point
            self.axial_idx = self.z_dim // 2
            self.coronal_idx = self.y_dim // 2
            self.sagittal_idx = self.x_dim // 2
            self.selected_point = [self.axial_idx, self.coronal_idx, self.sagittal_idx]

            # Update the maximum values for sliders based on the new dimensions
            self.axial_slider.setRange(0, self.z_dim - 1)
            self.axial_slider.setValue(self.axial_idx)

            self.coronal_slider.setRange(0, self.y_dim - 1)
            self.coronal_slider.setValue(self.coronal_idx)

            self.sagittal_slider.setRange(0, self.x_dim - 1)
            self.sagittal_slider.setValue(self.sagittal_idx)

            # Reset zoom levels
            self.axial_zoom_slider.setValue(100)
            self.coronal_zoom_slider.setValue(100)
            self.sagittal_zoom_slider.setValue(100)

            # Update views
            self.update_views()

    def create_view(self, layout, orientation):
        """ Create a view (axial, coronal, sagittal) with corresponding controls. """
        view = plt.figure()
        ax = view.add_subplot(111)
        canvas = FigureCanvas(view)

        view_layout = QVBoxLayout()
        view_layout.addWidget(canvas)

        # Zoom slider for each view
        zoom_layout = QHBoxLayout()
        zoom_label = QLabel(f"Zoom {orientation}")
        zoom_slider = self.create_slider(100, 300, 100, self.update_views)
        zoom_layout.addWidget(zoom_label)
        zoom_layout.addWidget(zoom_slider)
        view_layout.addLayout(zoom_layout)

        # Brightness and contrast sliders for each view
        brightness_slider = self.create_slider(-100, 250, 75, lambda: self.update_brightness(orientation))
        contrast_slider = self.create_slider(-50, 200, 0, lambda: self.update_contrast(orientation))
        brightness_label = QLabel(f"Brightness {orientation}")
        contrast_label = QLabel(f"Contrast {orientation}")

        brightness_layout = QHBoxLayout()
        brightness_layout.addWidget(brightness_label)
        brightness_layout.addWidget(brightness_slider)
        view_layout.addLayout(brightness_layout)

        contrast_layout = QHBoxLayout()
        contrast_layout.addWidget(contrast_label)
        contrast_layout.addWidget(contrast_slider)
        view_layout.addLayout(contrast_layout)

        layout.addLayout(view_layout)

        # Assign attributes dynamically for each view
        setattr(self, f'{orientation.lower()}_view', view)
        setattr(self, f'{orientation.lower()}_ax', ax)
        setattr(self, f'{orientation.lower()}_canvas', canvas)
        setattr(self, f'{orientation.lower()}_zoom_slider', zoom_slider)
        setattr(self, f'{orientation.lower()}_brightness_slider', brightness_slider)
        setattr(self, f'{orientation.lower()}_contrast_slider', contrast_slider)

        # Connect mouse events for point selection
        canvas.mpl_connect('button_press_event', lambda event: self.on_mouse_press(canvas, orientation, event))

    def create_slider(self, min_val, max_val, init_val, callback):
        """ Create a customizable slider. """
        slider = QSlider(Qt.Horizontal)
        slider.setRange(min_val, max_val)
        slider.setValue(init_val)
        slider.valueChanged.connect(callback)
        return slider

    def create_slice_sliders(self, layout):
        """ Create horizontal sliders for slice navigation. """
        # Layout for vertical sliders
        slider_layout = QHBoxLayout()

        # Axial Slider
        self.axial_slider = self.create_vertical_slider(0, self.axial_idx, self.update_views_from_axial_slider)
        slider_layout.addWidget(QLabel("Axial"), alignment=Qt.AlignCenter)
        slider_layout.addWidget(self.axial_slider)

        # Coronal Slider
        self.coronal_slider = self.create_vertical_slider(0, self.coronal_idx, self.update_views_from_coronal_slider)
        slider_layout.addWidget(QLabel("Coronal"), alignment=Qt.AlignCenter)
        slider_layout.addWidget(self.coronal_slider)

        # Sagittal Slider
        self.sagittal_slider = self.create_vertical_slider(0, self.sagittal_idx, self.update_views_from_sagittal_slider)
        slider_layout.addWidget(QLabel("Sagittal"), alignment=Qt.AlignCenter)
        slider_layout.addWidget(self.sagittal_slider)

        layout.addLayout(slider_layout)  # Add the slider layout to the main layout

    def create_vertical_slider(self, min_value, init_value, callback):
        """ Create a vertical slider. """
        slider = QSlider(Qt.Vertical)
        slider.setMinimum(min_value)
        slider.setValue(init_value)
        slider.valueChanged.connect(callback)
        return slider

    def apply_brightness_contrast(self, image, brightness, contrast):
        """ Apply brightness and contrast adjustments to the image. """
        adjusted_image = image.astype(np.float32) + brightness
        adjusted_image = np.clip(adjusted_image, 0, 255)

        contrast_factor = (contrast + 50) / 50
        adjusted_image = ((adjusted_image - 127.5) * contrast_factor + 127.5)
        adjusted_image = np.clip(adjusted_image, 0, 255)

        return adjusted_image.astype(np.uint8)

    def update_views(self):
        if self.data is not None:
            self.update_axial_view()
            self.update_coronal_view()
            self.update_sagittal_view()

    def update_brightness(self, orientation):
        """ Update brightness for a specific view. """
        slider = getattr(self, f'{orientation.lower()}_brightness_slider')
        setattr(self, f'{orientation.lower()}_brightness', slider.value())
        self.update_views()

    def update_contrast(self, orientation):
        """ Update contrast for a specific view. """
        slider = getattr(self, f'{orientation.lower()}_contrast_slider')
        setattr(self, f'{orientation.lower()}_contrast', slider.value())
        self.update_views()

    def update_axial_view(self):
        if self.data is not None:
            self.update_view(self.axial_ax, self.axial_canvas, self.data[self.axial_idx], 'Axial', [self.selected_point[2], self.selected_point[1]], self.axial_zoom_slider, self.axial_brightness, self.axial_contrast)

    def update_coronal_view(self):
        if self.data is not None:
            self.update_view(self.coronal_ax, self.coronal_canvas, self.data[:, self.coronal_idx], 'Coronal', [self.selected_point[2], self.selected_point[0]], self.coronal_zoom_slider, self.coronal_brightness, self.coronal_contrast)

    def update_sagittal_view(self):
        if self.data is not None:
            self.update_view(self.sagittal_ax, self.sagittal_canvas, self.data[:, :, self.sagittal_idx], 'S agittal', [self.selected_point[1], self.selected_point[0]], self.sagittal_zoom_slider, self.sagittal_brightness, self.sagittal_contrast)

    def update_view(self, ax, canvas, data, orientation, point, zoom_slider, brightness, contrast):
        """ Update a specific view with brightness, contrast, and zoom adjustments. """
        ax.clear()
        ax.imshow(self.apply_brightness_contrast(data, brightness, contrast), cmap='gray')
        ax.plot(point[0], point[1], 'ro')

        # Draw axes lines
        ax.axhline(y=point[1], color='r', linestyle='--')
        ax.axvline(x=point[0], color='r', linestyle='--')

        # Apply zoom from slider
        zoom_factor = zoom_slider.value() / 100
        height, width = data.shape
        center_x, center_y = width // 2, height // 2
        half_width = width / (2 * zoom_factor)
        half_height = height / (2 * zoom_factor)
        ax.set_xlim([center_x - half_width, center_x + half_width])
        ax.set_ylim([center_y - half_height, center_y + half_height])

        ax.set_title(f'{orientation} View')
        canvas.draw()

    def update_views_from_axial_slider(self):
        self.axial_idx = self.axial_slider.value()
        self.selected_point[0] = self.axial_idx
        self.update_views()

    def update_views_from_coronal_slider(self):
        self.coronal_idx = self.coronal_slider.value()
        self.selected_point[1] = self.coronal_idx
        self.update_views()

    def update_views_from_sagittal_slider(self):
        self.sagittal_idx = self.sagittal_slider.value()
        self.selected_point[2] = self.sagittal_idx
        self.update_views()

    def on_mouse_press(self, canvas, orientation, event):
        """ Handle mouse press to mark a selected point in a specific view. """
        if event.button == 1:  # Left mouse button
            if orientation == "Axial":
                self.selected_point[1] = int(event.ydata)
                self.selected_point[2] = int(event.xdata)
                self.coronal_slider.setValue(self.selected_point[1])
                self.sagittal_slider.setValue(self.selected_point[2])
            elif orientation == "Coronal":
                self.selected_point[0] = int(event.ydata)
                self.selected_point[2] = int(event.xdata)
                self.axial_slider.setValue(self.selected_point[0])
                self.sagittal_slider.setValue(self.selected_point[2])
            elif orientation == "Sagittal":
                self.selected_point[0] = int(event.ydata)
                self.selected_point[1] = int(event.xdata)
                self.axial_slider.setValue(self.selected_point[0])
                self.coronal_slider.setValue(self.selected_point[1])
            self.update_views()

    def reset_view(self):
        """ Reset all views to their initial state. """
        if self.data is not None:
            self.axial_idx = self.z_dim // 2
            self.coronal_idx = self.y_dim // 2
            self.sagittal_idx = self.x_dim // 2
            self.selected_point = [self.axial_idx, self.coronal_idx, self.sagittal_idx]

            self.axial_slider.setValue(self.axial_idx)
            self.coronal_slider.setValue(self.coronal_idx)
            self.sagittal_slider.setValue(self.sagittal_idx)

            self.axial_zoom_slider.setValue(100)
            self.coronal_zoom_slider.setValue(100)
            self.sagittal_zoom_slider.setValue(100)

            self.axial_brightness_slider.setValue(0)
            self.axial_contrast_slider.setValue(0)
            self.coronal_brightness_slider.setValue(0)
            self.coronal_contrast_slider.setValue(0)
            self.sagittal_brightness_slider.setValue(0)
            self.sagittal_contrast_slider.setValue(0)

            self.axial_brightness = 0
            self.axial_contrast = 0
            self.coronal_brightness = 0
            self.coronal_contrast = 0
            self.sagittal_brightness = 0
            self.sagittal_contrast = 0

            self.update_views()

    def main_style(self):
        return """
            QPushButton {
                background-color: #3498db;
                color: white;
                font-size: 18px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QLabel {
                font-size: 16px;
            }
            QSlider {
                background-color: #f2f2f2;
            }
        """


if __name__ == '__main__':
    app = QApplication(sys.argv)

    viewer = MultiViewer()
    viewer.setWindowTitle('NIfTI Multi-Viewer')
    viewer.setGeometry(100, 100, 1200, 800)  # Set a reasonable window size
    viewer.show()

    sys.exit(app.exec_())
