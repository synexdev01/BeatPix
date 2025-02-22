import os
import requests
import zipfile
import tkinter as tk
from tkinter import ttk
import time

# Ablak beállítása
root = tk.Tk()
root.title("Beatpix setup")
root.geometry("250x150")
root.resizable(False, False)

FFMPEG_URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
FFMPEG_DIR = "packages/ffmpeg"

progress = ttk.Progressbar(root, length=200, mode="determinate")
progress.pack(pady=10)

status_label = tk.Label(root, text="Click setup to start.", font=("Arial", 10))
status_label.pack(pady=5)

def setup():
    os.system("cls")
    status_label.config(text="Checking for FFmpeg...")
    root.update()

    if not os.path.exists(FFMPEG_DIR):
        os.makedirs(FFMPEG_DIR)
        zip_path = os.path.join(FFMPEG_DIR, "ffmpeg.zip")

        os.system("cls")
        status_label.config(text="Downloading FFmpeg...")
        root.update()

        response = requests.get(FFMPEG_URL, stream=True)
        total_size = int(response.headers.get("content-length", 0))
        downloaded_size = 0

        with open(zip_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    
                    if total_size > 0:
                        progress["value"] = (downloaded_size / total_size) * 50
                        root.update()

        os.system("cls")
        status_label.config(text="Unpacking zip...")
        root.update()

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            file_list = zip_ref.namelist()
            total_files = len(file_list)
            
            for i, file in enumerate(file_list):
                zip_ref.extract(file, FFMPEG_DIR)
                progress["value"] = 50 + ((i + 1) / total_files) * 50 
                root.update()

        os.remove(zip_path)

        progress["value"] = 100
        root.update()

    else:
        progress["value"] = 100
        root.update()
        status_label.config(text="Packages are already installed.")
        root.update()
        time.sleep(1)

    status_label.config(text="Starting program...")
    root.update()
    time.sleep(2)
    root.destroy()
    open_main_window()

def open_main_window():
    main_window = tk.Tk()
    main_window.title("BeatPix")
    main_window.geometry("400x200")
    tk.Label(main_window, text="Welcome to BeatPix!", font=("Arial", 14)).pack(pady=20)
    main_window.mainloop()

button = tk.Button(root, text="Setup", command=setup)
button.pack(pady=10)

root.mainloop()
