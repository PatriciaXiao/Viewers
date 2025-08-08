Absolutely! Since you only have **Docker access**, the easiest way is to run an **nginx reverse proxy as a Docker container** that:

* Listens on a new port (e.g., 8043)
* Forwards `/dicom-web` requests to your Orthanc server on port 8042
* Injects the Basic Auth header so OHIF Viewer can access Orthanc without needing to login manually
* Sets proper CORS headers so OHIF running on port 3000 can access it

---

# Step-by-step: Setup nginx reverse proxy with Docker

---

## 1. Create an nginx config file on your host

Create a file, for example `/home/patxiao/nginx_orthanc_proxy.conf` with the following content (adjust hostnames/IPs if needed):

```nginx
events {
  worker_connections 1024;
}

http {
  server {
    listen 8043;

    location /dicom-web/ {
      proxy_pass http://host.docker.internal:8042/dicom-web/;

      # Basic Auth header for Orthanc (replace with your base64 user:pass)
      proxy_set_header Authorization "Basic UGF0cmljaWFGaWF4bzpwYXR4aWFvMjAyNQ==";

      # Enable CORS for OHIF on port 3000
      add_header 'Access-Control-Allow-Origin' 'http://localhost:3000' always;
      add_header 'Access-Control-Allow-Credentials' 'true' always;
      add_header 'Access-Control-Allow-Headers' 'Authorization, Content-Type' always;

      # Handle preflight OPTIONS requests for CORS
      if ($request_method = OPTIONS ) {
        add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS, PUT, DELETE';
        add_header 'Access-Control-Allow-Origin' 'http://localhost:3000';
        add_header 'Access-Control-Allow-Credentials' 'true';
        add_header 'Access-Control-Allow-Headers' 'Authorization, Content-Type';
        return 204;
      }
    }
  }
}
```

---

## 2. Get the base64 for your Orthanc username\:password

Run on your server:

```bash
echo -n 'PatriciaXiao:patxiao2025' | base64
```

You’ll get something like:

```
UGF0cmljaWFGaWF4bzpwYXR4aWFvMjAyNQ==
```

Make sure this matches the value in the config above (`proxy_set_header Authorization ...`).

---

## 3. Run the nginx container with the config mounted

Run this Docker command to start nginx:

```bash
docker run -d \
  --name orthanc-nginx-proxy \
  -p 8043:8043 \
  -v /home/patxiao/Viewers/MyNote/config/nginx_proxy.conf:/etc/nginx/nginx.conf:ro \
  nginx
```

* This runs nginx with your custom config
* Listens on port 8043 on the host

Validate: check ```http://172.28.119.119:8043/dicom-web/studies```

---

## 4. Verify the proxy is working

Test from the server:

```bash
curl -i http://localhost:8043/dicom-web/studies
```

You should get a **valid JSON list of studies** (same as from Orthanc's API), *without* an auth prompt.

---

## 5. Run OHIF Viewer Docker with new DICOMWEB\_SERVER

Start OHIF container, telling it to use the proxy URL (note the use of `host.docker.internal`):

```bash
docker run -d \
  --name ohif \
  -p 3000:80 \
  --add-host=host.docker.internal:host-gateway \
  -e "VITE_DICOMWEB_SERVER=http://172.28.119.119:8043/dicom-web" \
  ohif/viewer
```

debug here:

```bash
docker run --rm --add-host=host.docker.internal:host-gateway curlimages/curl \
  curl -i http://172.28.119.119:8043/dicom-web/studies
```

```bash
docker run -d \
  --name ohif \
  -p 3000:80 \
  --add-host=host.docker.internal:host-gateway \
  -e "VITE_DICOMWEB_SERVER=http://172.28.119.119:8043/dicom-web" \
  ohif/viewer
```

---

## 6. Open OHIF Viewer

Open your browser to:

```
http://172.28.119.119:3000/
```

It should load your Orthanc studies without asking for username/password.

---

# Why this works:

* Orthanc stays protected behind auth on 8042
* nginx on 8043 adds the auth header automatically for OHIF
* nginx adds CORS headers so OHIF running on 3000 can communicate
* OHIF talks to 8043, **no login popup**, seamless browsing

---

If you want me to help with writing a `docker-compose.yml` or debug any step, just ask!
