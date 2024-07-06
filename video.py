import tkinter as tk
from tkinter import simpledialog, messagebox
import cv2
import os

# Function to play the video
def play_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        messagebox.showerror("Error", "Could not open video file.")
        return
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('Video', frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

# Function to get user input and show video
def show_video():
    message = simpledialog.askstring("Input", "Enter the message:")
    if message:
        video_path = f"{message}.mp4"
        if os.path.isfile(video_path):
            play_video(video_path)
        else:
            messagebox.showerror("Error", f"No video found with the name {message}.mp4")

# Function to handle the "Translate More" button
def translate_more():
    show_video()

# Main GUI setup
root = tk.Tk()
root.title("Sign Language Translator")

translate_more_button = tk.Button(root, text="Translate More", command=translate_more)
translate_more_button.pack(pady=20)

# Initial call to show_video
show_video()

root.mainloop()
