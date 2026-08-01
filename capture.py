import cv2
import requests
from datetime import datetime

print("--------------------------------")
print(datetime.now())
print("Villa Webcam Helper")
print("--------------------------------")

# Webcam URL
URL = "https://live.neos360.com/luchon/fixes/img/upload/plateau_cabane/plateau_cabane.mp4"

print("Downloading webcam...")

response = requests.get(URL)
response.raise_for_status()

with open("webcam.mp4", "wb") as f:
    f.write(response.content)

print("Opening video...")

video = cv2.VideoCapture("webcam.mp4")

success, frame = video.read()

if not success:
    raise Exception("Couldn't read first frame")

# Create today's filename
timestamp = datetime.now().strftime("%Y%m%d_%H%M")
archive_filename = f"{timestamp}.jpg"

# Save both versions
cv2.imwrite("latest.jpg", frame)
cv2.imwrite(archive_filename, frame)

video.release()

print("latest.jpg created successfully!")
print(f"{archive_filename} created successfully!")
