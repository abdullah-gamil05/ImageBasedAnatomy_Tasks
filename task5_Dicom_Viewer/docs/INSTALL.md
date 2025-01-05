# Installation Guide for Task 5: DICOM Viewer

## Prerequisites
1. **Python Version**: Ensure you have Python 3.7 or above installed. You can download it from [python.org](https://www.python.org/).
2. **Libraries Required**:
   - `pydicom`: For handling DICOM files.
   - `numpy`: For data manipulation.
   - `Pillow`: For image rendering.
   - `tkinter`: For GUI creation.

## Steps to Install
1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd task5_dicom_viewer
   ```

2. **Set Up a Virtual Environment (Optional)**:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Linux/Mac
   venv\Scripts\activate    # On Windows
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   ```bash
   python src/main.py
   ```

## Notes
- Ensure the DICOM files are stored in the `data/input/` directory.
- Output files (e.g., anonymized DICOMs, visualizations) will be saved in the `data/output/` directory.
