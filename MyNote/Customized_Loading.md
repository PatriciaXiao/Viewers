To set up the OHIF Viewer to load DICOM images from your local folder `/Users/patriciaxiao/Documents/GitHub/Viewers/MRI_spine_sample`, you'll need to run a **DICOMweb server** (e.g., Orthanc) to serve those files in a way the OHIF Viewer can understand.

OHIF **does not directly read from local folders or `.dcm` files** — it speaks to **DICOMweb servers**.

---

## ✅ Step-by-Step Guide: Setup OHIF Viewer with Your Local DICOM Files

---

### **Step 1: Install Docker (if not done already)**

Install Docker from: [https://docs.docker.com/desktop/install/mac/](https://docs.docker.com/desktop/install/mac/)

Make sure Docker is running:

```bash
docker version
```

---

### **Step 2: Start Orthanc and Mount Your Dataset**

Run this command to start Orthanc with your local DICOM folder:

```bash
docker run -d \
  --name orthanc \
  -p 8042:8042 -p 4242:4242 \
  -v /Users/patriciaxiao/Documents/GitHub/Viewers/MRI_spine_sample:/dicom:ro \
  jodogne/orthanc-plugins
```

But here's the catch:

> Orthanc does **not automatically import DICOM files** just because they are mounted — we need to **tell it to import them**.

---

### **Step 3: Import DICOM Files into Orthanc**

Run this inside the Orthanc container to load the files:

```bash
docker exec -it orthanc bash
find /dicom -type f | while read file; do curl -X POST "http://localhost:8042/instances" --data-binary @"$file" -H "Content-Type: application/dicom"; done
exit
```

**Above Not Working**

Recommended fixation:

```bash
docker exec -it orthanc bash
find /Users/patriciaxiao/Documents/GitHub/Viewers/MRI_spine_sample -type f | while read file; do curl -X POST "http://localhost:8042/instances" --data-binary @"$file" -H "Content-Type: application/dicom"; done
```

This command finds all files and uploads them to Orthanc, even if they don’t have a `.dcm` extension.

You can verify by visiting:

```
http://localhost:8042/
```

Username: `orthanc`, Password: `orthanc`

You should see your studies appear under "Explorer".

---

### **Step 4: Point OHIF Viewer to Orthanc**

Open your OHIF viewer source folder.

Edit this config file:

```
platform/app/public/config/default.js
```

Update the `dicomWeb` section to:

```js
dicomWeb: [
  {
    name: 'Orthanc',
    wadoUriRoot: 'http://localhost:8042/wado',
    qidoRoot: 'http://localhost:8042/dicom-web',
    wadoRoot: 'http://localhost:8042/dicom-web',
    qidoSupportsIncludeField: true,
    imageRendering: 'wadouri',
    thumbnailRendering: 'wadouri',
    enableStudyLazyLoad: true,
  },
]
```

Then restart OHIF (if using yarn):

```bash
yarn dev
```

Visit:

```
http://localhost:3000/
```

You should now see your loaded studies!

---

## ✅ Summary

| Step | Task                                                 |
| ---- | ---------------------------------------------------- |
| 1    | Install Docker                                       |
| 2    | Run Orthanc and mount your local folder              |
| 3    | Use `curl` inside Orthanc container to import DICOMs |
| 4    | Configure OHIF to use Orthanc DICOMweb               |
| 5    | Launch OHIF                                          |

---

Would you like a one-line script to automate all of the above?

```shell
docker rm -f orthanc 2>/dev/null && docker run -d --name orthanc -p 8042:8042 -p 4242:4242 -v /Users/patriciaxiao/Documents/GitHub/Viewers/MRI_spine_sample:/dicom:ro jodogne/orthanc-plugins

```