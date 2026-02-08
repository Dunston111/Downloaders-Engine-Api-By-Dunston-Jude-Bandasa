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
        
        # Get the directory where index.py actually lives
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Look for cookies.txt in the same folder as this script
        cookie_path = os.path.join(current_dir, 'cookies.txt')

        ydl_opts = {
            'format': '18', 
            'cookiefile': cookie_path,
            'quiet': True,
            'no_check_certificate': True,
            'extractor_args': {'youtube': {'player_client': ['ios']}}
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
