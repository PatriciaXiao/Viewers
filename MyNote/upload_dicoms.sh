#!/bin/bash
# Upload all files in the directory to Orthanc

DICOM_DIR="/Users/patriciaxiao/Documents/GitHub/Viewers/MRI_spine_sample"  # change for Linux path if needed
ORTHANC_URL="http://localhost:8042/instances"

find "$DICOM_DIR" -type f | while read file; do
  echo "Uploading: $file"
  curl -s -X POST "$ORTHANC_URL" \
       -H "Content-Type: application/dicom" \
       --data-binary @"$file" > /dev/null
done

echo "✅ All files uploaded."
