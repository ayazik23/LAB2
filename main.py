import requests
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

TOKEN = "r94itb8n6baiqcldjrv6ljrgva"
PROJECT_ID = "67404"
MODEL = "object-detection-model-2"
HEADERS = {
    "X-Auth-token": TOKEN,
    "Content-Type": "application/octet-stream"
}

app = ttk.Window(themename="flatly")
app.title("Smart Image Detector")
app.geometry("700x800")
app.resizable(False, False)

main_canvas = tk.Canvas(app, borderwidth=0, highlightthickness=0)
scrollbar = ttk.Scrollbar(app, orient="vertical", command=main_canvas.yview)
scrollable_frame = ttk.Frame(main_canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: main_canvas.configure(
        scrollregion=main_canvas.bbox("all")
    )
)

main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
main_canvas.configure(yscrollcommand=scrollbar.set)

main_canvas.pack(side=LEFT, fill=BOTH, expand=True)
scrollbar.pack(side=RIGHT, fill=Y)

title_label = ttk.Label(
    scrollable_frame,
    text="Upload Image for Detection",
    font=("Helvetica", 20, "bold")
)
title_label.pack(pady=(20, 10))

image_frame = ttk.LabelFrame(scrollable_frame, text="Selected Image", padding=10)
image_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)
image_label = ttk.Label(image_frame)
image_label.pack()

result_box = ttk.LabelFrame(scrollable_frame, text="Prediction Result", padding=10)
result_box.pack(pady=15, padx=20, fill=BOTH)
result_label = ttk.Label(
    result_box,
    text="Waiting for image...",
    font=("Helvetica", 12),
    wraplength=600,
    justify="left"
)
result_label.pack()

def upload_image():
    file_path = filedialog.askopenfilename(
        filetypes=[("JPG Files", "*.jpg"), ("All Files", "*.*")]
    )
    if not file_path:
        return

    img = Image.open(file_path)
    img.thumbnail((600, 800))
    img_tk = ImageTk.PhotoImage(img)
    image_label.config(image=img_tk)
    image_label.image = img_tk

    result_label.config(text="Predicting...")

    try:
        with open(file_path, 'rb') as image_file:
            response = requests.post(
                f'https://platform.sentisight.ai/api/predict/{PROJECT_ID}/{MODEL}/',
                headers=HEADERS,
                data=image_file
            )
        if response.status_code == 200:
            result_label.config(text=f"Prediction:\n{response.text}")
        else:
            result_label.config(text=f"Error {response.status_code}:\n{response.text}")
    except Exception as e:
        result_label.config(text=f"Exception occurred:\n{e}")

upload_button = ttk.Button(
    scrollable_frame,
    text="Upload Image",
    bootstyle=SUCCESS,
    width=20,
    command=upload_image
)
upload_button.pack(pady=(10, 40)) 

footer = ttk.Label(
    scrollable_frame,
    text="Made by MK",
    font=("Helvetica", 10)
)
footer.pack(pady=(0, 30))

def _on_mousewheel(event):
    main_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

main_canvas.bind_all("<MouseWheel>", _on_mousewheel)

app.mainloop()
