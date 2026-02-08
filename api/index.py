from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/get-video', methods=['POST'])
def get_video():
    try:
        url = request.json.get('url')
        
        # YOUR NEW COOKIE STRING
        my_cookies = "GPS=1; YSC=zOgrIjh55Rw; VISITOR_INFO1_LIVE=MH-XmQ6-KMk; VISITOR_PRIVACY_METADATA=CgJNWRIEGgAgTA%3D%3D; __Secure-YNID=15.YT=ODPhlrqK6QHpe0i_xjQZQyxJ71uWFoEj_jdaylhKbYW8JVLgjJpNz3-66h8m1Jy-ZZ9W5CzFCDswjeceMa7cVBWdOAHHSwpvsmcTZFn7AYBEnyCAhNb9qBZgD5cd1qA_b9iVbh2sva-ADRcveeAmzROn3L8z973CWzeZjMeRIAi1R1jhpZhVTjymS0By7VAtNL31LPO0SFfCNY2xim_MofqvOwATzfklxpkStPz5iuHKA9a81i-9UsVDyVaeZxchaa0vIyhNURXN2YSVHKIQLf0_caQ75ZjYNlbUMdunfkUAFt4toHvw_eICspdyW6RzsTXlCCIyUMnYkFmiV-W7kw; __Secure-ROLLOUT_TOKEN=CN68gaTs1MeoQRCD6ZrM5MmSAxjh0eDN5MmSAw%3D%3D; PREF=f6=40000000&tz=Asia.Kuala_Lumpur"

        ydl_opts = {
            'format': '18',  # 360p MP4: The only one guaranteed to work on Vercel
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
            'nocheckcertificate': True,
            'http_headers': {
                'Cookie': my_cookies,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
            }
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # download=False makes this nearly instant
            info = ydl.extract_info(url, download=False)
            return jsonify({
                'success': True,
                'title': info.get('title'),
                'download_url': info.get('url')
            })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

app = app
