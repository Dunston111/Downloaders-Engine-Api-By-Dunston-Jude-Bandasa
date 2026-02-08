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
        
        # 1. Read the cookie file from your app folder
        current_dir = os.path.dirname(os.path.abspath(__file__))
        original_cookie_path = os.path.join(current_dir, 'cookies.txt')
        
        # 2. Copy it to /tmp (The only writable area in Vercel)
        temp_cookie_path = "/tmp/cookies.txt"
        with open(original_cookie_path, 'r') as f:
            data = f.read()
        with open(temp_cookie_path, 'w') as f:
            f.write(data)

        ydl_opts = {
            'format': '18', 
            'cookiefile': temp_cookie_path, # Point to the writable copy
            'quiet': True,
            'no_check_certificate': True,
            'extractor_args': {
                'youtube': {
                    'player_client': ['ios'],
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
