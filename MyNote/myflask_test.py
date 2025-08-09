from flask import Flask, render_template_string

app = Flask(__name__)

@app.route("/")
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>OHIF in Flask Iframe</title>
        <style>
            html, body {
                margin: 0;
                padding: 0;
                height: 100%;
                overflow: hidden;
            }
            iframe {
                width: 100%;
                height: 100%;
                border: none;
            }
        </style>
    </head>
    <body>
        <iframe src="http://172.28.119.119:8042/ohif"></iframe>
    </body>
    </html>
    """)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
