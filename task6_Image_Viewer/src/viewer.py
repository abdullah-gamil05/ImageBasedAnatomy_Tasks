class ImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pro Image Viewer")
        self.setGeometry(100, 100, 1400, 900)

        # Initialize variables
        self.input_image = None
        self.output_image1 = None
        self.output_image2 = None
        self.history_output1 = []  # Stack to keep track of output_image1 states
        self.history_output2 = []  # Stack to keep track of output_image2 states
        self.interpolation_method = 'linear'

        # Set dark theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ffffff;  /* White background for the main window */
            }
            QWidget {
                color: #333333;  /* Dark gray text color for better contrast */
                font-size: 12px;
            }
            QPushButton {
                background-color: #f0f0f0;  /* Light gray background for buttons */
                border: 1px solid #cccccc;  /* Light border for buttons */
                border-radius: 4px;
                padding: 8px 16px;
                margin: 2px;
                color: #333333;  /* Dark gray text color for buttons */
            }
            QPushButton:hover {
                background-color: #e0e0e0;  /* Slightly darker gray on hover */
            }
            QPushButton:pressed {
                background-color: #d0d0d0;  /* Even darker gray when pressed */
            }
            QGroupBox {
                border: 1px solid #cccccc;  /* Light border for group boxes */
                border-radius: 4px;
                margin-top: 10px;
                padding-top: 15px;
                background-color: #fafafa;  /* Very light gray background for group boxes */
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
                color: #333333;  /* Dark gray title text color */
            }
            QGraphicsView {
                border: 2px solid #cccccc;  /* Light border for graphics view */
                border-radius: 4px;
                background-color: #ffffff;  /* White background for graphics view */
            }
        """)

        self.initUI()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main layout
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Title and toolbar
        toolbar_layout = QHBoxLayout()
        title_label = QLabel("Pro Image Viewer")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #ffffff;")
        toolbar_layout.addWidget(title_label)
        toolbar_layout.addStretch()

        # Basic tools in toolbar
        tools_group = QGroupBox()
        tools_group.setStyleSheet("QGroupBox { border: none; }")
        tools_layout = QHBoxLayout(tools_group)

        # Add toolbar buttons
        self.load_button = QPushButton("Load Image")
        self.zoom_in_button = QPushButton("Zoom In")
        self.zoom_out_button = QPushButton("Zoom Out")
        self.reset_button = QPushButton("Reset")
        self.undo_button = QPushButton("Undo")

        # Zoom type combo box
        self.zoom_type_combo = QComboBox()
        self.zoom_type_combo.addItems(["Nearest", "Linear", "Bilinear", "Cubic"])
        self.zoom_type_combo.currentIndexChanged.connect(self.update_interpolation_method)

        # Add the combo box to the tools layout
        tools_layout.addWidget(self.zoom_type_combo)

        tools_layout.addWidget(self.undo_button)
        tools_layout.addWidget(self.load_button)
        tools_layout.addWidget(self.zoom_in_button)
        tools_layout.addWidget(self.zoom_out_button)
        tools_layout.addWidget(self.reset_button)


        toolbar_layout.addWidget(tools_group)
        main_layout.addLayout(toolbar_layout)

        # Brightness and Contrast sliders
        sliders_group = QGroupBox("Brightness and Contrast Adjustments")
        sliders_layout = QHBoxLayout(sliders_group)

        self.brightness_slider_input = self.create_slider("Brightness (Input)")
        self.contrast_slider_input = self.create_slider("Contrast (Input)")
        self.brightness_slider_output1 = self.create_slider("Brightness (Output 1)")
        self.contrast_slider_output1 = self.create_slider("Contrast (Output 1)")
        self.brightness_slider_output2 = self.create_slider("Brightness (Output 2)")
        self.contrast_slider_output2 = self.create_slider("Contrast (Output 2)")

        # Add sliders to the layout
        sliders_layout.addWidget(QLabel("Brightness (Input)"))
        sliders_layout.addWidget(self.brightness_slider_input)
        sliders_layout.addWidget(QLabel("Contrast (Input)"))
        sliders_layout.addWidget(self.contrast_slider_input)
        sliders_layout.addWidget(QLabel("Brightness (Output 1)"))
        sliders_layout.addWidget(self.brightness_slider_output1)
        sliders_layout.addWidget(QLabel("Contrast (Output 1)"))
        sliders_layout.addWidget(self.contrast_slider_output1)
        sliders_layout.addWidget(QLabel("Brightness (Output 2)"))
        sliders_layout.addWidget(self.brightness_slider_output2)
        sliders_layout.addWidget(QLabel("Contrast (Output 2)"))
        sliders_layout.addWidget(self.contrast_slider_output2)

        # Add the sliders group to the main layout
        main_layout.addWidget(sliders_group)

        # Image views
        views_layout = QHBoxLayout()
        views_layout.setSpacing(15)

        # Create image view containers
        self.input_view = self.create_image_view("Input Image")
        self.output_view1 = self.create_image_view("Output 1")
        self.output_view2 = self.create_image_view("Output 2")

        # Connect double-click events to show histograms

        self.input_view.mouseDoubleClickEvent = lambda event: self.show_histogram(self.input_image,
                                                                                  "Input Image Histogram")
        self.output_view1.mouseDoubleClickEvent = lambda event: self.show_histogram(self.output_image1,
                                                                                    "Output 1 Histogram")
        self.output_view2.mouseDoubleClickEvent = lambda event: self.show_histogram(self.output_image2,
                                                                                    "Output 2 Histogram")

        self.input_scene = self.input_view.scene()
        self.output_scene1 = self.output_view1.scene()
        self.output_scene2 = self.output_view2.scene()


        views_layout.addWidget(self.create_view_container(self.input_view, "Input Image"))
        views_layout.addWidget(self.create_view_container(self.output_view1, "Processed Image 1"))
        views_layout.addWidget(self.create_view_container(self.output_view2, "Processed Image 2"))

        main_layout.addLayout(views_layout)

        # Bottom controls
        controls_layout = QHBoxLayout()

        # Image processing tools
        processing_group = QGroupBox("Image Processing")
        processing_layout = QHBoxLayout()

        # Create processing buttons
        self.noise_button = self.create_processing_button("Add Noise")
        self.denoise_button = self.create_processing_button("Denoise")
        self.contrast_button = self.create_processing_button("Contrast")

        processing_layout.addWidget(self.noise_button)
        processing_layout.addWidget(self.denoise_button)
        processing_layout.addWidget(self.contrast_button)
        processing_group.setLayout(processing_layout)

        # Filters group
        filters_group = QGroupBox("Filters")
        filters_layout = QHBoxLayout()

        self.lowpass_button = self.create_processing_button("Lowpass")
        self.highpass_button = self.create_processing_button("Highpass")

        filters_layout.addWidget(self.lowpass_button)
        filters_layout.addWidget(self.highpass_button)
        filters_group.setLayout(filters_layout)

        # Add groups to controls layout
        controls_layout.addWidget(processing_group)
        controls_layout.addWidget(filters_group)

        # Add SNR calculation group
        snr_group = QGroupBox("Signal-to-Noise & Contrast-to-Noise Ratio")
        snr_layout = QHBoxLayout()

        self.snr_input_button = self.create_processing_button("SNR,CNR_0")
        self.snr_output1_button = self.create_processing_button("SNR,CNR_1")
        self.snr_output2_button = self.create_processing_button("SNR,CNR_2")

        snr_layout.addWidget(self.snr_input_button)
        snr_layout.addWidget(self.snr_output1_button)
        snr_layout.addWidget(self.snr_output2_button)
        snr_group.setLayout(snr_layout)

        controls_layout.addWidget(snr_group)
        main_layout.addLayout(controls_layout)


        # Connect signals
        self.connect_signals()

    def create_processing_button(self, text):
        button = QPushButton(text)
        button.setFixedWidth(100)
        return button

    def create_image_view(self, title):
        view = QGraphicsView()
        view.setScene(QGraphicsScene())
        view.setFixedSize(600, 600)
        view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        view.setRenderHint(QPainter.SmoothPixmapTransform)
        return view

    def create_view_container(self, view, title):
        container = QFrame()
        container.setFrameStyle(QFrame.StyledPanel)
        layout = QVBoxLayout(container)

        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-weight: bold; margin-bottom: 5px;")

        layout.addWidget(title_label)
        layout.addWidget(view)
        return container

    def connect_signals(self):
        # Connect all the button signals to their respective slots
        self.load_button.clicked.connect(self.load_image)
        self.zoom_in_button.clicked.connect(self.zoom_in)
        self.zoom_out_button.clicked.connect(self.zoom_out)
        self.reset_button.clicked.connect(self.reset_outputs)
        self.noise_button.clicked.connect(self.add_noise)
        self.denoise_button.clicked.connect(self.denoise)
        self.contrast_button.clicked.connect(self.adjust_contrast)
        self.lowpass_button.clicked.connect(self.apply_lowpass_filter)
        self.highpass_button.clicked.connect(self.apply_highpass_filter)
        self.snr_input_button.clicked.connect(self.open_snr_calculator_input)
        self.snr_output1_button.clicked.connect(self.open_snr_calculator_output1)
        self.snr_output2_button.clicked.connect(self.open_snr_calculator_output2)
        self.undo_button.clicked.connect(self.undo)

    def reset_outputs(self):
        """Reset the output images and sliders."""
        self.output_image1 = None
        self.output_image2 = None
        self.output_scene1.clear()  # Clear the first output scene
        self.output_scene2.clear()# Clear the second output scene
        self.history_output1.clear()
        self.history_output2.clear()

        # Reset brightness and contrast sliders to 0
        self.brightness_slider_input.setValue(0)
        self.contrast_slider_input.setValue(0)
        self.brightness_slider_output1.setValue(0)
        self.contrast_slider_output1.setValue(0)
        self.brightness_slider_output2.setValue(0)
        self.contrast_slider_output2.setValue(0)

    def undo(self):
        """Undo the last image processing action."""
        if self.history_output2:
            # Restore the last state of output_image2
            self.output_image2 = self.history_output2.pop()
            self.display_image(self.output_image2, self.output_scene2)
        elif self.history_output1:
            # Restore the last state of output_image1 or input_image
            self.output_image1 = self.history_output1.pop()
            self.display_image(self.output_image1, self.output_scene1)
        else:
            # If no history, clear the output images
            if self.output_image2 is not None:
                self.output_image2 = None
                self.output_scene2.clear()  # Clear the second output scene
            elif self.output_image1 is not None:
                self.output_image1 = None
                self.output_scene1.clear()  # Clear the first output scene
            else:
                QMessageBox.warning(self, "Warning", "No actions to undo.")

    def update_interpolation_method(self, index):
        """Update the interpolation method based on the selected item in the combo box."""
        if index == 0:
            self.interpolation_method = 'nearest'
        elif index == 1:
            self.interpolation_method = 'linear'
        elif index == 2:
            self.interpolation_method = 'bilinear'
        elif index == 3:
            self.interpolation_method = 'cubic'


    def create_slider(self, label):
        slider = QSlider(Qt.Horizontal)
        slider.setRange(-100, 100)
        slider.setValue(0)
        slider.setTickPosition(QSlider.TicksBelow)
        slider.setTickInterval(10)
        slider.setSingleStep(1)
        slider.valueChanged.connect(self.update_image)
        return slider

    def update_image(self):
        # Update the images based on the slider values
        if self.input_image is not None:
            brightness_input = self.brightness_slider_input.value()
            contrast_input = self.contrast_slider_input.value()
            adjusted_input = self.adjust_brightness_contrast(self.input_image, brightness_input, contrast_input)
            self.display_image(adjusted_input, self.input_scene)

            if self.output_image1 is not None:
                brightness_output1 = self.brightness_slider_output1.value()
                contrast_output1 = self.contrast_slider_output1.value()
                adjusted_output1 = self.adjust_brightness_contrast(self.output_image1, brightness_output1,
                                                                   contrast_output1)
                self.display_image(adjusted_output1, self.output_scene1)

                if self.output_image2 is not None:
                    brightness_output2 = self.brightness_slider_output2.value()
                    contrast_output2 = self.contrast_slider_output2.value()
                    adjusted_output2 = self.adjust_brightness_contrast(self.output_image2, brightness_output2,
                                                                       contrast_output2)
                    self.display_image(adjusted_output2, self.output_scene2)

    def adjust_brightness_contrast(self, img, brightness, contrast):
        # Adjust brightness and contrast of the image
        img = cv2.convertScaleAbs(img, alpha=(contrast / 100 + 1), beta=brightness+32)
        return img

    def apply_lowpass_filter(self):
        if self.input_image is not None:
            # Check which images are available and show the result accordingly
            if self.output_image1 is None:
                # If only input image is available, show filtered image in output1
                # Apply Gaussian Blur as a low-pass filter
                filtered_image = cv2.GaussianBlur(self.input_image, (5, 5), 0)
                self.output_image1 = filtered_image
                self.display_image(filtered_image, self.output_scene1)
            elif self.output_image1 is not None and self.output_image2 is None:
                # If both input and output1 are available, show filtered image in output2
                # Apply Gaussian Blur as a low-pass filter
                self.history_output1.append(self.output_image1.copy())
                filtered_image = cv2.GaussianBlur(self.output_image1, (5, 5), 0)
                self.output_image2 = filtered_image
                self.display_image(filtered_image, self.output_scene2)
            elif self.output_image1 is not None and self.output_image2 is not None:
                # If all three images are available, apply low-pass filter to output2
                # Apply Gaussian Blur as a low-pass filter
                self.history_output2.append(self.output_image2.copy())
                filtered_image = cv2.GaussianBlur(self.output_image2, (5, 5), 0)
                self.output_image2 = filtered_image
                self.display_image(filtered_image, self.output_scene2)

    def apply_highpass_filter(self):
        if self.input_image is not None:

            # Check which images are available and show the result accordingly
            if self.output_image1 is None:
                # If only input image is available, show filtered image in output1
                # Apply a high-pass filter using a kernel
                kernel = np.array([[0, -1, 0],
                                   [-1, 5, -1],
                                   [0, -1, 0]])
                filtered_image = cv2.filter2D(self.input_image, -1, kernel)
                self.output_image1 = filtered_image
                self.display_image(filtered_image, self.output_scene1)
            elif self.output_image1 is not None and self.output_image2 is None:
                # If both input and output1 are available, show filtered image in output2
                # Apply a high-pass filter using a kernel
                self.history_output1.append(self.output_image1.copy())
                kernel = np.array([[0, -1, 0],
                                   [-1, 5, -1],
                                   [0, -1, 0]])
                filtered_image = cv2.filter2D(self.output_image1, -1, kernel)
                self.output_image2 = filtered_image
                self.display_image(filtered_image, self.output_scene2)
            elif self.output_image1 is not None and self.output_image2 is not None:
                # If all three images are available, apply high-pass filter to output2
                # Apply a high-pass filter using a kernel
                self.history_output2.append(self.output_image2.copy())
                kernel = np.array([[0, -1, 0],
                                   [-1, 5, -1],
                                   [0, -1, 0]])
                filtered_image = cv2.filter2D(self.output_image2, -1, kernel)
                self.output_image2 = filtered_image
                self.display_image(filtered_image, self.output_scene2)

    def open_snr_calculator_input(self):
        if self.input_image is not None:
            snr_calculator = SNRCalculator(self, self.input_image)
            snr_calculator.show()


    def open_snr_calculator_output1(self):
        if self.output_image1 is not None:
            snr_calculator = SNRCalculator(self, self.output_image1)
            snr_calculator.show()

    def open_snr_calculator_output2(self):
        if self.output_image2 is not None:
            snr_calculator = SNRCalculator(self, self.output_image2)
            snr_calculator.show()



    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "",
                                                   "Images (*.png  *.jpg *.jpeg *.bmp *.gif)")
        if file_name:
            self.input_image = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE)
            #self.input_image = cv2.imread(file_name)
            if self.input_image is not None:
                #self.input_image = cv2.cvtColor(self.input_image, cv2.COLOR_BGR2RGB)
                self.display_image(self.input_image, self.input_scene)
            else:
                QMessageBox.critical(self, "Error", "Failed to load image.")

    def display_image(self, img, scene):
        #height, width, channel = img.shape
        height, width = img.shape
        #bytes_per_line = width * 3
        #q_img = QImage(img.data, width, height, bytes_per_line, QImage.Format_RGB888)
        q_img = QImage(img.data, width, height, width, QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(q_img)
        scene.clear()
        scene.addPixmap(pixmap)
        scene.setSceneRect(0, 0, width, height)
        for view in [self.input_view]:
            if view.scene() == scene:
                view.fitInView(scene.sceneRect(), Qt.KeepAspectRatio)

    def zoom_in(self):
        if self.input_image is not None:
            if self.output_image1 is None :
                # Save the current state of input_image before zooming
                self.history_output1.append(self.input_image.copy())
                # Zoom input_image and store it in output_image1
                self.output_image1 = self.zoom(self.input_image, 1.4)
                self.display_image(self.output_image1, self.output_scene1)
            elif self.output_image1 is not None :
                # Save the current state of output_image1 before zooming
                self.history_output1.append(self.output_image1.copy())
                # Zoom output_image1 and store it in output_image2
                self.output_image2 = self.zoom(self.output_image1, 1.4)
                self.display_image(self.output_image2, self.output_scene2)
            elif self.output_image2 is not None:
                # Save the current state of output_image2 before zooming
                self.history_output2.append(self.output_image2.copy())
                # Zoom output_image2
                self.output_image2 = self.zoom(self.output_image2, 1.4)
                self.display_image(self.output_image1, self.output_scene1)

    def zoom_out(self):
        if self.input_image is not None:
            if self.output_image1 is None and self.output_image2 is None:
                # Save the current state of input_image before zooming
                self.history_output1.append(self.input_image.copy())
                # Zoom input_image and store it in output_image1
                self.output_image1 = self.zoom(self.input_image, 0.8)
                self.display_image(self.output_image1, self.output_scene1)
            elif self.output_image1 is not None and self.output_image2 is None:
                # Save the current state of output_image1 before zooming
                self.history_output1.append(self.output_image1.copy())
                # Zoom output_image1 and store it in output_image2
                self.output_image2 = self.zoom(self.output_image1, 0.8)
                self.display_image(self.output_image2, self.output_scene2)
            elif self.output_image2 is not None:
                # Save the current state of output_image2 before zooming
                self.history_output2.append(self.output_image2.copy())
                # Zoom output_image2
                self.output_image2 = self.zoom(self.output_image2, 0.8)
                self.display_image(self.output_image2, self.output_scene2)

    def zoom(self, img, zoom_factor):
        if self.interpolation_method == 'nearest':
            return self.nearest_neighbor_zoom(img, zoom_factor)
        elif self.interpolation_method == 'linear':
            return self.linear_zoom(img, zoom_factor)
        elif self.interpolation_method == 'bilinear':
            return self.bilinear_zoom(img, zoom_factor)
        elif self.interpolation_method == 'cubic':
            return self.cubic_zoom(img, zoom_factor)


    def nearest_neighbor_zoom(self, img, zoom_factor):

        try:
            height, width = img.shape
            new_height, new_width = int(height * zoom_factor), int(width * zoom_factor)
            zoomed_image = np.zeros((new_height, new_width), dtype=img.dtype)

            # Using floor division for indices
            for i in range(new_height):
                for j in range(new_width):
                    zoomed_image[i, j] = img[int(i / zoom_factor), int(j / zoom_factor)]

            return zoomed_image
        except Exception as e:
            print(f"Error in nearest_neighbor_zoom: {e}")
            return img

    def linear_zoom(self, img, zoom_factor):
        """Linear interpolation using cv2.resize with LINEAR interpolation."""
        try:
            height, width = img.shape
            new_height = int(height * zoom_factor)
            new_width = int(width * zoom_factor)

            # Use cv2.resize with LINEAR interpolation
            zoomed_image = cv2.resize(
                img,
                (new_width, new_height),
                interpolation=cv2.INTER_LINEAR
            )

            return zoomed_image

        except Exception as e:
            print(f"Error in linear_zoom: {e}")
            return img
        '''
        def cubic_interpolate(p0, p1, p2, p3, t):
            a = -0.5 * p0 + 1.5 * p1 - 1.5 * p2 + 0.5 * p3
            b = p0 - 2.5 * p1 + 2 * p2 - 0.5 * p3
            c = -0.5 * p0 + 0.5 * p2
            d = p1
            return a * t ** 3 + b * t ** 2 + c * t + d

        for i in range(new_height):
            for j in range(new_width):
                x = i / zoom_factor
                y = j / zoom_factor

                x1 = int(np.floor(x))
                y1 = int(np.floor(y))

                x0 = max(x1 - 1, 0)
                x2 = min(x1 + 1, height - 1)
                x3 = min(x1 + 2, height - 1)
                y0 = max(y1 - 1, 0)
                y2 = min(y1 + 1, width - 1)
                y3 = min(y1 + 2, width - 1)

                a = x - x1
                b = y - y1

                # Interpolate in x direction
                col0 = cubic_interpolate(
                    float(img[x0, y0]), float(img[x1, y0]),
                    float(img[x2, y0]), float(img[x3, y0]), a
                )
                col1 = cubic_interpolate(
                    float(img[x0, y1]), float(img[x1, y1]),
                    float(img[x2, y1]), float(img[x3, y1]), a
                )
                col2 = cubic_interpolate(
                    float(img[x0, y2]), float(img[x1, y2]),
                    float(img[x2, y2]), float(img[x3, y2]), a
                )
                col3 = cubic_interpolate(
                    float(img[x0, y3]), float(img[x1, y3]),
                    float(img[x2, y3]), float(img[x3, y3]), a
                )

                # Interpolate in y direction
                value = cubic_interpolate(col0, col1, col2, col3, b)
                zoomed_image[i, j] = np.clip(value, 0, 255)
                '''

    def bilinear_zoom(self, img, zoom_factor):
        """Using linear zoom as in original code."""
        return self.linear_zoom(img, zoom_factor)

    def cubic_zoom(self, img, zoom_factor):
        """Cubic interpolation using cv2.resize with CUBIC interpolation."""
        try:
            height, width = img.shape
            new_height = int(height * zoom_factor)
            new_width = int(width * zoom_factor)

            # Use cv2.resize with CUBIC interpolation
            zoomed_image = cv2.resize(
                img,
                (new_width, new_height),
                interpolation=cv2.INTER_CUBIC
            )

            return zoomed_image

        except Exception as e:
            print(f"Error in cubic_zoom: {e}")
            return img

    def add_noise(self):
        if self.input_image is not None:
            noise_type = QInputDialog.getItem(self, "Select Noise Type", "Choose noise type:",
                                              ["Gaussian", "Salt & Pepper", "Poisson"], 0, False)[0]

            # Check which images are available and show the result accordingly
            if self.output_image1 is None:
                if noise_type == "Gaussian":
                    noise = np.random.normal(0, 1, self.input_image.shape).astype(np.uint8)
                    noisy_image = cv2.add(self.input_image, noise)
                elif noise_type == "Salt & Pepper":
                    noisy_image = self.input_image.copy()
                    s_vs_p = 0.5
                    amount = 0.04
                    num_salt = np.ceil(amount * noisy_image.size * s_vs_p)
                    coords = [np.random.randint(0, i - 1, int(num_salt)) for i in noisy_image.shape]
                    noisy_image[coords[0], coords[1]] = 255
                    num_pepper = np.ceil(amount * noisy_image.size * (1. - s_vs_p))
                    coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in noisy_image.shape]
                    noisy_image[coords[0], coords[1]] = 0
                elif noise_type == "Poisson":
                    noisy_image = np.random.poisson(self.input_image).astype(np.uint8)
                # If only input image is available, show noisy image in output1
                self.output_image1 = noisy_image
                self.display_image(noisy_image, self.output_scene1)
            elif self.output_image1 is not None and self.output_image2 is None:
                self.history_output1.append(self.output_image1.copy())
                if noise_type == "Gaussian":
                    noise = np.random.normal(0, 1, self.output_image1.shape).astype(np.uint8)
                    noisy_image = cv2.add(self.output_image1, noise)
                elif noise_type == "Salt & Pepper":
                    noisy_image = self.output_image1.copy()
                    s_vs_p = 0.5
                    amount = 0.04
                    num_salt = np.ceil(amount * noisy_image.size * s_vs_p)
                    coords = [np.random.randint(0, i - 1, int(num_salt)) for i in noisy_image.shape]
                    noisy_image[coords[0], coords[1]] = 255
                    num_pepper = np.ceil(amount * noisy_image.size * (1. - s_vs_p))
                    coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in noisy_image.shape]
                    noisy_image[coords[0], coords[1]] = 0
                elif noise_type == "Poisson":
                    noisy_image = np.random.poisson(self.output_image1).astype(np.uint8)
                # If both input and output1 are available, show noisy image in output2
                self.output_image2 = noisy_image
                self.display_image(noisy_image, self.output_scene2)
            elif self.output_image1 is not None and self.output_image2 is not None:
                self.history_output2.append(self.output_image2.copy())
                if noise_type == "Gaussian":
                    noise = np.random.normal(0, 1, self.output_image2.shape).astype(np.uint8)
                    noisy_image = cv2.add(self.output_image2, noise)
                elif noise_type == "Salt & Pepper":
                    noisy_image = self.output_image2.copy()
                    s_vs_p = 0.5
                    amount = 0.04
                    num_salt = np.ceil(amount * noisy_image.size * s_vs_p)
                    coords = [np.random.randint(0, i - 1, int(num_salt)) for i in noisy_image.shape]
                    noisy_image[coords[0], coords[1]] = 255
                    num_pepper = np.ceil(amount * noisy_image.size * (1. - s_vs_p))
                    coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in noisy_image.shape]
                    noisy_image[coords[0], coords[1]] = 0
                elif noise_type == "Poisson":
                    noisy_image = np.random.poisson(self.output_image2).astype(np.uint8)
                # If all three images are available, apply noise to output2
                self.output_image2 = noisy_image
                self.display_image(noisy_image, self.output_scene2)

    def denoise(self):
        if self.output_image1 is not None:
            denoise_type = QInputDialog.getItem(self, "Select Denoise Type", "Choose denoise type:",
                                                ["Gaussian Blur", "Median Filter", "Bilateral Filter"], 0, False)[0]
            if denoise_type == "Gaussian Blur":
                denoised_image = cv2.GaussianBlur(self.output_image1, (5, 5), 0)
            elif denoise_type == "Median Filter":
                denoised_image = cv2.medianBlur(self.output_image1, 5)
            elif denoise_type == "Bilateral Filter":
                denoised_image = cv2.bilateralFilter(self.output_image1, 9, 75, 75)

            # Check which images are available and show the result accordingly
            if self.output_image2 is None:
                self.history_output1.append(self.output_image1.copy())
                # If only output1 is available, show denoised image in output2
                self.output_image2 = denoised_image
                self.display_image(denoised_image, self.output_scene2)
            else:
                self.history_output2.append(self.output_image2.copy())
                if denoise_type == "Gaussian Blur":
                    denoised_image = cv2.GaussianBlur(self.output_image2, (5, 5), 0)
                elif denoise_type == "Median Filter":
                    denoised_image = cv2.medianBlur(self.output_image2, 5)
                elif denoise_type == "Bilateral Filter":
                    denoised_image = cv2.bilateralFilter(self.output_image2, 9, 75, 75)
                # If both output1 and output2 are available, apply denoising to output2
                self.output_image2 = denoised_image
                self.display_image(denoised_image, self.output_scene2)

    def adjust_contrast(self):
        if self.input_image is not None:
            contrast_type = QInputDialog.getItem(self, "Select Contrast Adjustment", "Choose contrast adjustment:",
                                                 ["Histogram Equalization", "CLAHE", "Custom"], 0, False)[0]

            # Check which images are available and show the result accordingly
            if self.output_image1 is None:
                if contrast_type == "Histogram Equalization":
                    adjusted_image = cv2.equalizeHist(self.input_image)
                elif contrast_type == "CLAHE":
                    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
                    adjusted_image = clahe.apply(self.input_image)
                elif contrast_type == "Custom":
                    alpha, beta = 1.5, 0  # Contrast and brightness
                    adjusted_image = cv2.convertScaleAbs(self.input_image, alpha=alpha, beta=beta)
                # If only input image is available, show adjusted image in output1
                self.output_image1 = adjusted_image
                self.display_image(adjusted_image, self.output_scene1)
            elif self.output_image1 is not None and self.output_image2 is None:
                self.history_output1.append(self.output_image1.copy())
                if contrast_type == "Histogram Equalization":
                    adjusted_image = cv2.equalizeHist(self.output_image1)
                elif contrast_type == "CLAHE":
                    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
                    adjusted_image = clahe.apply(self.output_image1)
                elif contrast_type == "Custom":
                    alpha, beta = 1.5, 0  # Contrast and brightness
                    adjusted_image = cv2.convertScaleAbs(self.output_image1, alpha=alpha, beta=beta)
                # If both input and output1 are available, show adjusted image in output2
                self.output_image2 = adjusted_image
                self.display_image(adjusted_image, self.output_scene2)
            elif self.output_image1 is not None and self.output_image2 is not None:
                self.history_output2.append(self.output_image2.copy())
                if contrast_type == "Histogram Equalization":
                    adjusted_image = cv2.equalizeHist(self.output_image2)
                elif contrast_type == "CLAHE":
                    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
                    adjusted_image = clahe.apply(self.output_image2)
                elif contrast_type == "Custom":
                    alpha, beta = 1.5, 0  # Contrast and brightness
                    adjusted_image = cv2.convertScaleAbs(self.output_image2, alpha=alpha, beta=beta)
                # If all three images are available, apply contrast adjustment to output2
                self.output_image2 = adjusted_image
                self.display_image(adjusted_image, self.output_scene2)

    def show_histogram(self, img, title):
        """Display the histogram of the given image."""
        if img is not None:
            hist = cv2.calcHist([img], [0], None, [256], [0, 256])
            plt.figure()
            plt.title(title)
            plt.xlabel("Pixel Value")
            plt.ylabel("Frequency")
            plt.plot(hist)
            plt.xlim([0, 256])
            plt.show()
        else:
             QMessageBox.warning(self, "Warning", "No image to display histogram.")
