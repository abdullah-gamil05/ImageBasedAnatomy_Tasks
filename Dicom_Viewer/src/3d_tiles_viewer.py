class Tile3DViewer:


    def __init__(self, dicom_files, master):
        self.master = master
        self.dicom_files = dicom_files
        self.pixel_array = None
        self.load_dicom_series()
        self.create_tile_window()

    def load_dicom_series(self):
        pixel_arrays = []

        for dicom_file in self.dicom_files:
            try:

                ds = pydicom.dcmread(dicom_file)
                if hasattr(ds, 'pixel_array'):
                    # Handle excess padding
                    pixel_data = ds.pixel_array
                    if pixel_data.ndim == 3 and pixel_data.shape[0] > 1:
                        # If the pixel data has excess padding, trim it
                        pixel_data = pixel_data[:pixel_data.shape[0] - 1]  # Adjust as necessary
                    pixel_arrays.append(pixel_data)
            except Exception as e:
                print(f"Error loading DICOM file {dicom_file}: {e}")
        # Stack the pixel arrays if they are 3D

        if pixel_arrays:
            self.pixel_array = np.concatenate(pixel_arrays, axis=0)  # Concatenate along the first axis

    def create_tile_window(self, rows=4, cols=5):
        # Calculate the size of the window based on the number of rows and columns
        tile_size = 80 # Size of each tile (in pixels)
        window_width = cols * (tile_size + 10)+50 # 10 pixels padding + 50 for scrollbar
        window_height = rows * (tile_size + 10)+50# 10 pixels padding + 50 for title bar

        self.tile_window = Toplevel(self.master)
        self.tile_window.title("3D DICOM Tiles")
        self.tile_window.geometry(f"{window_width}x{window_height}")

        canvas = Canvas(self.tile_window)
        scrollbar = Scrollbar(self.tile_window, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Add tiles for each DICOM file
        if self.pixel_array is not None:
            num_slices = self.pixel_array.shape[0]
            total_tiles = rows * cols  # Total number of tiles to display

            # Limit the number of slices to display
            for idx in range(min(num_slices, total_tiles)):
                try:
                    slice_image = self.pixel_array[idx]

                    # Check for supported shapes
                    if slice_image.ndim == 2:  # Grayscale image
                        slice_image = self.normalize_image(slice_image)
                    elif slice_image.ndim == 3:  # Multi-channel image
                        if slice_image.shape[0] in [1, 3]:  # Single channel or RGB
                            slice_image = np.squeeze(slice_image)  # Remove single-dimensional entries
                            if slice_image.ndim == 3:  # If still 3D, average across channels
                                slice_image = np.mean(slice_image, axis=0).astype(np.uint8)
                            slice_image = self.normalize_image(slice_image)
                        else:
                            # Handle unsupported shapes
                            if slice_image.shape[0] == 12:  # Shape (12, 224, 192)
                                slice_image = np.mean(slice_image, axis=0).astype(np.uint8)
                            elif slice_image.shape[0] == 21:  # Shape (21, 336, 336)
                                slice_image = np.mean(slice_image, axis=0).astype(np.uint8)
                            else:
                                print(f"Skipping slice {idx}: Unsupported pixel array shape {slice_image.shape}")
                                continue  # Skip unsupported shapes
                            slice_image = self.normalize_image(slice_image)
                    else:
                        print(f"Skipping slice {idx}: Unsupported pixel array shape {slice_image.shape}")
                        continue  # Skip unsupported shapes

                    image = Image.fromarray(slice_image)
                    image.thumbnail((tile_size, tile_size))  # Resize for display
                    img_tk = ImageTk.PhotoImage(image)

                    label = Label(scrollable_frame, image=img_tk)
                    label.image = img_tk  # Keep reference to avoid garbage collection
                    label.grid(row=idx // cols, column=idx % cols, padx=5, pady=5, sticky="nsew")
                except Exception as e:
                    print(f"Error displaying slice {idx}: {e}")

            # Configure grid weights to center the grid
            for r in range(rows):
                scrollable_frame.grid_rowconfigure(r, weight=1)
            for c in range(cols):
                scrollable_frame.grid_columnconfigure(c, weight=1)
                # Adjust the grid to fit the window
            #scrollable_frame.pack(fill="both", expand=True)

    def normalize_image(self, image):

        # Normalize the image to the range [0, 255]
        image_min = np.min(image)
        image_max = np.max(image)
        if image_max > image_min:

            normalized_image = (image - image_min) / (image_max - image_min) * 255
            return normalized_image.astype(np.uint8)

        return image.astype(np.uint8)
