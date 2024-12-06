import torch
import cv2
import numpy as np
from PIL import Image as PILImage
import io
import flet as ft


def main(page: ft.Page):
    page.title = "Tomato Disease Recognition"
    page.scroll = "auto"
    page.theme_mode = "dark"

    # UI Components
    title_text = ft.Text("Tomato Disease Recognition",
                         size=24, weight="bold", color="white")
    subtitle_text = ft.Text(
        "Upload an image to detect disease in tomato plants.", color="white")
    image_display = ft.Image(src="", width=300, height=300, fit="contain")
    result_text = ft.Text("Detected Diseases:", color="white", size=16)
    disease_list = ft.Column([])

    def process_image(uploaded_file):
        pass
        # Here goes your image processing code

    # File Picker for Image Upload
    file_picker = ft.FilePicker(on_result=lambda e: process_image(
        e.files[0].content) if e.files else None)

    # Adding FilePicker to the page overlay
    page.overlay.append(file_picker)

    # File Picker Button
    upload_button = ft.ElevatedButton("Choisir une image", icon=ft.icons.UPLOAD_FILE,
                                      on_click=lambda _: file_picker.pick_files(allow_multiple=False))

    # Adding components to page
    page.add(
        title_text,
        subtitle_text,
        upload_button,
        image_display,
        result_text,
        disease_list
    )


# Run the Flet app
ft.app(target=main)
