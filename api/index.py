import os, yt_dlp
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/get-video', methods=['POST'])
def get_video():
    try:
        url = request.json.get('url')
        c_path = os.path.join(os.path.dirname(__file__), 'cookies.txt')
        t_path = "/tmp/cookies.txt"

        if not os.path.exists(t_path):
            with open(c_path, 'r') as f:
                with open(t_path, 'w') as t: t.write(f.read())

        ydl_opts = {
            'format': 'best', 
            'cookiefile': t_path,
            'quiet': True,
            'no_check_certificate': True,
            # ULTRA SPEED: Don't check for subtitles, chapters, or related clips
            'ignore_playlist': True,
            'youtube_include_dash_manifest': False,
            'youtube_include_hls_manifest': False,
            'no_warnings': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # force_generic_extractor can sometimes skip the heavy YouTube handshake
            info = ydl.extract_info(url, download=False)
            return jsonify({
                'success': True,
                'title': info.get('title'),
                'download_url': info.get('url')
            })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400
