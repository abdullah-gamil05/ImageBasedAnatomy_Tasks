# Installation Guide for Task 2.2: Enhanced Soccer Player Tracking and Heatmap Visualization

## Prerequisites
1. Ensure you have Python 3.8 or above installed. You can download it from [python.org](https://www.python.org/).
2. Install `pip`, the Python package manager, if not already available.
3. (Optional) Set up a virtual environment for the project:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Linux/Mac
   venv\Scripts\activate    # On Windows
   ```

## Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/abdullah-gamil05/ImageBasedAnatomy_Tasks.git
   cd task2.2_Player_Tracking_and_Heatmap
   ```
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Download the YOLO v8 pretrained model and place it in the `models/` directory.

4. Run the application:
   ```bash
   python src/main.py
   ```

## Notes
- Ensure the video files are in the `data/` folder for processing.
- Output heatmaps and videos will be saved in the `results/` folder.
