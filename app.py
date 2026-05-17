from flask import Flask, request, jsonify, render_template_string
from groq import Groq
import os

app = Flask(__name__)

SYSTEM = """You are NEXUS AI — advanced AI. Bilingual Myanmar/English. Expert in Networking, Cybersecurity, GED, English, Coding, General knowledge. Auto-detect language."""

HTML = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NEXUS AI</title>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { background:#050a0e; color:#c8dde8; font-family:Arial,sans-serif; display:flex; flex-direction:column; height:100vh; }
.header { background:#0a1520; padding:14px 16px; border-bottom:1px solid rgba(0,212,255,0.2); }
.header h1 { color:#00d4ff; font-size:18px; letter-spacing:2px; }
.header p { color:#3a5a6a; font-size:11px; margin-top:2px; }
#messages { flex:1; overflow-y:auto; padding:16px; display:flex; flex-direction:column; gap:12px; }
.msg-user { align-self:flex-end; background:rgba(255,107,53,0.1); border:1px solid rgba(255,107,53,0.25); padding:10px 14px; border-radius:16px 4px 16px 16px; max-width:80%; font-size:14px; line-height:1.6; }
.msg-ai { align-self:flex-start; background:rgba(0,212,255,0.07); border:1px solid rgba(0,212,255,0.2); padding:10px 14px; border-radius:4px 16px 16px 16px; max-width:85%; font-size:14px; line-height:1.7; white-space:pre-wrap; }
.typing { align-self:flex-start; padding:12px 16px; color:#00d4ff; font-size:13px; }
.input-area { padding:12px; background:#0a1520; border-top:1px solid rgba(0,212,255,0.2); display:flex; gap:8px; }
#userInput { flex:1; background:#050a0e; border:1px solid rgba(0,212,255,0.3); border-radius:20px; padding:10px 16px; color:#c8dde8; font-size:15px; outline:none; }
#userInput:focus { border-color:#00d4ff; }
#sendBtn { background:rgba(0,212,255,0.2); border:1px solid #00d4ff; border-radius:50%; width:42px; height:42px; color:#00d4ff; font-size:18px; cursor:pointer; }
#sendBtn:active { background:rgba(0,212,255,0.4); }
</style>
</head>
<body>
<div class="header">
  <h1>⚡ NEXUS AI</h1>
  <p>Networking · CyberSec · GED · English · Coding</p>
</div>
<div id="messages">
  <div class="msg-ai">မင်္ဂလာပါ! ငါ NEXUS AI ပါ။ မေးချင်တာ မေးပါ 🤖<br><br>Hello! I am NEXUS AI. Ask me anything about Networking, Cybersecurity, GED, English, or Coding!</div>
</div>
<div class="input-area">
  <input type="text" id="userInput" placeholder="မေးချင်တာ ရိုက်ပါ..." />
  <button id="sendBtn" onclick="sendMsg()">➤</button>
</div>

<script>
document.getElementById('userInput').addEventListener('keypress', function(e) {
  if (e.key === 'Enter') sendMsg();
});

var history = [];
var busy = false;

function sendMsg() {
  if (busy) return;
  var input = document.getElementById('userInput');
  var text = input.value.trim();
  if (!text) return;

  busy = true;
  input.value = '';

  var msgs = document.getElementById('messages');

  var userDiv = document.createElement('div');
  userDiv.className = 'msg-user';
  userDiv.textContent = text;
  msgs.appendChild(userDiv);

  var typingDiv = document.createElement('div');
  typingDiv.className = 'typing';
  typingDiv.id = 'typing';
  typingDiv.textContent = 'NEXUS AI တွေးနေသည်...';
  msgs.appendChild(typingDiv);

  msgs.scrollTop = msgs.scrollHeight;

  history.push({role: 'user', content: text});

  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/chat', true);
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.onreadystatechange = function() {
    if (xhr.readyState === 4) {
      var td = document.getElementById('typing');
      if (td) td.remove();
      busy = false;
      if (xhr.status === 200) {
        var data = JSON.parse(xhr.responseText);
        var aiDiv = document.createElement('div');
        aiDiv.className = 'msg-ai';
        if (data.reply) {
          aiDiv.textContent = data.reply;
          history.push({role: 'assistant', content: data.reply});
        } else {
          aiDiv.textContent = 'Error: ' + (data.error || 'Unknown error');
        }
        msgs.appendChild(aiDiv);
      } else {
        var errDiv = document.createElement('div');
        errDiv.className = 'msg-ai';
        errDiv.textContent = 'Error: ' + xhr.status;
        msgs.appendChild(errDiv);
      }
      msgs.scrollTop = msgs.scrollHeight;
    }
  };
  xhr.send(JSON.stringify({history: history}));
}
</script>
</body>
</html>"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        api_key = os.environ.get('GROQ_API_KEY', '')
        if not api_key:
            return jsonify({'error': 'API key missing'})
        client = Groq(api_key=api_key)
        data = request.json
        history = data.get('history', [])
        resp = client.chat.completions.create(
            model='llama-3.3-70b-versatile',
            messages=[{'role': 'system', 'content': SYSTEM}] + history,
            max_tokens=1024,
            temperature=0.7,
            timeout=25,
)
        return jsonify({'reply': resp.choices[0].message.content})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
