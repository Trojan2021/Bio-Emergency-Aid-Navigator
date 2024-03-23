import tkinter as tk

import cv2
import supervision as sv
from Adafruit_IO import Client
from PIL import Image, ImageTk
from ultralytics import YOLO

ADAFRUIT_IO_USERNAME = "xxxxxxxxx"
ADAFRUIT_IO_KEY = "xxxxxxxxx"

FEED_NAME = "test"

aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)


def requestDrop():
    value = input("Enter 0 for close or 1 for open (q to quit): ")

    if value.lower() == "q":
        return

    try:
        value = int(value)
    except ValueError:
        print("Invalid input")
    if value not in [0, 1]:
        print("Invalid input. Please enter 0 or 1.")
    else:
        aio.send_data(FEED_NAME, value)
        print(f"Published value {value} to Adafruit IO feed")


# Initialize the video capture
video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Initialize the YOLO model
model = YOLO("yolov8s.pt")

# Create a Tkinter window
root = tk.Tk()
root.title("YOLO Video Stream")

# Create a label to display the video frame
label = tk.Label(root)
label.pack()


def update_frame():
    # Read a frame from the video
    r, image = video.read()

    # Get YOLO predictions
    results = model(image, conf=0.85)[0]
    detections = sv.Detections.from_ultralytics(results)
    if "person" in detections.data["class_name"]:
        print("Beans")
        requestDrop()

    # Convert the frame to RGB
    im_array = results.plot()
    # im_array = image[..., ::-1]
    im = Image.fromarray(im_array)

    # Update the label with the new frame
    img = ImageTk.PhotoImage(im)
    label.config(image=img)
    label.image = img

    # Call this function again after 10 milliseconds
    root.after(10, update_frame)


# Start updating the frame
update_frame()

# Run the Tkinter event loop
root.mainloop()

# Release the video capture
video.release()
