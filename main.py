import os
from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# Facebook-style Token Input Page
HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>Facebook Token Login</title>
    <style>
        body { font-family: Helvetica, Arial, sans-serif; background: #e9ebee; display: flex; justify-content: center; align-items: center; height: 100vh; }
        .card {
            background: #fff;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.1);
            width: 400px;
            text-align: center;
        }
        .card h2 {
            color: #1877f2;
            margin-bottom: 20px;
        }
        input[type="text"] {
            width: 100%;
            padding: 14px;
            font-size: 16px;
            border: 1px solid #ddd;
            border-radius: 6px;
            margin-top: 10px;
        }
        button {
            width: 100%;
            margin-top: 20px;
            padding: 12px;
            font-size: 16px;
            background-color: #1877f2;
            border: none;
            border-radius: 6px;
            color: white;
            font-weight: bold;
            cursor: pointer;
        }
        button:hover {
            background-color: #165ecb;
        }
    </style>
</head>
<body>
    <div class="card">
        <h2>Facebook Messenger Viewer</h2>
        <form action="/groups" method="POST">
            <input type="text" name="token" placeholder="Enter your access token" required>
            <button type="submit">View Conversations</button>
        </form>
    </div>
</body>
</html>
"""

# Facebook-style Messenger Group List Page
HTML_GROUPS = """
<!DOCTYPE html>
<html>
<head>
    <title>Your Messenger Groups</title>
    <style>
        body { font-family: Helvetica, Arial, sans-serif; background: #f5f6f7; padding: 40px; }
        h2 { color: #1877f2; }
        .group {
            background: #fff;
            border-radius: 8px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.1);
            padding: 15px;
            display: flex;
            align-items: center;
            margin-bottom: 15px;
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
            background: #1877f2;
            color: white;
            border-radius: 5px;
            cursor: pointer;
            margin-left: 10px;
        }
        .btn:hover {
            background-color: #165ecb;
        }
    </style>
</head>
<body>
    <h2>Your Messenger Group Chats</h2>
    {% for convo in groups %}
        {% if convo.participants.data|length > 2 %}
            <div class="group">
                <img src="https://graph.facebook.com/{{ convo.id }}/picture?type=large" alt="Group DP">
                <div class="group-name">
                    {{ convo.name or 'Unnamed Group' }}
                </div>
                <div class="info">
                    <small>ID: {{ convo.id }}</small>
                    <small>Participants: {{ convo.participants.data|length }}</small>
                </div>
                <form method="POST" action="/group_chat">
                    <input type="hidden" name="token" value="{{ token }}">
                    <input type="hidden" name="thread_id" value="{{ convo.id }}">
                    <input type="hidden" name="group_name" value="{{ convo.name or 'Unnamed Group' }}">
                    <button type="submit" class="btn">View</button>
                </form>
            </div>
        {% endif %}
    {% endfor %}
</body>
</html>
"""

# Facebook-style Message Viewer
HTML_MESSAGES = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ group_name }}</title>
    <style>
        body { font-family: Helvetica, Arial, sans-serif; background: #f0f2f5; margin: 0; padding: 20px; }
        h3 { color: #1877f2; }
        .scroll-box {
            max-height: 100vh;
            overflow-y: auto;
            padding: 10px;
            background: #fff;
            border-radius: 10px;
            box-shadow: 0 0 5px rgba(0,0,0,0.1);
        }
        .msg {
            border-bottom: 1px solid #eee;
            padding: 8px 5px;
            margin-bottom: 6px;
        }
        .header {
            display: flex;
            align-items: center;
            font-size: 14px;
            font-weight: bold;
            color: #1877f2;
            margin-bottom: 3px;
        }
        .header img {
            width: 28px;
            height: 28px;
            border-radius: 50%;
            margin-right: 10px;
        }
        .header .name-id {
            display: flex;
            flex-direction: column;
        }
        .name-id .name {
            line-height: 1;
        }
        .name-id .userid {
            font-size: 11px;
            color: #555;
        }
        .message-text {
            font-size: 14px;
            margin-left: 38px;
            white-space: pre-wrap;
            word-wrap: break-word;
            color: #222;
        }
        .timestamp {
            font-size: 11px;
            color: #888;
            margin-left: 38px;
            margin-top: 3px;
        }
    </style>
</head>
<body>
    <h3>{{ group_name }}</h3>
    <div class="scroll-box">
        {% for m in messages %}
            <div class="msg">
                <div class="header">
                    <img src="https://graph.facebook.com/{{ m.from.id if m.from else '0' }}/picture?type=normal" alt="profile-pic">
                    <div class="name-id">
                        <div class="name">{{ m.from.name if m.from else 'Unknown' }}</div>
                        <div class="userid">ID: {{ m.from.id if m.from else 'Unknown' }}</div>
                    </div>
                </div>
                <div class="message-text">{{ m.message|default('[No Text]') }}</div>
                <div class="timestamp">{{ m.created_time }}</div>
            </div>
        {% endfor %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML_FORM)

@app.route('/groups', methods=['POST'])
def groups():
    token = request.form['token']
    url = f"https://graph.facebook.com/v19.0/me/conversations?access_token={token}&fields=participants.limit(100),id,name"
    res = requests.get(url).json()
    if 'data' not in res:
        return "<h3 style='color:red;text-align:center;'>Invalid token or no group data found.</h3>"
    return render_template_string(HTML_GROUPS, groups=res['data'], token=token)

@app.route('/group_chat', methods=['POST'])
def group_chat():
    token = request.form['token']
    thread_id = request.form['thread_id']
    group_name = request.form.get('group_name', 'Group Messages')
    url = f"https://graph.facebook.com/v19.0/{thread_id}/messages?access_token={token}&fields=message,from,id,created_time&limit=3000"
    res = requests.get(url).json()
    return render_template_string(HTML_MESSAGES, messages=res.get('data', []), group_name=group_name)

if __name__ == '__main__':
    os.system('clear' if os.name == 'posix' else 'cls')
    print("Broken Nadeem Messenger Viewer is running at http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000)
