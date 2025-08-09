#!/usr/bin/env python3
from flask import Flask, request, Response, stream_with_context, render_template_string, abort
import requests
import os
from urllib.parse import urljoin

app = Flask(__name__)

# ---------- CONFIG ----------
# Where Orthanc OHIF is reachable from the server (use host/port accessible from the server)
ORTHANC_OHIF_BASE = "http://127.0.0.1:8042/ohif/"   # <-- change if needed
ORTHANC_AUTH = ("PatriciaXiao", "patxiao2025")      # <-- secure this in env in production
# Optionally set to True to restrict to local requests only
REQUIRE_LOGIN = False
# ----------------------------

# A very small HTML page embedding the iframe (you can use your own template)
INDEX_HTML = """
<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>Embedded OHIF</title>
    <style>body,html{height:100%;margin:0}iframe{border:0;width:100%;height:100%}</style>
  </head>
  <body>
    <iframe src="{{ url }}" id="ohif_iframe" allowfullscreen></iframe>
  </body>
</html>
"""

def build_target_url(path):
    # join will correctly handle missing/trailing slashes
    if path:
        return urljoin(ORTHANC_OHIF_BASE, path)
    return ORTHANC_OHIF_BASE

@app.route("/")
def index():
    # iframe points to the proxy root (which will proxy /ohif/)
    return render_template_string(INDEX_HTML, url="/ohif_proxy/")

@app.route("/ohif_proxy/", defaults={"path": ""}, methods=["GET","POST","PUT","DELETE","OPTIONS","HEAD"])
@app.route("/ohif_proxy/<path:path>", methods=["GET","POST","PUT","DELETE","OPTIONS","HEAD"])
def ohif_proxy(path):
    # (Optional) Add your access control here, e.g. require session login
    if REQUIRE_LOGIN:
        # replace with your auth check
        # if not session.get("user"): return redirect(url_for("login"))
        pass

    target = build_target_url(path)
    method = request.method

    # Build headers to forward: allow OHIF/Orthanc to operate. Drop host header.
    forward_headers = {}
    for name, value in request.headers.items():
        lname = name.lower()
        if lname in ("host", "content-length", "accept-encoding", "connection"):
            continue
        # let servlet pass original accept header etc.
        forward_headers[name] = value

    # If the browser includes an Authorization header, we ignore it and use server-side credentials.
    # You could forward $http_authorization if you want to pass client credentials through.
    try:
        # stream content for large responses
        resp = requests.request(
            method=method,
            url=target,
            headers=forward_headers,
            params=request.args,
            data=request.get_data(),    # POST body
            auth=ORTHANC_AUTH,
            stream=True,
            allow_redirects=False,
            timeout=60
        )
    except requests.RequestException as e:
        # Upstream failed
        return ("Upstream request failed: %s" % str(e), 502)

    # Build Flask response streaming the upstream body
    excluded_headers = {"content-encoding", "transfer-encoding", "connection", "keep-alive"}
    headers = [(name, value) for name, value in resp.headers.items() if name.lower() not in excluded_headers]

    # Remove X-Frame-Options (prevents embedding). You may want to set your own CSP/headers.
    filtered_headers = {}
    for name, value in headers:
        if name.lower() in ("x-frame-options", "x-xss-protection"):
            continue
        filtered_headers[name] = value

    # Ensure the response has a content-type, etc.
    content_type = resp.headers.get("Content-Type")
    if content_type:
        filtered_headers["Content-Type"] = content_type

    # Important: allow embedding by setting Content-Security-Policy frame-ancestors or removing X-Frame-Options
    # You can restrict origins instead of '*'
    filtered_headers["Content-Security-Policy"] = "frame-ancestors 'self' http://172.28.119.119:*"

    # Stream the body back to the client
    return Response(stream_with_context(resp.iter_content(chunk_size=8192)),
                    status=resp.status_code,
                    headers=filtered_headers)

if __name__ == "__main__":
    # ensure requests doesn't buffer entire response for large downloads
    # run on production with gunicorn or uwsgi; this is only a simple dev runner
    app.run(host="0.0.0.0", port=3000, debug=True)
