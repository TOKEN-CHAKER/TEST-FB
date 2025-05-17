import os
from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# HTML form to input token
HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>Enter Access Token</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f0f2f5; text-align: center; padding-top: 100px; }
        input { width: 60%; padding: 12px; font-size: 16px; border: 1px solid #ccc; border-radius: 6px; }
        button { margin-top: 20px; padding: 10px 30px; font-size: 18px; background: #1877f2; color: white; border: none; border-radius: 6px; cursor: pointer; }
    </style>
</head>
<body>
    <h2>Enter Your Facebook Access Token</h2>
    <form action="/groups" method="POST">
        <input type="text" name="token" placeholder="Paste your access token..." required>
        <br>
        <button type="submit">View Messenger Groups</button>
    </form>
</body>
</html>
"""

# HTML to list messenger groups with all profile photos
HTML_GROUPS = """
<!DOCTYPE html>
<html>
<head>
    <title>Your Messenger Groups</title>
    <style>
        body { font-family: Arial; background: #fff; padding: 40px; }
        .group {
            border: 1px solid #ddd;
            border-radius: 8px;
            margin-bottom: 15px;
            padding: 15px;
            display: flex;
            align-items: center;
            background: #f9f9f9;
        }
        .photos {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-right: 20px;
        }
        .photos img {
            border-radius: 50%;
            width: 40px;
            height: 40px;
        }
        .info {
            flex: 1;
        }
        .info strong {
            display: block;
            margin-bottom: 5px;
        }
        form {
            margin-left: 20px;
        }
        button {
            padding: 6px 16px;
            font-size: 14px;
            background: #28a745;
            color: white;
            border: none;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <h2>Your Messenger Group Chats</h2>
    {% for convo in groups %}
        {% if convo.participants.data|length > 2 %}
            <div class="group">
                <div class="photos">
                    {% for user in convo.participants.data %}
                        <img src="https://graph.facebook.com/{{ user.id }}/picture?type=normal" title="{{ user.name }}" alt="DP">
                    {% endfor %}
                </div>
                <div class="info">
                    <strong>Group ID:</strong> {{ convo.id }}
                    <strong>Participants:</strong> {{ convo.participants.data|length }}
                </div>
                <form method="POST" action="/group_chat">
                    <input type="hidden" name="token" value="{{ token }}">
                    <input type="hidden" name="thread_id" value="{{ convo.id }}">
                    <button type="submit">Open Chat</button>
                </form>
            </div>
        {% endif %}
    {% endfor %}
</body>
</html>
"""

# HTML for showing group messages
HTML_MESSAGES = """
<!DOCTYPE html>
<html>
<head>
    <title>Group Messages</title>
    <style>
        body { font-family: Arial; background: #f0f2f5; padding: 40px; }
        .msg {
            background: white;
            border-radius: 8px;
            padding: 12px;
            margin-bottom: 10px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        .msg strong { color: #1877f2; }
        .meta { font-size: 13px; color: #555; margin-top: 4px; }
    </style>
</head>
<body>
    <h2>Group Messages</h2>
    {% for m in messages %}
        <div class="msg">
            <strong>{{ m.from.name if m.from else 'Unknown' }}</strong>: {{ m.message|default('[No Text]') }}
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
    print("Broken Nadeem Messenger Viewer is running at http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000)
