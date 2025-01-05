# Medical Image Multi-Viewer Application

This project is a **Medical Image Multi-Viewer** tool designed to visualize medical images in **axial**, **coronal**, and **sagittal** planes. The application provides a user-friendly interface with features to manipulate image views, adjust brightness and contrast, and zoom into specific regions of interest. The tool supports medical image files in the **NIfTI format (.nii, .nii.gz)**.

---
 ![Loading Animation](https://raw.githubusercontent.com/abdullah-gamil05/ImageBasedAnatomy_Tasks/main/assets/Gif.gif)
## Features

- **Multi-Planar Viewing**:
  - Visualize medical images in axial, coronal, and sagittal planes.
 - Slice navigation using intuitive sliders.

- **Brightness and Contrast Adjustments**:
  - Fine-tune brightness and contrast for each view independently.

- **Zoom Functionality**:
  - Zoom into specific regions for detailed examination.

- **Reset View**:
  - Restore default settings for all views with a single click.

- **Interactive Point Selection**:
  - Select specific points in the images to highlight them across views.

- **NIfTI File Support**:
  - Load and visualize medical images in `.nii` or `.nii.gz` formats.

---

## Installation

### Prerequisites
- Python 3.8+
- Required libraries: 
  - PyQt5 (for GUI implementation)
  - matplotlib
  - SimpleITK
  - numpy
  - Pillow
    
 ### Clone the repository:

   ```bash
   git clone https://github.com/abdullah-gamil05/ImageBasedAnatomy_Tasks/task1_MPR.git
   ```

### Navigate to the project directory:

   ```bash
   cd task1_MPR
   ```


## Usage

### 1. Launch the Application
- Run the script `multi_viewer.py`.

### 2. Load a NIfTI File
- Click the **"Load NIfTI File"** button and select a `.nii` or `.nii.gz` file from your system.

### 3. Adjust Views
- Use the **sliders** to navigate through slices in each plane (axial, coronal, sagittal).
- Adjust **brightness** and **contrast** using dedicated sliders for each view.
- Use the **zoom slider** to magnify specific areas.

### 4. Reset the View
- Click the **"Reset View"** button to restore all settings to default.

### 5. Interactive Selection
- Click on a point in one view to highlight its corresponding position in the other views.

---

## Application Interface

### 1. Main Controls
- Buttons for loading files and resetting views.
- Sliders for navigating slices, adjusting brightness, contrast, and zoom.

### 2. Multi-Planar Views
- Axial, coronal, and sagittal views displayed side by side.
- Adjustable via individual control panels.

### 3. User-Friendly Design
- Intuitive layout with tooltips and easy-to-use sliders.

 ---
 
## Example Views

### **Axial View**
<img src="https://raw.githubusercontent.com/abdullah-gamil05/ImageBasedAnatomy_Tasks/main/task1_MPR/results/axial_view.png" alt="Axial View" width="400" height="300" />

### **Coronal View**
<img src="https://raw.githubusercontent.com/abdullah-gamil05/ImageBasedAnatomy_Tasks/main/task1_MPR/results/coronal_view.png" alt="Coronal View" width="400" height="300" />

### **Sagittal View**
<img src="https://raw.githubusercontent.com/abdullah-gamil05/ImageBasedAnatomy_Tasks/main/task1_MPR/results/sagittal_view.png" alt="Sagittal View" width="400" height="300" />


---

## Technical Details

1. **Main Components**:
   - **`MultiViewer` class**: Implements the core functionality of the viewer.
   - **Brightness and Contrast Adjustments**:
     - Image pixel values are normalized, adjusted, and clipped within the rang[0,255].
   - **Zoom Functionality**:
     - Controlled using a slider that dynamically adjusts the viewport dimensions.

2. **Dependencies**:
   - **PyQt5**: For building the graphical user interface.
   - **SimpleITK**: For handling medical image formats like NIfTI.
   - **matplotlib**: For rendering and displaying the medical images.
   - **numpy**: For efficient numerical operations on pixel data.

3. **Modularity**:
   - Separate utility functions for image adjustments, zoom, and data processing.

---

## Known Limitations

- Currently supports only `.nii` and `.nii.gz` file formats.
- Performance may decrease with very large datasets.
- 
---

## Future Enhancements

- Implement oblique plane reconstruction.
- Add support for real-time 3D rendering.
- Include tools for basic segmentation and annotation.

---

## Acknowledgements
- **Libraries**: SimpleITK, Matplotlib, PyQt5
- **Dataset**: Sample DICOM datasets from [Open Access Medical Imaging](https://www.openaccessimaging.org).
