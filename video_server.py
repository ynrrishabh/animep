import requests
from flask import Flask, request, Response, render_template_string

app = Flask(__name__)

@app.route("/proxy")
def proxy():
    ep_url = request.args.get("ep_url", "")
    if not ep_url:
        return "No episode URL provided.", 400
    resp = requests.get(ep_url)
    html = resp.text
    # Inject custom CSS to hide the logo
    custom_css = """
    <style>
      .custom-logo { position: absolute !important; left: -9999px !important; }
    </style>
    """
    html = html.replace("</head>", custom_css + "</head>")
    return Response(html, mimetype="text/html")

@app.route("/play")
def play():
    ep_url = request.args.get("ep_url", "")
    if not ep_url:
        return "No episode URL provided.", 400
    proxy_url = f"/proxy?ep_url={ep_url}"
    HTML = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width,initial-scale=1">
      <title>Anime Player</title>
      <style>
        body {{ margin:0; background:#000; width:100vw; height:100vh; overflow:hidden; }}
        #playerframe {{ width:100vw; height:100vh; border:none; display:block; }}
        .err {{ color: #fff; text-align: center; }}
      </style>
    </head>
    <body>
      <iframe id="playerframe" src="{proxy_url}" allowfullscreen></iframe>
    </body>
    </html>
    '''
    return HTML

@app.route("/ping")
def ping():
    return "pong"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
