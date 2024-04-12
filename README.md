# Bio-Emergency-Aid-Navigator

For MakeOHI/O 2024, The Cool Beans created the Bio-Emergency-Aid-Navigator (BEAN). The BEAN is designed to identify people to find lost individuals or to deliver first-aid materials if they're injured. We see this potentially aiding in search parties during forest fires, among other circumstances, for a specific example. The project uses a DJI Mavic Mini drone with YOLOv8 to showcase the idea. On the DJI Mavic Mini, we've created our own drop system with custom 3D printed parts, an Adafruit ESP32, and a servo to simulate the drop of first-aid. YOLOv8 has a lot of different models for different scenarios depending on the desired accuracy/speed so for the BEAN we've decided to use YOLOv8-S. We've help trained the YOLOv8-S model with footage we took on the drone during MakeOHI/O. Also, we're providing a dashboard interface to display information relating to the drone. For example, it displays a live feed from the drone, the option to switch between drones, the GPS location of the drone, the items in the drone's drop system.

In the future, we'd like to expand upon the project to provide more and/or heavier supplies by using better drones, better materials, and a better drop system (with the consideration of a balance between cost, efficiency, weight, etc.). This relates to our goal of having different specifically targeted first-aid kits based on the scenario the drone is being deployed for. Also, with more experience and expertise, we'd like to fine-tune the YOLOv8 models to distinguish between people and injured people effectively.
