from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/get-video', methods=['POST'])
def get_video():
    try:
        url = request.json.get('url')
        
        # The cookies you found
        my_cookies = "GPS=1; YSC=zOgrIjh55Rw; VISITOR_INFO1_LIVE=MH-XmQ6-KMk; VISITOR_PRIVACY_METADATA=CgJNWRIEGgAgTA%3D%3D; __Secure-YNID=15.YT=ODPhlrqK6QHpe0i_xjQZQyxJ71uWFoEj_jdaylhKbYW8JVLgjJpNz3-66h8m1Jy-ZZ9W5CzFCDswjeceMa7cVBWdOAHHSwpvsmcTZFn7AYBEnyCAhNb9qBZgD5cd1qA_b9iVbh2sva-ADRcveeAmzROn3L8z973CWzeZjMeRIAi1R1jhpZhVTjymS0By7VAtNL31LPO0SFfCNY2xim_MofqvOwATzfklxpkStPz5iuHKA9a81i-9UsVDyVaeZxchaa0vIyhNURXN2YSVHKIQLf0_caQ75ZjYNlbUMdunfkUAFt4toHvw_eICspdyW6RzsTXlCCIyUMnYkFmiV-W7kw; __Secure-ROLLOUT_TOKEN=CN68gaTs1MeoQRCD6ZrM5MmSAxjh0eDN5MmSAw%3D%3D; PREF=f6=40000000&tz=Asia.Kuala_Lumpur"

        ydl_opts = {
            # 'best' tells it to stop being picky and just find a single file that works
            'format': 'best', 
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
            'nocheckcertificate': True,
            # This makes the server look like a mobile phone (less likely to be blocked)
            'user_agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36',
            'http_headers': {
                'Cookie': my_cookies
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
        # If it fails, we send back the actual error so we can see it
        return jsonify({'success': False, 'error': str(e)}), 400

app = app
