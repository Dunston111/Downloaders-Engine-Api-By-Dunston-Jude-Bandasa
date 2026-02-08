from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/get-video', methods=['POST'])
def get_video():
    try:
        url = request.json.get('url')
        my_cookies = "__Secure-3PSID=g.a0006QgpakK4bwOgTM6gmJQfSEsbRpELb6r0RAX7vs16Uo7_q6x1EOlaqRYaC-Klxs5NbsBiWQACgYKAbsSARcSFQHGX2MioYCAFHZrsVKAwBjOasJFaBoVAUF8yKojIXD_0S-hX0IyAcUuIlTi0076;__Secure-1PSIDTS=sidts-CjUB7I_69KESUfvf7GI8UCif1Vk-7r_5yodQTUlSNbO5yQ-V7aH7cug69fSZiS0fKiyEOUyAzRAA;CONSISTENCY=AAsGu9kW-Ab5egQbVxVldMqikaByNN5zsBFU_gro6CTDKs8sKjW7SwA6IeJ3AZxUoos_Rmrku1Bbm5K6zWjJkTk86BZEoYRpcTZeKYWsRhGaeUr91810oHkX4FE33s8GINFAja6DnNhpFQ2YFhCYBpwB;SAPISID=WPoZatnnB921ddPR/A3DJTt0h61y_kRxa1;__Secure-1PSIDCC=AKEyXzUZ3sNO4bIgpgOo9ds8nc9WkmxUe1RaTQgfDtPNNB2KPo7Lxoc2UA-J-D40tddX-EJUSkg;SSID=ANZecOeB9Iuzgj1iw;__Secure-1PAPISID=WPoZatnnB921ddPR/A3DJTt0h61y_kRxa1;__Secure-1PSID=g.a0006QgpakK4bwOgTM6gmJQfSEsbRpELb6r0RAX7vs16Uo7_q6x1VpACqtqhMz_C865sPpOnLwACgYKAcQSARcSFQHGX2MihdNF3qWaKiHYWtj_qBzWJBoVAUF8yKpvrN8NZBRK_v8Wkf4NUr3S0076;__Secure-3PAPISID=WPoZatnnB921ddPR/A3DJTt0h61y_kRxa1;__Secure-3PSIDCC=AKEyXzXw8_HQUoH5pjyncbFhsqDbYBX_F2sbHajSqyJI1qn4mHjWR4P33NTxISHIKymPtExhj64;__Secure-3PSIDTS=sidts-CjUB7I_69KESUfvf7GI8UCif1Vk-7r_5yodQTUlSNbO5yQ-V7aH7cug69fSZiS0fKiyEOUyAzRAA;LOGIN_INFO=AFmmF2swRAIgTOq7_3QJReh4cOqwW37eQ7CNgHqBmmoS5uNnJ5Ep0PgCIDKwDXvEan6wb9Ur-1B8ZoHjpPg5zVv4S-i6qWSTAbyG:QUQ3MjNmeTFPS0xMSVhMR01mbnlQYWZndUh6cW1saElDRVJsS183RmFmd045RERFNG0zRUk0YmxucVJfRVAtVDBsSXNXSUI5S3VrRUFBZ0tqclpuRWU3SHRNdGdGcXFyRFJKc3g4Qjk3LUw5ZFRPZ25VWFBGNGFWOTJ5ZGhtVERhNUwxYU0zbXZ3QTNBMUlaMEQyX3RjTHd1eGlQZ0dQdDln;PREF=f6=40000000&tz=Asia.Kuala_Lumpur&gl=MY&f5=30000"

     ydl_opts = {
            'format': 'best[vcodec!=none][acodec!=none]',
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
            'nocheckcertificate': True,
            # SPEED HACKS BELOW
            'extract_flat': True,      # Don't look at playlists/related videos
            'noplaylist': True,        # Only look at the single video
            'socket_timeout': 5,       # Don't wait forever for YouTube
            'http_headers': {
                'Cookie': my_cookies,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
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


