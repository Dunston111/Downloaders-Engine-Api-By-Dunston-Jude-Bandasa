from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/get-video', methods=['POST'])
def get_video():
    try:
        url = request.json.get('url')
        
        ydl_opts = {
            # Forces the "Web" client which is more stable for links
            'format': '18/best[vcodec!=none][acodec!=none]',
            'quiet': True,
            'no_check_certificate': True,
            # This is the "Magic" part: it uses the iOS client identity
            # which YouTube currently challenges less than Desktop
            'extractor_args': {
                'youtube': {
                    'player_client': ['ios'],
                }
            },
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1'
            }
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({
                'success': True,
                'title': info.get('title'),
                'download_url': info.get('url')
            })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

app = app
