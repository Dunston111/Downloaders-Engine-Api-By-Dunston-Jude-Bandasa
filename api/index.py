import yt_dlp
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Allows your website to talk to your laptop

@app.route('/get-video', methods=['POST'])
def get_video():
    try:
        data = request.json
        video_url = data.get('url')
        
        ydl_opts = {
            'format': 'best',
            'cookiefile': 'cookies.txt', # Keep cookies.txt in the same folder
            'quiet': True,
            'no_check_certificate': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            return jsonify({
                'success': True,
                'title': info.get('title'),
                'download_url': info.get('url')
            })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    app.run(port=5000)