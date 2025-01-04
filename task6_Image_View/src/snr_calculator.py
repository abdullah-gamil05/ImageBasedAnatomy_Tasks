class SNRCalculator(QMainWindow):
    def __init__(self, parent=None, image=None):
        super().__init__(parent)
        self.setWindowTitle("SNR Calculator")
        self.setGeometry(100, 100, 800, 400)

        # Layouts
        self.main_layout = QVBoxLayout()
        self.input_layout = QVBoxLayout()
        self.output_layout = QVBoxLayout()

        # Input Image View
        self.input_label = QLabel(self)
        self.input_label.setAlignment(Qt.AlignCenter)
        self.input_layout.addWidget(self.input_label)

        # Display the passed image
        if image is not None:
            self.image = image
            self.display_input_image(image)

        # SNR Calculation
        self.snr_button = QPushButton("Calculate SNR", self)
        self.snr_button.clicked.connect(self.calculate_snr)
        self.input_layout.addWidget(self.snr_button)

        # CNR Calculation
        self.cnr_button = QPushButton("Calculate CNR", self)
        self.cnr_button.clicked.connect(self.calculate_cnr)
        self.input_layout.addWidget(self.cnr_button)

        #Reset button 3la baseet
        self.reset_button = QPushButton("Reset", self)
        self.reset_button.clicked.connect(self.reset_ROIs)
        self.input_layout.addWidget(self.reset_button)

        self.undo_button = QPushButton("Undo", self)
        self.undo_button.clicked.connect(self.remove_last_roi)
        self.input_layout.addWidget(self.undo_button)

        # Output Labels
        self.output_label = QLabel("SNR/CNR: Not calculated", self)
        self.output_label.setAlignment(Qt.AlignCenter)
        self.output_layout.addWidget(self.output_label)

        # Add layouts to main layout
        self.main_layout.addLayout(self.input_layout)
        self.main_layout.addLayout(self.output_layout)

        container = QWidget()
        container.setLayout(self.main_layout)
        self.setCentralWidget(container)

        # Variables
        self.start_point = None
        self.current_rect = None
        self.rois = []  # List to store multiple ROIs
        self.drawing_roi = False


    def reset_ROIs(self):
        self.rois.clear()
        self.drawing_roi = False
        self.current_rect = None
        self.start_point = None
        self.update()

    def remove_last_roi(self):
        if self.rois:
            self.rois.pop()
            self.update()  # Refresh the display

    def display_input_image(self, img):
        """Display the loaded grayscale image on the label."""
        height, width = img.shape
        label_width = self.input_label.width()
        label_height = self.input_label.height()
        scale = min(label_width / width, label_height / height)

        # Resize the image to fit QLabel while maintaining aspect ratio
        resized_img = cv2.resize(img, (int(width * scale), int(height * scale)), interpolation=cv2.INTER_AREA)
        height, width = resized_img.shape
        q_img = QImage(resized_img.data, width, height, width, QImage.Format_Grayscale8)
        self.input_label.setPixmap(QPixmap.fromImage(q_img))

    def map_to_label(self, global_pos):
        """Map global mouse position to QLabel coordinates."""
        label_pos = self.input_label.mapFromGlobal(global_pos)
        pixmap = self.input_label.pixmap()
        if pixmap:
            label_width = self.input_label.width()
            label_height = self.input_label.height()
            pixmap_width = pixmap.width()
            pixmap_height = pixmap.height()

            scale_x = pixmap_width / label_width
            scale_y = pixmap_height / label_height

            x = int(label_pos.x() * scale_x)
            y = int(label_pos.y() * scale_y)
            return x, y
        return None

    def mousePressEvent(self, event):
        """Handle mouse press event to start drawing an ROI."""
        if event.button() == Qt.LeftButton:
            label_coords = self.map_to_label(event.globalPos())
            if label_coords:
                self.start_point = label_coords
                self.drawing_roi = True

    def mouseMoveEvent(self, event):
        """Handle mouse move event for real-time drawing."""
        if self.drawing_roi:
            label_coords = self.map_to_label(event.globalPos())
            if label_coords:
                self.current_rect = QRect(
                    min(self.start_point[0], label_coords[0]),
                    min(self.start_point[1], label_coords[1]),
                    abs(self.start_point[0] - label_coords[0]),
                    abs(self.start_point[1] - label_coords[1]),
                )
                self.update()  # Trigger repaint for real-time feedback

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            label_coords = self.map_to_label(event.globalPos())
            if label_coords and self.drawing_roi:
                final_rect = QRect(
                    min(self.start_point[0], label_coords[0]),
                    min(self.start_point[1], label_coords[1]),
                    abs(self.start_point[0] - label_coords[0]),
                    abs(self.start_point[1] - label_coords[1]),
                )

                # Validate ROI size
                min_size = 5  # Minimum size for ROI width and height
                if final_rect.width() >= min_size and final_rect.height() >= min_size:
                    if len(self.rois) < 3:  # Limit to 3 ROIs
                        self.rois.append(final_rect)
                else:
                    print("ROI too small. Please select a larger area.")

                self.current_rect = None
                self.drawing_roi = False
                self.update()

    def paintEvent(self, event):
        """Draw the ROIs and the current rectangle in real time."""
        super().paintEvent(event)
        if self.image is not None:
            # Reset the QLabel pixmap to the original image
            height, width = self.image.shape
            q_img = QImage(self.image.data, width, height, width, QImage.Format_Grayscale8)
            self.input_label.setPixmap(QPixmap.fromImage(q_img))

            # Prepare to draw on the QLabel
            painter = QPainter(self.input_label.pixmap())

            # Draw all ROIs
            colors = [QColor(255, 0, 0), QColor(0, 255, 0), QColor(0, 0, 255)]  # Red, Green, Blue
            for i, roi in enumerate(self.rois):
                painter.setPen(colors[i % len(colors)])  # Cycle through colors
                painter.drawRect(roi)

            # Draw the current rectangle (while dragging)
            if self.current_rect:
                painter.setPen(QColor(255, 255, 0))  # Yellow for current rectangle
                painter.drawRect(self.current_rect)

            painter.end()

    def calculate_snr(self):
        if len(self.rois) >= 2 and self.image is not None:
            roi1_np = self.extract_roi(self.image, self.rois[0])
            roi2_np = self.extract_roi(self.image, self.rois[1])



            signal = np.mean(roi1_np)
            noise = np.mean(roi2_np)
            snr = signal / noise if noise != 0 else float('inf')

            self.output_label.setText(f"SNR: {snr:.2f}")
        else:
            self.output_label.setText("Please select at least 2 ROIs before calculating SNR.")

    def calculate_cnr(self):
        """Calculate the CNR using the selected ROIs."""
        if len(self.rois) == 3 and self.image is not None:
            roi1_np = self.extract_roi(self.image, self.rois[0])
            roi2_np = self.extract_roi(self.image, self.rois[1])
            roi3_np = self.extract_roi(self.image, self.rois[2])

            contrast = abs(np.mean(roi1_np) - np.mean(roi2_np))
            noise = np.std(roi3_np)
            cnr = contrast / noise if noise != 0 else float('inf')

            self.output_label.setText(f"CNR: {cnr:.2f}")
        else:
            self.output_label.setText("Please select exactly 3 ROIs before calculating CNR.")

    def extract_roi(self, image, roi):
        """Extract the pixel values from the selected ROI."""
        x1, y1, x2, y2 = roi.left(), roi.top(), roi.right(), roi.bottom()
        return image[y1:y2, x1:x2]

