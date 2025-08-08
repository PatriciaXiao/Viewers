#!/usr/bin/env python3
import os
from pyorthanc import Orthanc, upload

# ==== CONFIGURATION ====
#DICOM_DIR = "/Users/patriciaxiao/Documents/GitHub/Viewers/MRI_spine_sample"
DICOM_DIR = "/home/patxiao/MRI_spine_sample" # on ads-vs18
ORTHANC_URL = "http://localhost:8042"
ORTHANC_USERNAME = "orthanc"  # change if needed
ORTHANC_PASSWORD = "orthanc"  # change if needed

# ==== CONNECT TO ORTHANC ====
client = Orthanc(ORTHANC_URL, username=ORTHANC_USERNAME, password=ORTHANC_PASSWORD)

# ==== UPLOAD EVERYTHING ====
for root, _, files in os.walk(DICOM_DIR):
    for f in files:
        file_path = os.path.join(root, f)
        try:
            #with open(file_path, "rb") as dicom_file:
            #    client.upload_file(dicom_file.read())
            upload(client, file_path)
            print(f"✅ Uploaded: {file_path}")
        except Exception as e:
            print(f"❌ Failed to upload {file_path}: {e}")

print("🎉 Upload complete!")

"""
curl -u orthanc:orthanc http://172.28.119.119:8042/dicom-web/studies

docker run -d \
  --name ohif \
  -p 3000:80 \
  --add-host=host.docker.internal:host-gateway \
  -v /home/patxiao/Viewers/MyNote/config.json:/usr/share/nginx/html/config/default.js:ro \
  ohif/viewer
  
"""