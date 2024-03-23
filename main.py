# import cv2
# import supervision as sv
# from ultralytics import YOLO
# from PIL import Image

# video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# r, image = video.read()
# video.release()
# model = YOLO("yolov8s.pt")
# results = model(image)[0]
# detections = sv.Detections.from_ultralytics(results)

# print(results)
# for result in results:
#     im_array = result.plot()  # Get a BGR numpy array of predictions
#     im = Image.fromarray(im_array[..., ::-1])  # Convert to RGB PIL image
#     im.show()  # Show the image
#     im.save("results.jpg")  # Save the image

import tkinter as tk
from PIL import Image, ImageTk
import supervision as sv
import cv2
from ultralytics import YOLO

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
