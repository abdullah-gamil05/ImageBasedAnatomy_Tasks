# Enhanced Soccer Player Tracking and Heatmap Visualization

## Overview
This project leverages **YOLO v8** for real-time soccer player detection and tracking, alongside heatmap generation to visualize player movements on a soccer field. The application enables tracking multiple players in a video and creates heatmaps to analyze their positional behavior during the game.

## Features
- **Real-Time Player Detection**:
  - Utilizes the YOLO v8 model to detect and track soccer players in video footage.
  - Filters out referees based on their clothing's dark color intensity.

- **Player Identification**:
  - Dynamically assigns unique IDs to players based on their positions.
  - Tracks up to 10 players with consistent ID assignment.

- **Heatmap Generation**:
  - Visualizes player movement on a soccer field.
  - Uses kernel density estimation (KDE) to generate heatmaps for positional density.

- **Intuitive GUI**:
  - Built with **Tkinter** and **ttkbootstrap** for an interactive user interface.
  - Features buttons for video selection and per-player heatmap generation.

## Requirements
### Python Libraries:
- `opencv-python`
- `ultralytics`
- `numpy`
- `matplotlib`
- `seaborn`
- `ttkbootstrap`
- `tkinter`

### Installation:
```bash
pip install opencv-python ultralytics numpy matplotlib seaborn ttkbootstrap
```

### 1. Key Functions:
- **Select Video**: Load a soccer game video by clicking the "Select Video" button.
- **Heatmap Generation**:
  - Click on a player's button (Player 0 to Player 9) to generate and view their heatmap.
  - The heatmap visualizes the player's movements on a soccer field layout.

### 2. Controls:
- Press `q` to stop video playback.
- Close the GUI to exit the program.

## How It Works
### 1. **Player Detection and Tracking**:
- The YOLO v8 model detects "person" class objects in the video frames.
- Bounding boxes are filtered to exclude referees (based on pixel color intensity).
- Unique player IDs are assigned based on positional proximity and maintained across frames.

### 2. **Heatmap Visualization**:
- Player movement data is stored as normalized coordinates (scaled to a 600x400 soccer field).
- KDE is applied to generate a heatmap of player positions, overlaid on a soccer field layout.

### 3. **Soccer Field Layout**:
- The soccer field is created using **matplotlib** patches (rectangles and circles) for accurate representation.

## Example Visuals
### 1. Player Tracking
- Video display with bounding boxes and IDs for tracked players.

### 2. Heatmap Visualization
- Heatmap overlaid on a soccer field layout.

## Limitations
- Can track a maximum of 10 players simultaneously.
- Requires videos with clear player visibility for accurate detection.
- Performance may vary depending on hardware specifications.

## Future Enhancements
- Integrate a database to store and retrieve heatmap data.
- Expand tracking to include referees and ball positions.
- Add support for exporting heatmaps as images or reports.

## Acknowledgments
- **YOLO v8**: Pre-trained model for object detection.
- **Ultralytics**: For their YOLO implementation.
- **Seaborn**: For creating KDE-based heatmaps.
- **Matplotlib**: For GUI visualizations.



