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

# HTML to list messenger groups
HTML_GROUPS = """
<!DOCTYPE html>
<html>
<head>
    <title>Your Messenger Groups</title>
    <style>
        body { font-family: Arial; background: #fff; padding: 40px; }
        .group {
            border-bottom: 1px solid #ccc;
            padding: 10px;
            display: flex;
            align-items: center;
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
            background: #28a745;
            color: white;
            border-radius: 5px;
            cursor: pointer;
            margin-left: 10px;
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
                    <select name="limit">
                        <option value="100">100</option>
                        <option value="500">500</option>
                        <option value="1000">1000</option>
                        <option value="1800" selected>1800</option>
                    </select>
                    <button type="submit" class="btn">View</button>
                </form>
            </div>
        {% endif %}
    {% endfor %}
</body>
</html>
"""

# HTML to display messages
HTML_MESSAGES = """
<!DOCTYPE html>
<html>
<head>
    <title>Group Messages</title>
    <style>
        body { font-family: Arial; background: #f0f2f5; padding: 40px; }
        .scroll-box {
            max-height: 200vh;
            overflow-y: auto;
            border: 1px solid #ccc;
            border-radius: 10px;
            padding: 20px;
            background: #ffffff;
        }
        .msg {
            background: #fff;
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
            margin-top: 4px;
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
    <h2>Group Messages (Total: {{ messages|length }})</h2>
    <div class="scroll-box">
        {% for m in messages %}
            <div class="msg">
                <img src="https://graph.facebook.com/{{ m.from.id if m.from else '0' }}/picture?type=normal" alt="DP">
                <div class="content">
                    <strong>{{ m.from.name if m.from else 'Unknown' }} ({{ m.from.id if m.from else 'N/A' }})</strong>: {{ m.message|default('[No Text]') }}
                    <div class="meta">{{ m.created_time }}</div>
                </div>
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
        return "Invalid token or no group data found."
    return render_template_string(HTML_GROUPS, groups=res['data'], token=token)

@app.route('/group_chat', methods=['POST'])
def group_chat():
    token = request.form['token']
    thread_id = request.form['thread_id']
    limit = request.form.get('limit', '1800')
    url = f"https://graph.facebook.com/v19.0/{thread_id}/messages?access_token={token}&fields=message,from,id,created_time&limit={limit}"
    res = requests.get(url).json()
    return render_template_string(HTML_MESSAGES, messages=res.get('data', []))

if __name__ == '__main__':
    os.system('clear')
    print("🚀 Broken Nadeem Messenger Viewer running at http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000)
