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
    body { margin:0; background:#000; width:100vw; height:100vh; overflow:hidden; }
    #playerframe { width:100vw; height:100vh; border:none; display:block; }
    .err { color: #fff; text-align: center; }
  </style>
</head>
<body>
  {% if ep_url %}
    <iframe id="playerframe" src="{{ ep_url }}" allowfullscreen></iframe>
    <script>
      window.onload = function() {
        var frame = document.getElementById('playerframe');
        if (frame.requestFullscreen) {
          frame.requestFullscreen();
        } else if (frame.webkitRequestFullscreen) {
          frame.webkitRequestFullscreen();
        } else if (frame.mozRequestFullScreen) {
          frame.mozRequestFullScreen();
        } else if (frame.msRequestFullscreen) {
          frame.msRequestFullscreen();
        }
      };
    </script>
  {% else %}
    <p class="err">No episode URL provided.</p>
  {% endif %}
</body>
</html>
"""

@app.route("/play")
def play():
    ep_url = request.args.get("ep_url", "")
    return render_template_string(HTML, ep_url=ep_url)

@app.route("/ping")
def ping():
    return "pong"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
