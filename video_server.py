from flask import Flask, request, render_template_string
import requests
from bs4 import BeautifulSoup

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
    .err { color: #fff; text-align: center; }
  </style>
</head>
<body>
  {% if src %}
    <video controls autoplay>
      <source src="{{ src }}" type="video/mp4">
      Your browser does not support video playback.
    </video>
  {% else %}
    <p class="err">No video source found or failed to extract video URL.</p>
    {% if error %}
      <pre class="err">{{ error }}</pre>
    {% endif %}
  {% endif %}
</body>
</html>
"""

def extract_video_url(ep_url):
    try:
        print(f"Fetching episode page: {ep_url}")
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(ep_url, headers=headers, timeout=20)
        print(f"Episode page status: {resp.status_code}")
        if resp.status_code != 200:
            return None, f"Failed to fetch episode page. Status: {resp.status_code}"
        soup = BeautifulSoup(resp.text, "html.parser")
        # Try to find <video> tag with <source>
        video = soup.find("video")
        if video:
            source = video.find("source")
            if source and source.has_attr("src"):
                return source["src"], None
        # Try to find <iframe> (sometimes used for embedded players)
        iframe = soup.find("iframe")
        if iframe and iframe.has_attr("src"):
            return iframe["src"], None
        # Try to find direct links in scripts or elsewhere (fallback)
        for tag in soup.find_all("a", href=True):
            if tag["href"].endswith(".mp4"):
                return tag["href"], None
        return None, "No video source found in episode page."
    except Exception as e:
        print(f"Exception in extract_video_url: {e}")
        return None, str(e)

@app.route("/play")
def play():
    ep_url = request.args.get("ep_url", "")
    src = None
    error = None
    if ep_url:
        src, error = extract_video_url(ep_url)
    return render_template_string(HTML, src=src, error=error)

@app.route("/ping")
def ping():
    return "pong"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
