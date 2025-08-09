import requests
from flask import Flask, Response

app = Flask(__name__)

@app.route("/<path:filename>")
def ohif_proxy(filename):
    url = f"http://172.28.119.119:8042/{filename}"
    r = requests.get(url, auth=('orthanc-user', 'orthanc-pass'))
    content_type = "application/javascript" if filename.endswith(".js") else r.headers.get("Content-Type", "text/plain")
    return Response(r.content, content_type=content_type)

@app.route("/")
def index():
    return '<iframe src="/ohif/" style="width:100%;height:100%;border:none"></iframe>'

if __name__ == "__main__":
    app.run(port=3000, debug=True)
