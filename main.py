import os
from flask import Flask, request, redirect, render_template_string
import requests

app = Flask(__name__)

HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>Enter Access Token</title>
    <style>
        body { width: 1200px; margin: auto; font-family: Arial; padding-top: 80px; text-align: center; }
        input { width: 60%; padding: 10px; font-size: 18px; }
        button { padding: 10px 30px; font-size: 20px; background: #1877f2; color: white; border: none; border-radius: 6px; }
    </style>
</head>
<body>
    <h2>ENTER YOUR FACEBOOK ACCESS TOKEN</h2>
    <form action="/groups" method="POST">
        <input type="text" name="token" placeholder="Paste your token here..." required>
        <br><br>
        <button type="submit">VIEW MESSENGER GROUPS</button>
    </form>
</body>
</html>
"""

HTML_GROUPS = """
<!DOCTYPE html>
<html>
<head>
    <title>Messenger Group List</title>
    <style>
        body { width: 1200px; margin: auto; font-family: Arial; padding-top: 40px; }
        .group { border-bottom: 1px solid #ccc; padding: 12px; }
        button { padding: 6px 20px; font-size: 16px; background: #28a745; color: white; border: none; border-radius: 5px; }
    </style>
</head>
<body>
    <h2>Your Messenger Group Chats</h2>
    {% for convo in groups %}
        {% if convo.participants.data|length > 2 %}
            <div class="group">
                <strong>Group ID:</strong> {{ convo.id }}<br>
                <strong>Participants:</strong> {{ convo.participants.data|length }}
                <form method="POST" action="/group_chat">
                    <input type="hidden" name="token" value="{{ token }}">
                    <input type="hidden" name="thread_id" value="{{ convo.id }}">
                    <br><button type="submit">Open Chat</button>
                </form>
            </div>
        {% endif %}
    {% endfor %}
</body>
</html>
"""

HTML_MESSAGES = """
<!DOCTYPE html>
<html>
<head>
    <title>Group Messages</title>
    <style>
        body { width: 1200px; margin: auto; font-family: Arial; padding-top: 40px; }
        .msg { border-bottom: 1px solid #ddd; padding: 10px; }
        .meta { font-size: 12px; color: gray; }
        h3 { color: #1877f2; }
    </style>
</head>
<body>
    <h3>Group Messages</h3>
    {% for m in messages %}
        <div class="msg">
            <strong>{{ m.from.name if m.from else 'Unknown' }}</strong>: {{ m.message }}<br>
            <div class="meta">{{ m.created_time }}</div>
        </div>
    {% endfor %}
</body>
</html>
"""

@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML_FORM)

@app.route('/groups', methods=['POST'])
def groups():
    token = request.form['token']
    url = f"https://graph.facebook.com/v19.0/me/conversations?access_token={token}&fields=participants.limit(100),id"
    res = requests.get(url).json()

    if 'data' not in res:
        return "Invalid token or no group data found."

    return render_template_string(HTML_GROUPS, groups=res['data'], token=token)

@app.route('/group_chat', methods=['POST'])
def group_chat():
    token = request.form['token']
    thread_id = request.form['thread_id']
    url = f"https://graph.facebook.com/v19.0/{thread_id}/messages?access_token={token}&fields=message,from,created_time&limit=100"
    res = requests.get(url).json()

    return render_template_string(HTML_MESSAGES, messages=res.get('data', []))

if __name__ == '__main__':
    os.system('clear')
    print("Broken Nadeem Messenger Group Viewer running at http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000)
