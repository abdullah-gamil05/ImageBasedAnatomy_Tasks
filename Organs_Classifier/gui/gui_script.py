import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.models import load_model

# Load our trained model
model = load_model('team12_model.h5')
class_names = ['brain', 'breast', 'liver', 'lung']  # Use our specific classes

# Create the main window
root = tk.Tk()
root.title("anatomy task2")
root.geometry("700x750")
root.iconbitmap(r"D:\python workspace\anatomy_tasks\x-rays (1).ico")

# Title Frame
title_frame = tk.Frame(root, bg="lightgrey", bd=5, relief="raised")
title_frame.pack(pady=5, padx=10, fill="x")

# Add icon in title frame
icon_image = Image.open(r"D:\python workspace\anatomy_tasks\x-rays (1).ico")
icon_image = icon_image.resize((24, 24))
icon_tk = ImageTk.PhotoImage(icon_image)
icon_label = tk.Label(title_frame, image=icon_tk, bg="lightgrey")
icon_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

# Title Text
title_label = tk.Label(title_frame, text="Team 12 Classification Model", font=("Helvetica", 14, "bold"), bg="lightgrey")
title_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")

# Function to classify the image
def classify_image(image_path):
    try:
        img = load_img(image_path, target_size=(128, 128), color_mode="grayscale")
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0

        predictions = model.predict(img_array)
        class_index = np.argmax(predictions[0])
        predicted_class = class_names[class_index]

        result_label.config(text=f"Predicted Organ: {predicted_class}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to classify the image: {e}")

# Function to load the image
def load_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        try:
            img = Image.open(file_path).resize((480, 480))
            img_tk = ImageTk.PhotoImage(img)
            image_label.config(image=img_tk)
            image_label.image = img_tk
            classify_image(file_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load the image: {e}")

# Image Display Label
image_label = tk.Label(root)
image_label.pack(pady=10)

# Create the main frame
main_frame = tk.Frame(root, bg="white", bd=2, relief="groove")  # Add a border and a groove effect
main_frame.pack(pady=10, padx=10, fill="both", expand=True)  # Expand to fill main window space

## Load icon image for button
button_icon = Image.open(r"D:\python workspace\anatomy_tasks\image.png")
"D:\python workspace\anatomy_tasks\image.png"
button_icon = button_icon.resize((30, 30))  # Resize icon to fit on button
button_icon_tk = ImageTk.PhotoImage(button_icon)

# Button for loading images, with icon on the left of text
button = tk.Button(root, text="Load Image to Classify", image=button_icon_tk, compound="left",  # Display icon on left
                   command=load_image, bg="#ADD8E6", fg="black",
                   font=("Helvetica", 10, "bold"), relief="raised",
                   borderwidth=3, padx=20, pady=10)
button.image = button_icon_tk  # Keep reference to avoid garbage collection
button.pack(pady=30)

#Hover Effect for Button
def on_enter(e):
    button.config(bg="#87CEEB")  # Lighter blue on hover

def on_leave(e):
    button.config(bg="#ADD8E6")  # Original color

button.bind("<Enter>", on_enter)
button.bind("<Leave>", on_leave)

#Result Display Frame and Label
result_frame = tk.Frame(main_frame, bg="lightblue", bd=2, relief="sunken")
result_frame.pack(pady=10, padx=5, fill="x")
result_label = tk.Label(result_frame, text="Predicted Organ: None", font=("Helvetica", 12, "bold"))
result_label.pack(padx=5, pady=5)


# Start the GUI
root.mainloop()
