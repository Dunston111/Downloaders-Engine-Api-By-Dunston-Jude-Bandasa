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
        
        # Fast pathing
        current_dir = os.path.dirname(os.path.abspath(__file__))
        original_cookie_path = os.path.join(current_dir, 'cookies.txt')
        temp_cookie_path = "/tmp/cookies.txt"
        
        # Only write if it doesn't exist to save precious milliseconds
        if not os.path.exists(temp_cookie_path):
            with open(original_cookie_path, 'r') as f:
                data = f.read()
            with open(temp_cookie_path, 'w') as f:
                f.write(data)

        ydl_opts = {
            'format': '18/best', # 18 is the fastest to find
            'cookiefile': temp_cookie_path,
            'quiet': True,
            'no_check_certificate': True,
            'no_warnings': True,
            # CRITICAL: Skip extracting the "whole" page, just get the URL
            'extract_flat': False, 
            'force_generic_extractor': False,
            'extractor_args': {
                'youtube': {
                    'player_client': ['ios'], # iOS is the fastest handshake
                    'player_skip': ['webpage', 'configs']
                }
            }
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # We fetch ONLY the basic info to beat the 10s timer
            info = ydl.extract_info(url, download=False)
            return jsonify({
                'success': True,
                'title': info.get('title'),
                'download_url': info.get('url')
            })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400
