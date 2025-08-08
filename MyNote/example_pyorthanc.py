from pyorthanc import Orthanc, upload

# Connect to your Orthanc server
# Replace with your Orthanc server address, username, and password if applicable
client = Orthanc('http://localhost:8042', username='your_username', password='your_password')

# Upload a single DICOM file
upload(client, 'path/to/your/dicom_file.dcm')

# Upload all DICOM files within a directory (recursively)
upload(client, 'path/to/your/dicom_directory', recursive=True)

# Upload a ZIP archive containing DICOM files
upload(client, 'path/to/your/dicom_files.zip')