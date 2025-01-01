import os
import pydicom
import numpy as np
import random
import string
import warnings
import threading
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
from tkinter import Tk, Label, StringVar, filedialog, Entry, Button, Canvas, Frame, Scrollbar, Toplevel, Listbox, END, ttk, Scale, messagebox

# Suppress warnings from pydicom about invalid VR values
warnings.filterwarnings("ignore", category=UserWarning, module='pydicom.valuerep')


# Mapping of DICOM tags to readable names
DICOM_TAGS = {
    "0010,1000": "Other Patient IDs",
    "0010,1001": "Other Patient Names",
    "0010,2160": "Ethnic Group",
    "0010,4000": "Patient Comments",
    "0020,000D": "Study Instance UID",
    "0020,000E": "Series Instance UID",
    "0020,0052": "Frame Reference UID",
    "0020,1040": "Position Reference Indicator",
    "0028,0002": "Samples Per Pixel",
    "0028,0004": "Photometric Interpretation",
    "0028,0100": "Bits Allocated",
    "0028,0101": "Bits Stored",
    "0028,0102": "High Bit",
    "0028,0103": "Pixel Representation",
    "0028,1050": "Window Center",
    "0028,1051": "Window Width",
    "0028,1052": "Rescale Intercept",
    "0028,1053": "Rescale Slope",
    "0028,2110": "Lossy Image Compression",
    "7FE0,0010": "Pixel Data",
    "0008,0000": "Group Length",
    "0008,0005": "Specific Character Set",
    "0008,0008": "Image Type",
    "0008,0013": "Instance Creation Time",
    "0008,0016": "SOP Class UID",
    "0008,0018": "SOP Instance UID",
    "0008,0020": "Study Date",
    "0008,0021": "Series Date",
    "0008,0022": "Acquisition Date",
    "0008,0023": "Content Date",
    "0008,1030": "Study Description",
    "0008,103E": "Series Description",
    "0008,1060": "Physician Reading Study",
    "0008,1070": "Operator Name",
    "0008,1090": "Manufacturer Model Name",
    "0008,1140": "Referenced Image Sequence",
    "0010,0000": "Group Length",
    "0010,0010": "Patient Name",
    "0010,0020": "Patient ID",
    "0010,0040": "Patient Sex",
    "0010,1010": "Patient Age",
    "0010,1020": "Patient Size",
    "0010,1030": "Patient Weight",
    "0018,0000": "Group Length",
    "0018,0015": "Body Part Examined",
    "0018,0020": "Scanning Sequence",
    "0018,0021": "Sequence Variant",
    "0018,0022": "Scan Options",
    "0018,0023": "MR Acquisition Type",
    "0008,0023": "Content Date",
    "0008,0030": "Study Time",
    "0008,0031": "Series Time",
    "0008,0032": "Acquisition Time",
    "0008,0033": "Content Time",
    "0008,0060": "Modality",
    "0008,0070": "Manufacturer",
    "0008,0080": "Institution Name",
    "0008,0090": "Referring Physician",
    "0008,1010": "Station Name",
    "0008,1040": "Institution Department Name",
    "0008,1050": "Performing Physician",
    "0008,1060": "Physician Reading Study",
    "0010,1000": "Other Patient IDs",
    "0010,2160": "Ethnic Group",
    "0010,4000": "Patient Comments",
    "0018,0080": "Repetition Time",
    "0018,0081": "Echo Time",
    "0018,0082": "Inversion Time",
    "0018,0083": "Number of Averages",
    "0018,0084": "Imaging Frequency",
    "0018,0085": "Imaged Nucleus",
    "0018,0086": "Echo Numbers"
}


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


class DICOMViewer:
    def __init__(self, master):
        self.master = master
        self.master.title("DICOM Viewer")
        self.master.geometry("1280x720")  # Increased width for sliders
        self.master.configure(bg="#1e1e1e")  # Dark background color

        self.selected_patient = StringVar()
        self.patient_data = {}
        self.current_image_index = 0
        self.video_running = False
        self.current_pixel_array = None  # To store pixel array for 3D/4D images
        self.cached_tags = {}  # Cache for tags
        self.current_image = None  # To store the currently displayed image

        self.create_widgets()

    def create_widgets(self):
        # Frame for controls
        control_frame = Frame(self.master, bg="#2e2e2e")
        control_frame.pack(side='top', fill='x', padx=10, pady=10)

        # Updated button colors and styles with smaller padding
        button_style = {'bg': "#007ACC", 'fg': "white", 'relief': 'flat', 'font': ("Arial", 9), 'padx': 5, 'pady': 3}

        Button(control_frame, text="Browse", command=self.browse_folder, **button_style).pack(side='left', padx=2,
                                                                                              pady=2)

        self.anonymize_entry = Entry(control_frame, width=20, bg="#3e3e3e", fg="white")
        self.anonymize_entry.pack(side='left', padx=5, pady=2)

        Button(control_frame, text="Anonymize Selected Patient", command=self.anonymize, **button_style).pack(
            side='left', padx=2, pady=2)
        Button(control_frame, text="Anonymize All Patients", command=self.anonymize_all, **button_style).pack(
            side='left', padx=2, pady=2)
        Button(control_frame, text="View All Tags", command=self.view_all_tags, **button_style).pack(side='left',
                                                                                                     padx=2, pady=2)
        Button(control_frame, text="Reset All Views", command=self.reset_viewer, **button_style).pack(side='left',
                                                                                                      padx=2, pady=2)

        # New buttons for exploring DICOM elements
        Button(control_frame, text="Patient Info", command=self.show_patient_info, **button_style).pack(side='left',
                                                                                                        padx=2, pady=2)
        Button(control_frame, text="Study Info", command=self.show_study_info, **button_style).pack(side='left', padx=2,
                                                                                                    pady=2)
        Button(control_frame, text="Modality Info", command=self.show_modality_info, **button_style).pack(side='left',
                                                                                                          padx=2,
                                                                                                          pady=2)
        Button(control_frame, text="Physician Info", command=self.show_physician_info, **button_style).pack(side='left',
                                                                                                            padx=2,
                                                                                                            pady=2)
        Button(control_frame, text="Image Info", command=self.show_image_info, **button_style).pack(side='left', padx=2,
                                                                                                    pady=2)

        self.anonymize_status_label = Label(control_frame, text="", bg="#2e2e2e", fg="white")
        self.anonymize_status_label.pack(side='left', padx=5, pady=2)

        self.search_entry = Entry(control_frame, width=20, bg="#3e3e3e", fg="white")
        self.search_entry.pack(side='left', padx=5, pady=2)

        Button(control_frame, text="Search Tag", command=self.search_tag, **button_style).pack(side='left', padx=2,
                                                                                               pady=2)

        # Add Show Tiles button
        Button(control_frame, text="Show Tiles", command=self.show_tiles, **button_style).pack(side='left', padx=2, pady=2)
        self.search_result_label = Label(control_frame, text="", bg="#2e2e2e", fg="white")
        self.search_result_label.pack(side='bottom', padx=5, pady=2)

        # Frame for patient list
        self.patient_frame = Frame(self.master, bg="#1e1e1e")
        self.patient_frame.pack(side='left', padx=10, fill='y')

        # Listbox for patient selection
        self.patient_listbox = Listbox(self.patient_frame, bg="#3e3e3e", fg="white", font=("Arial", 10),
                                       selectmode='single')
        self.patient_listbox.pack(side='left', fill='both', expand=True)

        # Scrollbar for the patient list
        self.patient_scrollbar = Scrollbar(self.patient_frame, command=self.patient_listbox.yview, bg="#2e2e2e",
                                           troughcolor="#2e2e2e")
        self.patient_scrollbar.pack(side='right', fill='y')
        self.patient_listbox.config(yscrollcommand=self.patient_scrollbar.set)

        self.patient_info_label = Label(self.master, text="", bg="#1e1e1e", fg="white", font=("Arial", 12))
        self.patient_info_label.pack(pady=10)

        # Frame for sliders
        self.slider_frame = Frame(self.master, bg="#1e1e1e")
        self.slider_frame.pack(side='right', padx=10, pady=0)

        # Sliders for brightness, contrast, and zoom
        self.brightness_slider = Scale(self.slider_frame, from_=0, to=2, resolution=0.1, orient='horizontal',
                                       label='Brightness', bg="#3e3e3e", fg="white", command=self.update_image)
        self.brightness_slider.set(1)  # Default value
        self.brightness_slider.pack(pady=5)

        self.contrast_slider = Scale(self.slider_frame, from_=0, to=2, resolution=0.1, orient='horizontal',
                                     label='Contrast', bg="#3e3e3e", fg="white", command=self.update_image)
        self.contrast_slider.set(1)  # Default value
        self.contrast_slider.pack(pady=5)

        self.zoom_slider = Scale(self.slider_frame, from_=1, to=3, resolution=0.1, orient='horizontal', label='Zoom',
                                 bg="#3e3e3e", fg="white", command=self.update_image)
        self.zoom_slider.set(1)  # Default value
        self.zoom_slider.pack(pady=5)

        # Frame for image/video display
        self.display_frame = Frame(self.master, bg="#1e1e1e", width=640, height=480)
        self.display_frame.pack(side='top', pady=10)

        # Specialized canvas for images and videos
        self.display_canvas = Canvas(self.display_frame, width=640, height=480, bg="#3e3e3e")
        self.display_canvas.pack()

        # Button to fit and rescale the image/video
        self.fit_button = Button(self.display_frame, text="Fit to Window", command=self.fit_to_window, bg="#2196F3",
                                 fg="white", relief='flat')
        self.fit_button.pack(pady=5)

        # Status bar
        self.status_bar = Label(self.master, text="Welcome to DICOM Viewer", bg="#1e1e1e", fg="white",
                                font=("Arial", 20))
        self.status_bar.pack(side='top', fill='x')

        # Navigation buttons for 3D/4D images
        nav_frame = Frame(self.master, bg="#2e2e2e")
        nav_frame.pack(side='bottom', fill='x', padx=10, pady=10)

        # Bind the selection event to update patient info
        self.patient_listbox.bind('<<ListboxSelect>>', self.on_patient_select)

    def show_tiles(self):
        if self.selected_patient.get() in self.patient_data:
            dicom_files = self.patient_data[self.selected_patient.get()]['dicom_files']
            Tile3DViewer(dicom_files, self.master)
        else:
            messagebox.showerror("Error", "No patient selected or no 3D DICOM files available.")

    def update_image(self, event=None):
        if self.current_image:
            # Get current slider values
            brightness_factor = self.brightness_slider.get()
            contrast_factor = self.contrast_slider.get()
            zoom_factor = self.zoom_slider.get()

            # Adjust brightness
            enhancer = ImageEnhance.Brightness(self.current_image)
            bright_image = enhancer.enhance(brightness_factor)

            # Adjust contrast
            enhancer = ImageEnhance.Contrast(bright_image)
            contrast_image = enhancer.enhance(contrast_factor)

            # Resize for zoom
            img_width, img_height = contrast_image.size
            new_width = int(img_width * zoom_factor)
            new_height = int(img_height * zoom_factor)
            final_image = contrast_image.resize((new_width, new_height), Image.LANCZOS)

            self.display_image(final_image)

    def normalize_image(self, pixel_array):
        # Normalize the pixel values to the range [0, 255]
        pixel_array = pixel_array.astype(np.float32)
        pixel_array -= np.min(pixel_array)
        pixel_array /= np.max(pixel_array)
        pixel_array *= 255
        return pixel_array.astype(np.uint8)

    def enhance_image(self, image):
        # Apply histogram equalization
        image = Image.fromarray(image)
        image = image.convert("L")  # Convert to grayscale
        image = ImageEnhance.Contrast(image).enhance(2)  # Increase contrast
        image = image.filter(ImageFilter.SHARPEN)  # Sharpen the image
        return image

    def show_image(self, dicom_path):
        try:
            ds = pydicom.dcmread(dicom_path, force=True)  # Force reading the file
            pixel_array = ds.pixel_array

            pixel_array = np.squeeze(pixel_array)

            if pixel_array.ndim == 2:  # Grayscale image
                normalized_array = self.normalize_image(pixel_array)
                enhanced_image = self.enhance_image(normalized_array)
                self.current_image = enhanced_image
                self.display_image(enhanced_image)
            elif pixel_array.ndim == 3:  # Color image (RGB)
                if pixel_array.shape[2] == 3:  # RGB
                    normalized_array = self.normalize_image(pixel_array)
                    enhanced_image = self.enhance_image(normalized_array)
                    self.current_image = enhanced_image
                    self.display_image(enhanced_image)
                elif pixel_array.shape[2] == 4:  # RGBA
                    normalized_array = self.normalize_image(pixel_array)
                    enhanced_image = self.enhance_image(normalized_array)
                    self.current_image = enhanced_image
                    self.display_image(enhanced_image)
            elif pixel_array.ndim == 4:  # 4D image (e.g., time series)
                self.current_pixel_array = pixel_array  # Store pixel array for navigation
                self.current_image_index = 0  # Start at the first frame
                self.play_video(self.current_pixel_array)  # Start video playback
            else:
                raise ValueError(f"Unsupported image shape: {pixel_array.shape}")

        except Exception as e:
            print(f"Error displaying image: {e}")

    def display_image(self, image):
        img_tk = ImageTk.PhotoImage(image)
        self.display_canvas.create_image((self.display_canvas.winfo_width() // 2, self.display_canvas.winfo_height() // 2), anchor='center', image=img_tk)
        self.display_canvas.image = img_tk

    def fit_to_window(self):
        if self.current_image:
            # Get the current image size
            img_width, img_height = self.current_image.size
            # Calculate the scaling factor
            scale_x = self.display_canvas.winfo_width() / img_width
            scale_y = self.display_canvas.winfo_height() / img_height
            scale = min(scale_x, scale_y)

            # Resize the image
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            resized_image = self.current_image.resize((new_width, new_height), Image.LANCZOS)
            self.display_image(resized_image)

    def browse_folder(self):
        folder = filedialog.askdirectory(title="Select Dataset Folder")
        if folder:
            threading.Thread(target=self.load_patient_data, args=(folder,), daemon=True).start()

    def load_patient_data(self, folder):
        self.patient_data = {}
        self.clear_previous_views()

        for root_dir, _, files in os.walk(folder):
            for file in files:
                if file.endswith(".dcm"):
                    dicom_path = os.path.join(root_dir, file)
                    try:
                        ds = pydicom.dcmread(dicom_path, force=True)  # Force reading the file
                        patient_id = ds.get("PatientID", "Unknown").strip()

                        if patient_id not in self.patient_data:
                            self.patient_data[patient_id] = {"metadata": {}, "dicom_files": []}

                        # Store metadata in a dictionary
                        self.patient_data[patient_id]["metadata"] = {
                            "Patient ID": patient_id,
                            "Patient Name": str(ds.get("PatientName", "Unknown")),  # Convert to string
                            "Patient Sex": str(ds.get("PatientSex", "Unknown")),
                            "Patient Age": str(ds.get("PatientAge", "Unknown")),
                            "Modality": str(ds.get("Modality", "Unknown")),
                            "Study Description": str(ds.get("StudyDescription", "Unknown")),
                            "Series Description": str(ds.get("SeriesDescription", "Unknown")),
                            "Manufacturer ": str(ds.get("Manufacturer", "Unknown")),
                            "Referring Physician": str(ds.get("ReferringPhysicianName", "Unknown")),
                            "Study Date": str(ds.get("StudyDate", "Unknown")),
                            "Study Time": str(ds.get("StudyTime", "Unknown")),
                            "Study ID": str(ds.get("StudyID", "Unknown")),
                            "Image Position": str(ds.get("ImagePositionPatient", "Unknown")),
                            "Image Orientation": str(ds.get("ImageOrientationPatient", "Unknown")),
                            "Pixel Spacing": str(ds.get("PixelSpacing", "Unknown")),
                        }
                        self.patient_data[patient_id]["dicom_files"].append(dicom_path)
                    except Exception as e:
                        print(f"Error processing file {file}: {e}")



        print(f"Loaded patient data: {self.patient_data}")  # Debugging line

        if self.patient_data:
            self.update_patient_menu()
            self.brightness_slider.config(state='normal')
            self.contrast_slider.config(state='normal')
            self.zoom_slider.config(state='normal')
        else:
            print("No patients found in the selected folder.")  # Debugging line

    def clear_previous_views(self):
        self.display_canvas.delete("all")
        self.current_pixel_array = None  # Reset current pixel array
        self.patient_listbox.delete(0, END)  # Clear the patient listbox

    def update_patient_menu(self):
        # Clear previous patient entries in the listbox
        self.patient_listbox.delete(0, END)

        patient_ids = list(self.patient_data.keys())
        if patient_ids:
            for pid in patient_ids:
                self.patient_listbox.insert(END, pid)  # Add patient ID to the listbox

            self.display_patient_info(patient_ids[0])  # Display info for the first patient

    def on_patient_select(self, event):
        selected_index = self.patient_listbox.curselection()
        if selected_index:
            patient_id = self.patient_listbox.get(selected_index)
            self.select_patient(patient_id)

    def select_patient(self, patient_id):
        self.selected_patient.set(patient_id)  # Update the selected patient
        self.display_patient_info(patient_id)  # Display the patient's info

    def display_patient_info(self, patient_id):
        if patient_id in self.patient_data:
            metadata = self.patient_data[patient_id]["metadata"]  # Access the metadata dictionary
            dicom_files = self.patient_data[patient_id]["dicom_files"]

            if dicom_files:
                self.current_image_index = 0
                self.show_image(dicom_files[self.current_image_index])
        else:
            self.patient_info_label.config(text="No patient information available.")

    def play_video(self, pixel_array):
        self.video_running = True
        self.current_frame_index = 0
        self.video_pixel_array = pixel_array
        self.update_video_frame()

    def update_video_frame(self):
        if self.video_running and self.video_pixel_array is not None:
            frame = self.video_pixel_array[self.current_frame_index]
            frame_image = Image.fromarray(frame).convert("L")
            img_tk = ImageTk.PhotoImage(frame_image)
            self.display_canvas.create_image((self.display_canvas.winfo_width() // 2, self.display_canvas.winfo_height() // 2), anchor='center', image=img_tk)
            self.display_canvas.image = img_tk

            self.current_frame_index = (self.current_frame_index + 1) % self.video_pixel_array.shape[0]
            self.master.after(100, self.update_video_frame)  # Adjust timing as needed

    def generate_random_value(self, prefix, length=8):
        """Generate a random string starting with the given prefix."""
        random_suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        return f"{prefix}_{random_suffix}"

    def anonymize(self):
        patient_id = self.selected_patient.get()
        prefix = self.anonymize_entry.get().strip()

        if not patient_id:
            self.anonymize_status_label.config(text="Please select a patient.")
            return

        if not prefix:
            self.anonymize_status_label.config(text="Please enter a prefix for anonymization.")
            return

        dicom_files = self.patient_data[patient_id]["dicom_files"]
        anonymized_folder = os.path.join(os.path.dirname(dicom_files[0]), "anonymized")
        os.makedirs(anonymized_folder, exist_ok=True)

        new_patient_id = self.generate_random_value(prefix)

        try:
            for dicom_path in dicom_files:
                ds = pydicom.dcmread(dicom_path, force=True)
                ds.PatientID = new_patient_id
                ds.PatientName = new_patient_id
                ds.PatientSex = new_patient_id
                ds.PatientAge = new_patient_id
                new_dicom_path = os.path.join(anonymized_folder, os.path.basename(dicom_path))
                ds.save_as(new_dicom_path)

            for metadata in self.patient_data[patient_id]["metadata"]:
                metadata["Patient ID"] = new_patient_id
                metadata["Patient Name"] = new_patient_id
                metadata["Patient Sex"] = new_patient_id
                metadata["Patient Age"] = new_patient_id

            self.patient_data[new_patient_id] = self.patient_data.pop(patient_id)
            self.selected_patient.set(new_patient_id)
            self.anonymize_status_label.config(text="Anonymized successfully.")
            self.update_patient_menu()
            self.display_patient_info(new_patient_id)

        except Exception as e:
            print(f"Error during anonymization: {e}")
            self.anonymize_status_label.config(text="Anonymized successfully.")

    def anonymize_all(self):
        prefix = self.anonymize_entry.get().strip()
        if prefix:
            if not self.patient_data:
                self.anonymize_status_label.config(text="No patient data available.")
                return

            first_patient_dicom_path = self.patient_data[next(iter(self.patient_data))]["dicom_files"][0]
            anonymized_folder = os.path.join(os.path.dirname(first_patient_dicom_path), "anonymized")
            os.makedirs(anonymized_folder, exist_ok=True)

            new_patient_data = {}
            for patient_id in list(self.patient_data.keys()):
                new_patient_id = self.generate_random_value(prefix)
                dicom_files = self.patient_data[patient_id]["dicom_files"]

                for dicom_path in dicom_files:
                    try:
                        ds = pydicom.dcmread(dicom_path, force=True)
                        ds.PatientID = new_patient_id
                        ds.PatientName = new_patient_id
                        ds.PatientSex = new_patient_id
                        ds.PatientAge = new_patient_id
                        new_dicom_path = os.path.join(anonymized_folder, os.path.basename(dicom_path))
                        ds.save_as(new_dicom_path)
                    except Exception as e:
                        print(f"Error saving anonymized file {dicom_path}: {e}")

                new_patient_data[new_patient_id] = self.patient_data[patient_id]
                new_patient_data[new_patient_id]["metadata"]["Patient ID"] = new_patient_id
                new_patient_data[new_patient_id]["metadata"]["Patient Name"] = new_patient_id
                new_patient_data[new_patient_id]["metadata"]["Patient Sex"] = new_patient_id
                new_patient_data[new_patient_id]["metadata"]["Patient Age"] = new_patient_id

            self.patient_data = new_patient_data
            self.anonymize_status_label.config(text="Anonymized successfully.")
            self.update_patient_menu()
        else:
            self.anonymize_status_label.config(text="Please enter a prefix for anonymization.")

    def search_tag(self):
        tag_input = self.search_entry.get().strip()
        print(f"Searching for tag: {tag_input}")  # Debugging line
        if tag_input:
            try:
                patient_id = self.selected_patient.get()
                if not patient_id:
                    self.search_result_label.config(text="Please select a patient.")
                    return

                dicom_files = self.patient_data[patient_id]["dicom_files"]
                results = []

                # Check if the input is in the format (0000,0000)
                if tag_input.startswith("(") and tag_input.endswith(")"):
                    tag_input = tag_input[1:-1].strip()  # Remove parentheses
                    group, element = tag_input.split(",")
                    group = int(group.strip(), 16)  # Convert to integer from hex
                    element = int(element.strip(), 16)  # Convert to integer from hex
                    tag = pydicom.tag.Tag((group, element))
                    print(f"Parsed tag: {tag}")  # Debugging line
                else:
                    self.search_result_label.config(text="Invalid tag format. Use (0000,0000).")
                    return

                for dicom_path in dicom_files:
                    ds = pydicom.dcmread(dicom_path, force=True)
                    if tag in ds:
                        # Use the tag's name safely
                        tag_name = DICOM_TAGS.get(tag, "Unknown Tag")  # Use a default value if tag is not found
                        results.append(f"{patient_id}: {tag_name}: {ds[tag]}")
                        print(f"Found tag in {dicom_path}: {tag_name}: {ds[tag]}")  # Debugging line

                self.show_search_results(results)
            except Exception as e:
                print(f"Error during search: {e}")  # Debugging line
                self.search_result_label.config(text=str(e))
        else:
            self.search_result_label.config(text="Please enter a tag to search.")


    def show_search_results(self, results):
        results_window = Toplevel(self.master)
        results_window.title("Search Results")
        results_window.configure(bg="#f0f0f0")

        results_tree = ttk.Treeview(results_window, columns=("Patient ID", "Tag", "Value"), show='headings')
        results_tree.heading("Patient ID", text="Patient ID")
        results_tree.heading("Tag", text="Tag")
        results_tree.heading("Value", text="Value")
        results_tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)

        scrollbar = Scrollbar(results_window, command= results_tree.yview)
        scrollbar.pack(side='right', fill='y')
        results_tree.config(yscrollcommand=scrollbar.set)

        # Insert unique results into the treeview
        unique_results = set(results)
        for result in unique_results:
            patient_id, tag, value = result.split(": ", 2)
            results_tree.insert("", "end", values=(patient_id, tag, value))

        if not unique_results:
            results_tree.insert("", "end", values=("No results found.", "", ""))


    def view_all_tags(self):
        patient_id = self.selected_patient.get()
        if not patient_id:
            print("No patient selected.")
            return

        if patient_id in self.cached_tags:
            self.display_tags(self.cached_tags[patient_id])
            return

        dicom_files = self.patient_data[patient_id]["dicom_files"]
        if not dicom_files:
            print("No DICOM files found for this patient.")
            return

        tags_window = Toplevel(self.master)
        tags_window.title(f"Tags for {patient_id}")
        tags_window.configure(bg="#f0f0f0")

        # Create a Treeview with an additional "Name" column
        tags_tree = ttk.Treeview(tags_window, columns=("Name", "Tag", "Value"), show='headings')
        tags_tree.heading("Name", text="Name")
        tags_tree.heading("Tag", text="Tag")
        tags_tree.heading("Value", text="Value")
        tags_tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)

        scrollbar = Scrollbar(tags_window, command=tags_tree.yview)
        scrollbar.pack(side='right', fill='y')
        tags_tree.config(yscrollcommand=scrollbar.set)

        all_tags = {}
        for dicom_path in dicom_files:
            try:
                ds = pydicom.dcmread(dicom_path, force=True)
                for elem in ds:
                    all_tags[elem.tag] = elem.value
            except Exception as e:
                print(f"Error reading {dicom_path}: {e}")

        self.cached_tags[patient_id] = all_tags
        self.display_tags(all_tags, tags_tree)

    def display_tags(self, all_tags, tags_tree):
        if not all_tags:
            tags_tree.insert("", "end", values=("No tags found.", "", ""))
        else:
            for tag, value in all_tags.items():
                # Convert the tag from a BaseTag object to the string format "0000,0000"
                tag_str = f"{tag.group:04X},{tag.element:04X}"
                # Get the readable name from the DICOM_TAGS dictionary
                tag_name = DICOM_TAGS.get(tag_str, f"Unknown Tag ({tag_str})")  # Default if not found
                # Insert the tag name, tag, and value into the tree
                tags_tree.insert("", "end", values=(tag_name, tag_str, str(value)))


    def reset_viewer(self):
        self.clear_previous_views()
        self.patient_data = {}
        self.selected_patient.set('')
        self.patient_listbox.delete(0, END)  # Clear the patient listbox
        self.patient_info_label.config(text="")
        self.anonymize_entry.delete(0, 'end')
        self.current_image_index = 0
        self.anonymize_status_label.config(text="")
        self.search_entry.delete(0, 'end')
        self.search_result_label.config(text="")
        self.video_running = False
        self.display_canvas.delete("all")
        self.cached_tags.clear()  # Clear the cached tags on reset
        self.status_bar.config(text="Viewer reset. Please load a dataset.")

    def show_patient_info(self):
        if self.selected_patient.get() in self.patient_data:
            patient_info = self.patient_data[self.selected_patient.get()]["metadata"]
            info_message = f"Patient Name: {patient_info.get('Patient Name', 'N/A')}\n" \
                           f"Patient ID: {patient_info.get('Patient ID', 'N/A')}\n" \
                           f"Patient Age: {patient_info.get('Patient Age', 'N/A')}\n" \
                           f"Patient Sex: {patient_info.get('Patient Sex', 'N/A')}"
            messagebox.showinfo("Patient Information", info_message)
        else:
            messagebox.showwarning("Warning", "No patient selected.")

    def show_study_info(self):
        if self.selected_patient.get() in self.patient_data:
            study_info = self.patient_data[self.selected_patient.get()]["metadata"]
            info_message = f"Study Date: {study_info.get('Study Date', 'N/A')}\n" \
                           f"Study Time: {study_info.get('Study Time', 'N/A')}\n" \
                           f"Study Description: {study_info.get('Study Description', 'N/A')}\n" \
                           f"Study ID: {study_info.get('Study ID', 'N/A')}"
            messagebox.showinfo("Study Information", info_message)
        else:
            messagebox.showwarning("Warning", "No patient selected.")

    def show_modality_info(self):
        if self.selected_patient.get() in self.patient_data:
            modality_info = self.patient_data[self.selected_patient.get()]["metadata"]
            info_message = f"Modality: {modality_info.get('Modality', 'N/A')}"
            messagebox.showinfo("Modality Information", info_message)
        else:
            messagebox.showwarning("Warning", "No patient selected.")

    def show_physician_info(self):
        if self.selected_patient.get() in self.patient_data:
            physician_info = self.patient_data[self.selected_patient.get()]["metadata"]
            info_message = f"Referring Physician: {physician_info.get('Referring Physician', 'N/A')}"
            messagebox.showinfo("Physician Information", info_message)
        else:
            messagebox.showwarning("Warning", "No patient selected.")

    def show_image_info(self):
        if self.selected_patient.get() in self.patient_data:
            image_info = self.patient_data[self.selected_patient.get()]["metadata"]
            info_message = f"Image Position: {image_info.get('Image Position', 'N/A')}\n" \
                           f"Image Orientation: {image_info.get('Image Orientation', 'N/A')}\n" \
                           f"Pixel Spacing: {image_info.get('Pixel Spacing', 'N/A')}"
            messagebox.showinfo("Image Information", info_message)
        else:
            messagebox.showwarning("Warning", "No patient selected.")

# Main application code to run the DICOMViewer
if __name__ == "__main__":
    root = Tk()
    viewer = DICOMViewer(root)
    root.mainloop()