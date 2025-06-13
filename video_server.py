from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Anime Player</title>
  <style>
    body { margin:0; background:#000; display:flex; justify-content:center; align-items:center; height:100vh; }
    video { max-width:100%; max-height:100%; }
  </style>
</head>
<body>
  {% if src %}
    <video controls autoplay>
      <source src="{{ src }}" type="video/mp4">
      Your browser does not support video playback.
    </video>
  {% else %}
    <p style="color:white; text-align:center;">No video source provided.</p>
  {% endif %}
</body>
</html>
"""

@app.route("/watch")
def watch():
    src = request.args.get("src", "")
    # Note: you might want to validate 'src' is a valid HTTP/S URL
    return render_template_string(HTML, src=src)

@app.route("/ping")
def ping():
    return "pong"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
