import requests
from flask import Flask, request, Response, render_template_string
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route("/proxy")
def proxy():
    ep_url = request.args.get("ep_url", "")
    if not ep_url:
        return "No episode URL provided.", 400
    
    try:
        logger.info(f"Fetching URL: {ep_url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://animesalt.cc/',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0'
        }
        
        resp = requests.get(ep_url, headers=headers, allow_redirects=True)
        logger.info(f"Response status: {resp.status_code}")
        logger.info(f"Final URL after redirects: {resp.url}")
        
        html = resp.text
        
        # Inject custom CSS to hide elements and fix video player
        custom_css = """
        <style>
            /* Hide logo and branding */
            .custom-logo, 
            img[src*="AnimeSaltLong.png"],
            img[src*="AnimeSaltLong-300x75.png"],
            img[src*="AnimeSaltLong-193x48.png"],
            .site-branding,
            .site-title,
            .site-description,
            .site-header,
            .site-footer,
            .bottom-bar,
            .site-header-inner,
            .site-logo { 
                display: none !important; 
            }
            
            /* Clean up the page */
            body { 
                background: #000 !important; 
                margin: 0 !important;
                padding: 0 !important;
            }
            
            /* Make video player full screen */
            #player { 
                width: 100% !important; 
                height: 100vh !important; 
                position: fixed !important;
                top: 0 !important;
                left: 0 !important;
                z-index: 9999 !important;
            }
            
            .video-js { 
                width: 100% !important; 
                height: 100vh !important; 
            }
            
            /* Hide any remaining UI elements */
            .entry-header,
            .entry-content > *:not(#player),
            .entry-footer,
            .comments-area,
            .widget-area,
            .sidebar,
            .site-navigation,
            .main-navigation {
                display: none !important;
            }
        </style>
        """
        
        # Inject custom JavaScript to handle video player
        custom_js = """
        <script>
            window.onload = function() {
                // Find video player iframe
                var playerFrame = document.querySelector('iframe[src*="player"]');
                if (playerFrame) {
                    playerFrame.style.width = '100%';
                    playerFrame.style.height = '100vh';
                    playerFrame.style.position = 'fixed';
                    playerFrame.style.top = '0';
                    playerFrame.style.left = '0';
                    playerFrame.style.border = 'none';
                }
            };
        </script>
        """
        
        # Insert our custom CSS and JS
        html = html.replace("</head>", custom_css + custom_js + "</head>")
        
        return Response(html, mimetype="text/html")
        
    except Exception as e:
        logger.error(f"Error in proxy: {str(e)}")
        return f"Error: {str(e)}", 500

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
