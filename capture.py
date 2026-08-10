import cv2
import requests
import os
import shutil
from datetime import datetime

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

print("--------------------------------")
print(f"Capture time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
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
timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
archive_filename = f"{timestamp}.jpg"

# Save both versions
cv2.imwrite("latest.jpg", frame)
cv2.imwrite(archive_filename, frame)

archive_path = os.path.join("archive", archive_filename)
shutil.copy(archive_filename, archive_path)

print(f"Copied to {archive_path}")

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

ARCHIVE_FOLDER = "1-bSLetTMdkuxQzo-zK65aHtqoJd49Sb2"

results = drive.files().list(
    q=f"name='LATEST.jpg' and '{LATEST_FOLDER}' in parents",
    fields="files(id,name)"
).execute()

files = results.get("files", [])

print(f"Found {len(files)} matching files.")

file_id = files[0]["id"]

media = MediaFileUpload(
    "latest.jpg",
    mimetype="image/jpeg"
)

drive.files().update(
    fileId=file_id,
    media_body=media
).execute()

print("LATEST.jpg updated successfully!")

import subprocess

subprocess.run(["git", "config", "user.name", "Villa Webcam Helper"])
subprocess.run(["git", "config", "user.email", "actions@github.com"])

subprocess.run(["git", "add", "archive"])

subprocess.run([
    "git",
    "commit",
    "-m",
    f"Archive webcam {archive_filename}"
])

subprocess.run(["git", "push"])

print("Archive committed to GitHub!")

#archive_metadata = {
    #"name": archive_filename,
    #"parents": [ARCHIVE_FOLDER]
#}

#archive_media = MediaFileUpload(
    #archive_filename,
    #mimetype="image/jpeg"
#)

#drive.files().create(
    #body=archive_metadata,
    #media_body=archive_media
#).execute()

#print(f"{archive_filename} archived successfully!")
