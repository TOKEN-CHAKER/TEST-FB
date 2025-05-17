# file: termux_messenger_viewer.py
import os
from flask import Flask, redirect, request, session, render_template_string
import requests

app = Flask(__name__)
app.secret_key = 'broken_nadeem_secret_key'

# Replace with your real credentials
FB_APP_ID = 'YOUR_FB_APP_ID'
FB_APP_SECRET = 'YOUR_FB_APP_SECRET'
REDIRECT_URI = 'http://127.0.0.1:5000/callback'

INDEX_HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>Facebook Login</title>
  <style>
    body { width: 1200px; margin: auto; font-family: Arial; text-align: center; padding-top: 100px; }
    button { font-size: 24px; padding: 15px 40px; background-color: #1877f2; color: white; border: none; border-radius: 8px; cursor: pointer; }
  </style>
</head>
<body>
  <h1>Login to Facebook</h1>
  <a href="/login"><button>LOGIN FACEBOOK</button></a>
</body>
</html>
"""

MESSENGER_HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>Messenger Viewer</title>
  <style>
    body { width: 1200px; margin: auto; font-family: sans-serif; }
    .message { border-bottom: 1px solid #ccc; padding: 12px; }
    .meta { font-size: 12px; color: gray; }
    h2 { margin-top: 30px; color: #1877f2; }
  </style>
</head>
<body>
  <h2>Messenger Messages</h2>
  {% for chat in chats %}
    {% if chat.messages %}
      {% for msg in chat.messages.data %}
        <div class="message">
          <strong>{{ msg.from.name if msg.from else "Unknown" }}</strong>: {{ msg.message }}<br>
          <span class="meta">{{ msg.created_time }}</span>
        </div>
      {% endfor %}
    {% endif %}
  {% endfor %}
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(INDEX_HTML)

@app.route('/login')
def login():
    fb_oauth_url = (
        f'https://www.facebook.com/v19.0/dialog/oauth'
        f'?client_id={FB_APP_ID}&redirect_uri={REDIRECT_URI}'
        f'&scope=email,public_profile,user_posts,user_messages'
    )
    return redirect(fb_oauth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_url = (
        f'https://graph.facebook.com/v19.0/oauth/access_token'
        f'?client_id={FB_APP_ID}&redirect_uri={REDIRECT_URI}'
        f'&client_secret={FB_APP_SECRET}&code={code}'
    )
    token_response = requests.get(token_url).json()
    access_token = token_response.get('access_token')
    
    if not access_token:
        return "Failed to retrieve access token."

    session['access_token'] = access_token
    return redirect('/messenger')

@app.route('/messenger')
def messenger():
    token = session.get('access_token')
    if not token:
        return redirect('/')

    convo_url = (
        f'https://graph.facebook.com/v19.0/me/conversations'
        f'?access_token={token}&fields=messages{{message,created_time,from}}'
    )
    response = requests.get(convo_url).json()
    chats = response.get('data', [])

    return render_template_string(MESSENGER_HTML, chats=chats)

if __name__ == '__main__':
    os.system('clear')
    print("Broken Nadeem Messenger Tool is running on http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000)
