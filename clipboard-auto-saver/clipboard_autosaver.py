# clipboard_autosaver.py

import os
from datetime import datetime
import time
import pyperclip
from PIL import ImageGrab
import tkinter as tk
import threading

# Get the absolute path of the script directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Set log folder paths relative to script
LOG_DIR = os.path.join(BASE_DIR, "logs")
IMAGE_DIR = os.path.join(LOG_DIR, "images")

# Create folders if they don't exist
os.makedirs(IMAGE_DIR, exist_ok=True)

def get_daily_log_path():
    today = datetime.now().strftime("%Y-%m-%d")
    return os.path.join(LOG_DIR, f"log_{today}.txt")


def save_text(text):
    # Append copied text to the daily log file with a timestamp.
    timestamp = datetime.now().strftime("[%H:%M:%S]")
    log_path = get_daily_log_path()
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} {text.strip()}\n\n")
    print(f"Saved text: {text[:40]}{'...' if len(text) > 40 else ''}")

def save_image(image):
    # Save a clipboard image to the images folder with timestamp.
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    image_path = os.path.join(IMAGE_DIR, f"{timestamp}.png")
    image.save(image_path)
    print(f"Saved image: {image_path}")

def monitor_clipboard(interval=1):
    # Check clipboard every `interval` seconds for new text or images.
    print("Clipboard monitoring started. Press Ctrl+C to stop.")
    last_text = ""
    last_image = None

    try:
        while True:
            # Check for new text
            current_text = pyperclip.paste()
            if current_text.strip() and current_text != last_text:
                save_text(current_text)
                last_text = current_text

            # Check for new image
            image = ImageGrab.grabclipboard()
            if image and image != last_image:
                save_image(image)
                last_image = image

            time.sleep(interval)

    except KeyboardInterrupt:
        print("\nMonitoring stopped.")



class ClipboardApp:
    def __init__(self, root):
        self.root = root
        root.title("Clipboard Auto-Saver")
        root.geometry("400x200")
        root.resizable(False, False)

        # Monitoring state
        self.running = False
        self.monitor_thread = None

        # UI elements
        self.toggle_button = tk.Button(root, text="▶ Start Monitoring", width=25, command=self.toggle_monitoring)
        self.toggle_button.pack(pady=30)

        self.status_label = tk.Label(root, text="Status: Idle", fg="gray")
        self.status_label.pack(pady=10)

    def toggle_monitoring(self):
        if not self.running:
            self.running = True
            self.toggle_button.config(text="⏸ Stop Monitoring")
            self.status_label.config(text="Status: Running...", fg="green")
            self.start_monitor_thread()
        else:
            self.running = False
            self.toggle_button.config(text="▶ Start Monitoring")
            self.status_label.config(text="Status: Stopped", fg="red")

    def start_monitor_thread(self):
        def loop():
            last_text = ""
            last_image = None

            while self.running:
                try:
                    current_text = pyperclip.paste()
                    if current_text.strip() and current_text != last_text:
                        save_text(current_text)
                        last_text = current_text
                        self.update_status("Saved text")

                    image = ImageGrab.grabclipboard()
                    if image and image != last_image:
                        save_image(image)
                        last_image = image
                        self.update_status("Saved image")

                    time.sleep(1)

                except Exception as e:
                    self.update_status(f"Error: {e}")
                    time.sleep(1)

        self.monitor_thread = threading.Thread(target=loop, daemon=True)
        self.monitor_thread.start()

    def update_status(self, message):
        self.status_label.config(text=f"Status: {message}", fg="green")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = ClipboardApp(root)
    root.mainloop()
