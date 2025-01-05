# DICOM Viewer
<p align="center">
<img src="https://raw.githubusercontent.com/abdullah-gamil05/ImageBasedAnatomy_Tasks/main/task5_Dicom_Viewer/results/gui.png" alt="GUI Overview" width="700">
</p>

## Overview
The **DICOM Viewer** is a professional-grade application designed to load, process, and visualize medical images in DICOM format. It supports 2D, M2D (multi-slice 2D), and 3D images, offering a modern GUI for interactive analysis and advanced features like anonymization and metadata review.

---

## Features

### Comprehensive Image Display
- **2D Images**: Sequential slices displayed as a video.
- **M2D Images**: Displayed as tiles for 3D exploration and video for multi-slice analysis.
- **3D Images**: Tile-based visualization for volumetric inspection.

### Interactive Tools
- Real-time zoom, pan, brightness, and contrast adjustments.

### Advanced Functionalities
- **Show Tiles**: Generate tiled views for M2D and 3D datasets.
- **Tag Search**: Search for specific DICOM tags and display their values.
- **Metadata Review**: View detailed patient, study, and image information.
- **Anonymization**: Remove sensitive patient data for research and sharing.

---

## Input and Output

### Input
- **File Type**: DICOM (`.dcm`) files.
- **Imaging Modalities**: CT, MRI, and other medical imaging formats.

### Output
- **Visualizations**: Videos of 2D slices, tiled views of M2D and 3D images.
- **Anonymized Files**: Securely anonymized DICOM files saved in the `data/output/` folder.

---

## Installation

### Prerequisites
- Python 3.7+
- Libraries: `pydicom`, `Pillow`, `Tkinter`, `numpy`

### Steps
1. Clone the repository:
   ```bash
   git clone <[repository_url](https://github.com/abdullah-gamil05/ImageBasedAnatomy_Tasks/new/main/task5_Dicom_Viewer)>
   cd task5_dicom_viewer
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## How It Works

1. **File Loading**: Use the "Load DICOM" button to browse and select `.dcm` files.
2. **Image Visualization**:
   - 2D slices are played as a video.
   - M2D and 3D data are displayed in tiled formats.
3. **Tag Search**: Input specific tag codes to retrieve metadata values.
4. **Anonymization**: Save anonymized DICOM files for secure sharing.

---

## Example Visualizations

### 1. 2D Sequential Slices
<img src="https://raw.githubusercontent.com/abdullah-gamil05/ImageBasedAnatomy_Tasks/main/task5_Dicom_Viewer/results/image1.png" alt="2D Slices" width="600">

### 2. M2D Tile Display

<img src="https://raw.githubusercontent.com/abdullah-gamil05/ImageBasedAnatomy_Tasks/main/task5_Dicom_Viewer/results/m2d_cine.gif" alt="M2D Cine" width="600">

### 3. 3D tiles 

<img src="https://raw.githubusercontent.com/abdullah-gamil05/ImageBasedAnatomy_Tasks/main/task5_Dicom_Viewer/results/3d_tiles_view.png" alt="M2D Tiles" width="600">

---

## Future Enhancements
- GPU-accelerated rendering for faster performance.
- AI-driven segmentation for automated region-of-interest detection.
- Web-based deployment for remote access.

---

## References
1. RadiAnt DICOM Viewer: [https://www.radiantviewer.com](https://www.radiantviewer.com)
2. MicroDicom Viewer: [https://www.microdicom.com](https://www.microdicom.com)
3. PyDicom Documentation: [https://pydicom.github.io](https://pydicom.github.io)

---

