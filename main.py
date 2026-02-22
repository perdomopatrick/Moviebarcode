import os
import subprocess
import threading
from tkinter import filedialog

import customtkinter as ctk
from PIL import Image

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MovieBarcodeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Moviebarcode Generator")
        self.geometry("900x650")

        self.video_path = None
        self.output_name = "barcode.png"

        self.title_label = ctk.CTkLabel(
            self, text="Moviebarcode Generator", font=("Arial", 28)
        )
        self.title_label.pack(pady=20)

        self.select_button = ctk.CTkButton(
            self, text="Select Video", command=self.select_video
        )
        self.select_button.pack(pady=10)

        self.generate_button = ctk.CTkButton(
            self, text="Generate Barcode", command=self.start_generation
        )
        self.generate_button.pack(pady=10)

        self.progress = ctk.CTkProgressBar(self, width=600)
        self.progress.set(0)
        self.progress.pack(pady=20)

        self.image_label = ctk.CTkLabel(self, text="No Barcode Generated Yet")
        self.image_label.pack(pady=20, fill="x")

    def select_video(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Video Files", "*.mp4 *.mkv *.avi *.mov")]
        )
        if file_path:
            self.video_path = os.path.abspath(file_path)
            print(f"Selected: {self.video_path}")

    def start_generation(self):
        if not self.video_path:
            return
        self.generate_button.configure(state="disabled")
        threading.Thread(target=self.generate_barcode, daemon=True).start()

    def generate_barcode(self):
        self.progress.set(0.1)
        video_dir = os.path.dirname(self.video_path)
        video_filename = os.path.basename(self.video_path)
        current_dir = os.getcwd()

        command = [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{video_dir}:/input",
            "-v",
            f"{current_dir}:/workspace",
            "moviebarcode",
            f"/input/{video_filename}",
            f"/workspace/{self.output_name}",
        ]
        self.progress.set(0.4)

        try:
            subprocess.run(command, check=True)
            self.progress.set(0.6)
            self.after(0, self.display_image)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.after(0, lambda: self.generate_button.configure(state="normal"))
            self.after(0, lambda: self.progress.set(1.0))

    def display_image(self):
        if os.path.exists(self.output_name):
            img = Image.open(self.output_name)

            ctk_img = ctk.CTkImage(
                light_image=img,
                dark_image=img,
                size=(850, 200),
            )

            self.image_label.configure(image=ctk_img, text="")
            self.image_label.image = ctk_img


if __name__ == "__main__":
    app = MovieBarcodeApp()
    app.mainloop()
