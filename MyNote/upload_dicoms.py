#!/usr/bin/env python3
import os
from pyorthanc import Orthanc, upload

# ==== CONFIGURATION ====
# Change this path to your DICOM folder
DICOM_DIR = "/Users/patriciaxiao/Documents/GitHub/Viewers/MRI_spine_sample"
# Orthanc connection info
ORTHANC_URL = "http://localhost:8042"
ORTHANC_USERNAME = "orthanc"  # change if needed
ORTHANC_PASSWORD = "orthanc"  # change if needed

# ==== CONNECT TO ORTHANC ====
client = Orthanc(ORTHANC_URL, username=ORTHANC_USERNAME, password=ORTHANC_PASSWORD)

# ==== UPLOAD RECURSIVELY ====
print(f"Uploading DICOM files from: {DICOM_DIR}")
upload(client, DICOM_DIR, recursive=True)
print("✅ Upload complete!")
