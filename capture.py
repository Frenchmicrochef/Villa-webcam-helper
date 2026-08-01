import cv2
import requests
from datetime import datetime

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

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

print("--------------------------------")
print("Connecting to Google Drive...")

SCOPES = ["https://www.googleapis.com/auth/drive"]

credentials = service_account.Credentials.from_service_account_file(
    "credentials.json",
    scopes=SCOPES
)

drive = build("drive", "v3", credentials=credentials)

print("Connected successfully!")

LATEST_FOLDER = "1Sydc4u15d_cMAPebFpcTI_rRkw1IGgXX"

results = drive.files().list(
    q=f"name='LATEST.jpg' and '{LATEST_FOLDER}' in parents",
    fields="files(id,name)"
).execute()

files = results.get("files", [])

print(f"Found {len(files)} matching files.")

# Delete existing LATEST.jpg

#if files:
    #drive.files().delete(fileId=files[0]["id"]).execute()
    #print("Old LATEST.jpg deleted.")

# Upload new latest.jpg

file_metadata = {
    "name": "LATEST.jpg",
    "parents": [LATEST_FOLDER]
}

media = MediaFileUpload(
    "latest.jpg",
    mimetype="image/jpeg"
)

new_file = drive.files().create(
    body=file_metadata,
    media_body=media,
    fields="id"
).execute()

print("New LATEST.jpg uploaded!")
print(f"File ID: {new_file['id']}")
