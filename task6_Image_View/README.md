# Image Viewer

## Overview
The Pro Image Viewer is a Python-based tool for visualizing, processing, and analyzing images. It provides a graphical user interface (GUI) built using PyQt5 and offers advanced image manipulation features powered by OpenCV.
---

## Purpose
This tool is designed for:
- **Medical Imaging Analysis**: Ideal for evaluating medical image quality.
- **Educational Purposes**: A learning aid in image processing and analysis.
- **Research and Presentation**: Facilitates image enhancements for professional and research use.

---

## Features

1. **Image Loading**:
   - **Supported Formats**: PNG, JPEG, BMP, GIF.
   - **Description**: Simple file browser for importing images.

2. **Zooming**:
   - **Interpolation Methods**: Nearest Neighbor, Linear, Bilinear, Cubic.
   - **Use Case**: Detailed inspection of image regions.

3. **Brightness and Contrast Adjustment**:
   - **Interactive Sliders**: Real-time control for fine-tuning brightness and contrast.
   - **Implementation**: Uses OpenCV's `convertScaleAbs` function.

4. **Filters**:
   - **Lowpass Filter**: Reduces noise with Gaussian Blur.
   - **Highpass Filter**: Enhances edges using kernel-based convolution.

5. **Noise Addition**:
   - **Types**: Gaussian, Salt & Pepper, Poisson.
   - **Use Case**: Simulate real-world conditions and test denoising algorithms.

6. **Denoising**:
   - **Methods**: Gaussian Blur, Median Filter, Bilateral Filter.
   - **Purpose**: Remove noise while preserving image details.

7. **Histogram Visualization**:
   - **Feature**: Displays pixel intensity distribution for input and processed images.

8. **Signal-to-Noise Ratio (SNR) and Contrast-to-Noise Ratio (CNR)**:
   - **Feature**: Analyze image quality with user-selected Regions of Interest (ROIs).

9. **Undo and Reset**:
   - **Undo**: Reverts the last processing step.
   - **Reset**: Restores the image to its original state.

---

## Code Structure

### Main Classes
1. **ImageViewer**:
   - Core logic for image loading, visualization, and processing.
   - **Key Methods**:
     - `load_image`: Load and display images.
     - `add_noise`, `denoise`: Add/remove noise.
     - `apply_lowpass_filter`, `apply_highpass_filter`: Smooth or sharpen images.
     - `zoom_in`, `zoom_out`: Image scaling with interpolation.

2. **SNRCalculator**:
   - Tools for selecting ROIs and calculating SNR/CNR.
   - **Key Methods**:
     - `calculate_snr`: Computes SNR.
     - `calculate_cnr`: Computes CNR using three ROIs.
     - `reset_ROIs`: Clears ROI selections.

---

## Concepts Behind the Implementation
- **Interpolation**: Improves zoom quality.
  - **Nearest Neighbor**: Fast, lower quality.
  - **Cubic**: High-quality, smooth results.
- **Noise Models**:
  - **Gaussian Noise**: Mimics sensor inaccuracies.
  - **Salt & Pepper Noise**: Simulates impulsive disturbances.
- **Histogram Equalization**:
  - Enhances contrast by redistributing pixel intensities.
  - **CLAHE** prevents over-amplification.
- **Image Filtering**:
  - **Lowpass**: Suppresses noise.
  - **Highpass**: Enhances details and edges.

---

## Technical References
- [OpenCV Documentation](https://docs.opencv.org/)
- [PyQt5 Official Documentation](https://riverbankcomputing.com/software/pyqt/intro)
- [Matplotlib Documentation](https://matplotlib.org/stable/contents.html)

---

## Usage Instructions
1. Clone the repository and ensure all dependencies are installed:
   ```bash
   git clone <[repository_link](https://github.com/abdullah-gamil05/ImageBasedAnatomy_Tasks/new/main/task6_Image_View)>
   pip install -r requirements.txt
