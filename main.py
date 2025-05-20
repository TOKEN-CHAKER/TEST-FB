from flask import Flask, request, send_file, render_template_string
import yt_dlp
import os

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Broken Nadeem 4K Video Tool</title>
    <style>
        body {
            background-color: #000;
            color: #0f0;
            font-family: monospace;
            text-align: center;
            padding: 40px;
        }
        input, button {
            padding: 12px;
            font-size: 18px;
            width: 70%;
            border-radius: 10px;
            border: none;
            margin: 10px;
        }
        video {
            width: 90%;
            margin-top: 20px;
            border: 4px solid #0f0;
            border-radius: 10px;
        }
    </style>
</head>
<body>
    <h1>Broken Nadeem Full HD 4K Video Tool</h1>
    <form method="POST">
        <input type="text" name="video_url" placeholder="Paste video URL here..." required>
        <br>
        <button type="submit">Play Full HD Video</button>
    </form>

    {% if stream_url %}
        <h2>{{ video_info.title }}</h2>
        <video controls autoplay>
            <source src="{{ stream_url }}" type="video/mp4">
            Your browser does not support the video tag.
        </video>
        <form method="POST" action="/download">
            <input type="hidden" name="url" value="{{ video_url }}">
            <button type="submit">Download 4K Video</button>
        </form>
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    video_url = None
    video_info = None
    stream_url = None
    if request.method == 'POST':
        video_url = request.form['video_url']
        try:
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
                'quiet': True,
                'noplaylist': True
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)
                stream_url = info['url']
                video_info = info
        except Exception as e:
            return f"<h3>Error: {str(e)}</h3>"
    return render_template_string(HTML, video_url=video_url, stream_url=stream_url, video_info=video_info)

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': 'video.%(ext)s'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
