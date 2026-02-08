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
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        original_cookie_path = os.path.join(current_dir, 'cookies.txt')
        temp_cookie_path = "/tmp/cookies.txt"
        
        # Read/Write to /tmp to bypass Vercel's read-only lock
        with open(original_cookie_path, 'r') as f:
            data = f.read()
        with open(temp_cookie_path, 'w') as f:
            f.write(data)

        ydl_opts = {
            # 'best' finds the highest quality file that is ALREADY merged (no ffmpeg needed)
            'format': 'best', 
            'cookiefile': temp_cookie_path,
            'quiet': True,
            'no_check_certificate': True,
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'ios'],
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
