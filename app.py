import base64
import os
import threading
import time
from io import BytesIO

import flet as ft
import requests
from dotenv import load_dotenv
from PIL import ImageChops, ImageDraw, ImageGrab

# Load the environment variables from .env file
load_dotenv()

# Access your LINE API key from .env file
env_line_api_key = os.getenv("LINE_API_KEY")


def send_line_notify(notification_message, image_file_path, line_api_key):
    line_notify_api = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": "Bearer " + line_api_key}
    payload = {"message": notification_message}
    files = {"imageFile": open(image_file_path, "rb")}
    post = requests.post(line_notify_api, headers=headers, params=payload, files=files)
    return post.status_code


def take_full_screenshot_with_bounding_box(start_x, start_y, width, height):
    # Take a full screenshot
    screenshot = ImageGrab.grab()

    # Draw a bounding box (rectangle) on the screenshot
    draw = ImageDraw.Draw(screenshot)
    draw.rectangle(
        [(start_x, start_y), (start_x + width, start_y + height)],
        outline="red",
        width=5,
    )

    return screenshot.convert("RGB")  # Convert to RGB if not already


def crop_selected_area(screenshot, start_x, start_y, width, height):
    # Crop the selected area from the full screenshot
    return screenshot.crop((start_x, start_y, start_x + width, start_y + height))


def create_low_quality_image(screenshot):
    # Create a lower-quality version of the screenshot to display (10% quality)
    buffer = BytesIO()
    screenshot.save(buffer, format="JPEG", quality=10)  # Reduce the quality to 10%
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode(
        "utf-8"
    )  # Convert to base64 for display


def save_screenshot_image(screenshot, file_path):
    # Save screenshot to a file
    screenshot.save(file_path, format="JPEG", quality=50)


def compare_images(img1, img2):
    # Compare two images using ImageChops
    diff = ImageChops.difference(img1, img2)
    if diff.getbbox():
        return False  # Images are different
    return True  # Images are the same


def main(page: ft.Page):
    page.title = "Screenshot App"

    # Variables for coordinates, size, interval, and LINE API key
    start_x = ft.TextField(label="Start X", value="0")
    start_y = ft.TextField(label="Start Y", value="0")
    width = ft.TextField(label="Width", value="100")
    height = ft.TextField(label="Height", value="100")
    interval = ft.TextField(label="Interval (seconds)", value="5")

    # Textbox for LINE API key with asterisks shown
    line_api_key_input = ft.TextField(
        label="LINE API Key", value="", password=True
    )  # Password hides input with asterisks

    # Image component to display the full screenshot
    screenshot_image = ft.Image(
        src_base64="", width=600, height=400
    )  # Keep original size
    status_text = ft.Text(value="Status: Ready", size=14)

    stop_event = threading.Event()

    def get_line_api_key():
        """Return the appropriate LINE API key, prioritizing the textbox value."""
        if (
            line_api_key_input.value.strip()
        ):  # Use the API key from the textbox if filled
            return line_api_key_input.value.strip()
        return env_line_api_key  # Otherwise, use the one from the .env file

    def periodic_screenshot(start_x, start_y, width, height, interval):
        last_cropped = None
        file_path = "final_screenshot.jpg"  # Path for the final screenshot file
        line_api_key = (
            get_line_api_key()
        )  # Get the LINE API key from the textbox or .env

        if not line_api_key:  # If no LINE API key is provided, stop the process
            status_text.value = "Error: No LINE API key provided"
            page.update()
            return

        while not stop_event.is_set():
            # Take a full screenshot and draw the bounding box on the selected area
            full_screenshot = take_full_screenshot_with_bounding_box(
                start_x, start_y, width, height
            )

            # Crop the selected area for comparison
            cropped_screenshot = crop_selected_area(
                full_screenshot, start_x, start_y, width, height
            )

            # Compare with the last cropped screenshot
            if last_cropped and compare_images(cropped_screenshot, last_cropped):
                # Save the final screenshot
                save_screenshot_image(full_screenshot, file_path)

                # Notify via LINE that the process finished
                status_code = send_line_notify(
                    "Process finished. Here is the final screenshot:",
                    file_path,
                    line_api_key,
                )
                if status_code == 200:
                    status_text.value = (
                        "Finished: No changes detected. Notification sent."
                    )
                else:
                    status_text.value = f"Finished: No changes detected. Failed to send notification (Status: {status_code})"

                stop_event.set()
                page.update()
                break

            # Store the current cropped screenshot for future comparison
            last_cropped = cropped_screenshot

            # Display the full screenshot with bounding box in the app
            screenshot_base64 = create_low_quality_image(full_screenshot)
            screenshot_image.src_base64 = screenshot_base64
            status_text.value = "Status: Capturing..."
            page.update()

            # Sleep for the specified interval
            time.sleep(interval)

        status_text.value = "Status: Finished"
        page.update()

    def on_start_screenshots(e):
        # Stop any ongoing screenshots
        stop_event.clear()

        # Convert interval to float
        try:
            interval_value = float(interval.value)
        except ValueError:
            status_text.value = "Error: Invalid interval input"
            page.update()
            return

        # Start periodic screenshots in a new thread
        threading.Thread(
            target=periodic_screenshot,
            args=(
                int(start_x.value),
                int(start_y.value),
                int(width.value),
                int(height.value),
                interval_value,
            ),
        ).start()

    def on_stop_screenshots(e):
        stop_event.set()
        status_text.value = "Status: Stopped"
        page.update()

    def on_remove_screenshot(e):
        # Clear the screenshot and reset status
        screenshot_image.src_base64 = ""
        status_text.value = "Screenshot removed"
        page.update()

    def on_take_screenshot_preview(e):
        # Take a screenshot for preview
        full_screenshot = take_full_screenshot_with_bounding_box(
            int(start_x.value), int(start_y.value), int(width.value), int(height.value)
        )
        screenshot_base64 = create_low_quality_image(full_screenshot)
        screenshot_image.src_base64 = screenshot_base64
        status_text.value = "Preview screenshot taken"
        page.update()

    # Buttons to start, stop, take preview, and remove screenshots
    start_button = ft.ElevatedButton(text="Start", on_click=on_start_screenshots)
    stop_button = ft.ElevatedButton(text="Stop", on_click=on_stop_screenshots)
    take_screenshot_preview_button = ft.ElevatedButton(
        text="Take Screenshot (Preview)", on_click=on_take_screenshot_preview
    )
    remove_button = ft.ElevatedButton(
        text="Remove Screenshot", on_click=on_remove_screenshot
    )

    # Add components to the page with textbox for LINE API key
    page.add(
        ft.Column(
            [
                ft.Row(
                    [start_x, start_y], spacing=20
                ),  # First row for Start X and Start Y
                ft.Row([width, height], spacing=20),  # Second row for Width and Height
                ft.Row([interval], spacing=20),  # Third row for the interval input
                ft.Row([line_api_key_input]),  # Textbox for LINE API key input
                ft.Text("Monitoring:", size=16),  # Label for Monitoring buttons
                ft.Row(
                    [start_button, stop_button], spacing=20
                ),  # Start and Stop buttons
                ft.Text("App Control:", size=16),  # Label for App Control buttons
                ft.Row(
                    [take_screenshot_preview_button, remove_button], spacing=20
                ),  # Preview and Remove buttons
                screenshot_image,  # Image widget to display the full screenshot
                ft.Container(
                    content=status_text, padding=ft.padding.only(top=20)
                ),  # Added padding for spacing
            ],
            spacing=20,
        )  # Overall vertical spacing for the layout
    )


ft.app(target=main)
