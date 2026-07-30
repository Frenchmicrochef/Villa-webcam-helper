import cv2
import requests

# Webcam URL
URL = "https://live.neos360.com/luchon/fixes/img/upload/plateau_cremaillere/plateau_cremaillere.mp4"

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

cv2.imwrite("LATEST.jpg", frame)

video.release()

print("LATEST.jpg created successfully!")
