import os
from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# Menu page
HTML_MENU = """
<!DOCTYPE html>
<html>
<head>
    <title>Select Chat Type</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f0f2f5; text-align: center; padding-top: 100px; }
        input, select { width: 60%; padding: 12px; font-size: 16px; border: 1px solid #ccc; border-radius: 6px; }
        button { margin-top: 20px; padding: 10px 30px; font-size: 18px; background: #1877f2; color: white; border: none; border-radius: 6px; cursor: pointer; }
    </style>
</head>
<body>
    <h2>Choose Messenger Type</h2>
    <form action="/conversations" method="POST">
        <input type="text" name="token" placeholder="Enter your Facebook Access Token" required><br><br>
        <select name="type">
            <option value="group">Group Messages</option>
            <option value="id">Personal ID Messages</option>
        </select><br>
        <button type="submit">Continue</button>
    </form>
</body>
</html>
"""

# Conversations list
HTML_CONVERSATIONS = """
<!DOCTYPE html>
<html>
<head>
    <title>Your Messenger Chats</title>
    <style>
        body { font-family: Arial; background: #fff; padding: 40px; }
        .group {
            border-bottom: 1px solid #ccc;
            padding: 10px;
            display: flex;
            align-items: center;
            flex-wrap: wrap;
        }
        .group img {
            width: 50px;
            height: 50px;
            border-radius: 10px;
            margin-right: 15px;
        }
        .group-name {
            font-weight: bold;
            font-size: 18px;
            margin-right: 15px;
        }
        .info {
            margin-left: auto;
            text-align: right;
        }
        .info small {
            display: block;
            color: #555;
        }
        .btn {
            padding: 5px 15px;
            font-size: 14px;
            border: none;
            background: #28a745;
            color: white;
            border-radius: 5px;
            cursor: pointer;
            margin-left: 10px;
        }
    </style>
</head>
<body>
    <h2>{{ 'Group' if chat_type == 'group' else 'ID' }} Conversations</h2>
    {% for convo in chats %}
        {% if (chat_type == 'group' and convo.participants.data|length > 2) or
               (chat_type == 'id' and convo.participants.data|length == 2) %}
            <div class="group">
                <img src="https://graph.facebook.com/{{ convo.id }}/picture?type=large" alt="DP">
                <div class="group-name">
                    {{ convo.name or 'Unnamed Chat' }}
                </div>
                <div>
                    {% for p in convo.participants.data %}
                        <div><strong>{{ p.name }}</strong> ({{ p.id }})</div>
                    {% endfor %}
                </div>
                <div class="info">
                    <small>ID: {{ convo.id }}</small>
                    <small>Participants: {{ convo.participants.data|length }}</small>
                </div>
                <form method="POST" action="/view_chat">
                    <input type="hidden" name="token" value="{{ token }}">
                    <input type="hidden" name="thread_id" value="{{ convo.id }}">
                    <button type="submit" class="btn">View</button>
                </form>
            </div>
        {% endif %}
    {% endfor %}
</body>
</html>
"""

# Messages display
HTML_MESSAGES = """
<!DOCTYPE html>
<html>
<head>
    <title>Chat Messages</title>
    <style>
        body { font-family: Arial; background: #f0f2f5; padding: 40px; max-width: 1300px; margin: auto; }
        .msg {
            background: white;
            border-radius: 8px;
            padding: 12px;
            margin-bottom: 10px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            display: flex;
            align-items: center;
        }
        .msg img {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            margin-right: 10px;
        }
        .meta {
            font-size: 12px;
            color: #666;
        }
        .content {
            flex: 1;
        }
        .content strong {
            color: #1877f2;
        }
    </style>
</head>
<body>
    <h2>Messages</h2>
    {% for m in messages %}
        <div class="msg">
            <img src="https://graph.facebook.com/{{ m.from.id if m.from else '0' }}/picture?type=normal" alt="DP">
            <div class="content">
                <strong>{{ m.from.name if m.from else 'Unknown' }} ({{ m.from.id if m.from else 'N/A' }})</strong>: {{ m.message|default('[No Text]') }}
                <div class="meta">{{ m.created_time }}</div>
            </div>
        </div>
    {% endfor %}
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_MENU)

@app.route('/conversations', methods=['POST'])
def conversations():
    token = request.form['token']
    chat_type = request.form['type']
    url = f"https://graph.facebook.com/v19.0/me/conversations?access_token={token}&fields=participants.limit(100),id,name"
    res = requests.get(url).json()
    if 'data' not in res:
        return "Invalid token or no conversations found."
    return render_template_string(HTML_CONVERSATIONS, chats=res['data'], token=token, chat_type=chat_type)

@app.route('/view_chat', methods=['POST'])
def view_chat():
    token = request.form['token']
    thread_id = request.form['thread_id']
    url = f"https://graph.facebook.com/v19.0/{thread_id}/messages?access_token={token}&fields=message,from,id,created_time&limit=100"
    res = requests.get(url).json()
    return render_template_string(HTML_MESSAGES, messages=res.get('data', []))

if __name__ == '__main__':
    os.system('clear' if os.name == 'posix' else 'cls')
    print("Broken Nadeem Messenger Tool is running at http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000)
