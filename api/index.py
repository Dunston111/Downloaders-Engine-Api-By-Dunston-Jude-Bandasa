import os
import yt_dlp
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/get-video', methods=['POST'])
def get_video():
    try:
        url = request.json.get('url')
        
        # Vercel path logic: look for cookies.txt in the root project folder
        # '..' goes up one level from the /api folder
        cookie_path = os.path.join(os.path.dirname(__file__), '..', 'cookies.txt')

        ydl_opts = {
            'format': '18',  # Best combined MP4 (360p) for serverless
            'cookiefile': cookie_path,
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True,
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'web'],
                    'player_skip': ['configs', 'webpage']
                }
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
