import os
# Fix for OpenMP conflict
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
os.environ['OMP_NUM_THREADS'] = '1'

import cv2
from ultralytics import YOLO
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import filedialog, messagebox
from matplotlib.patches import Rectangle, Circle
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import ttkbootstrap as ttk

# Load YOLO v8 model
model = YOLO('yolov8n.pt')

# Global variables
output_data = {}
current_canvas = None
video_playing = True
player_tracks = {}
used_ids = set()  # To track used player IDs
currently_tracked_ids = set()  # To track currently active IDs
inactive_ids = set()  # To track IDs of players who have left the frame


def create_soccer_field(ax):
    ax.add_patch(Rectangle((0, 0), 600, 400, color='green'))
    ax.add_patch(Rectangle((0, 0), 600, 400, edgecolor='white', linewidth=2, fill=False))
    ax.add_patch(Rectangle((0, 150), 18, 100, edgecolor='white', linewidth=2, fill=False))
    ax.add_patch(Rectangle((582, 150), 18, 100, edgecolor='white', linewidth=2, fill=False))
    ax.add_patch(Circle((300, 200), 45.15, edgecolor='white', linewidth=2, fill=False))
    ax.add_patch(Circle((300, 200), 0.3, color='white'))
    ax.plot([300, 300], [0, 400], color='white', linewidth=2)
    ax.set_xlim(0, 600)
    ax.set_ylim(0, 400)
    ax.set_xticks([])
    ax.set_yticks([])

def show_heatmap(player_id):
    global current_canvas

    if player_id not in output_data:
        messagebox.showinfo("Info", f"No data found for Player {player_id}")
        return

    player_positions = output_data[player_id]

    # Extract x and y coordinates
    x_coords = [pos[0] for pos in player_positions]
    y_coords = [400 - pos[1] for pos in player_positions]  # Invert Y-coordinates for correct orientation

    fig, ax = plt.subplots(figsize=(6, 4))
    create_soccer_field(ax)

    # Create the heatmap
    kde = sns.kdeplot(x=x_coords, y=y_coords, cmap="coolwarm", fill=True, bw_adjust=0.5, ax=ax, alpha=0.5)

    # Adjust opacity based on data density
    if len(player_positions) > 20:
        kde.set_alpha(0.8)
    else:
        kde.set_alpha(0.3)

    # Set title and limits
    plt.title(f'Heatmap for Player {player_id}')
    plt.xlim(0, 600)
    plt.ylim(0, 400)
    plt.axis('off')  # Remove axis for a cleaner look

    # Destroy the previous canvas if it exists
    if current_canvas:
        current_canvas.get_tk_widget().destroy()

    # Draw the new heatmap on the Tkinter canvas
    current_canvas = FigureCanvasTkAgg(fig, master=heatmap_frame)
    current_canvas.draw()
    current_canvas.get_tk_widget().pack()

def is_referee(bbox, frame):
    center_x = int((bbox[0] + bbox[2]) / 2)
    center_y = int((bbox[1] + bbox[3]) / 2)
    pixel_color = frame[center_y, center_x]
    return np.all(pixel_color < [80, 80, 80])  # Check for dark colors


def assign_player_id(center, frame_shape):
    global player_tracks, used_ids, currently_tracked_ids, inactive_ids

    normalized_x = center[0] / frame_shape[1] * 600
    normalized_y = center[1] / frame_shape[0] * 400

    min_dist = float('inf')
    closest_id = None

    for player_id, track in player_tracks.items():
        if track:
            last_pos = track[-1]
            dist = np.sqrt((normalized_x - last_pos[0]) ** 2 + (normalized_y - last_pos[1]) ** 2)
            if dist < min_dist:
                min_dist = dist
                closest_id = player_id

    if min_dist > 50 or closest_id is None:  # Threshold for new player
        new_id = len(player_tracks)
        while new_id in used_ids or new_id in inactive_ids:  # Ensure unique ID
            new_id += 1

        if new_id < 10:  # Limit to 10 players
            player_tracks[new_id] = [(normalized_x, normalized_y)]
            used_ids.add(new_id)
            currently_tracked_ids.add(new_id)  # Track currently active IDs
            return new_id
        return None
    else:
        if closest_id not in currently_tracked_ids:  # Prevent reusing the same ID
            currently_tracked_ids.add(closest_id)
        player_tracks[closest_id].append((normalized_x, normalized_y))
        return closest_id


def play_video(video_path):
    global video_playing, player_tracks, output_data, currently_tracked_ids, inactive_ids
    cap = cv2.VideoCapture(video_path)

    while video_playing:
        ret, frame = cap.read()
        if not ret:
            break

        results = model.track(frame)
        currently_tracked_ids.clear()

        for player in results[0].boxes:
            if player.cls == 0:  # Check if it's a person
                bbox = player.xyxy[0].cpu().numpy()

                if is_referee(bbox, frame):
                    continue

                center = ((bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2)
                player_id = assign_player_id(center, frame.shape)

                if player_id is not None:
                    cv2.rectangle(frame,
                                  (int(bbox[0]), int(bbox[1])),
                                  (int(bbox[2]), int(bbox[3])),
                                  (0, 255, 0), 2)
                    cv2.putText(frame, f"Player {player_id}",
                                (int(bbox[0]), int(bbox[1] - 10)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                (0, 255, 0), 2)

                    if player_id not in output_data:
                        output_data[player_id] = []
                    output_data[player_id].append(player_tracks[player_id][-1])

        frame = cv2.resize(frame, (800, 600))
        cv2.imshow('Soccer Game Tracking', frame)

        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            video_playing = False
            break

    cap.release()
    cv2.destroyAllWindows()


def select_video():
    video_path = filedialog.askopenfilename(title="Select Video", filetypes=[("Video Files", "*.mp4;*.avi")])
    if video_path:
        video_thread = threading.Thread(target=play_video, args=(video_path,))
        video_thread.daemon = True
        video_thread.start()


def on_closing():
    global video_playing
    video_playing = False
    root.destroy()


# Main GUI Setup
root = ttk.Window(themename="darkly")
root.title("Enhanced Soccer Player Tracking and Heatmap")
root.geometry("1200x700")

# Frames
button_frame = ttk.Frame(root, padding=50)
button_frame.pack(side=tk.LEFT, fill=tk.Y)

video_frame = ttk.Frame(root, padding=30)
video_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

heatmap_frame = ttk.Frame(root, padding=30)
heatmap_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Buttons
select_video_button = ttk.Button(button_frame, text="Select Video", command=select_video)
select_video_button.pack(pady=40)

for i in range(10):
    btn = ttk.Button(button_frame, text=f"Player {i}", command=lambda x=i: show_heatmap(x))
    btn.pack(pady=5)

# Status Bar
status_bar = ttk.Label(
    root,
    text="Welcome to Soccer Tracker",
    relief=tk.SUNKEN,
    anchor=tk.CENTER,  # Center-align text
    font=("Helvetica", 14)  # Set larger font and size
)
status_bar.pack(side=tk.TOP, fill=tk.X)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
