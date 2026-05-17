from flask import Flask, request, jsonify, render_template_string
from dotenv import load_dotenv
from groq import Groq
from pathlib import Path
import os

load_dotenv(Path.home() / ".nexus-ai.env")
API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=API_KEY)
app = Flask(__name__)
MODEL = "llama-3.3-70b-versatile"

SYSTEM = """You are NEXUS AI — the most advanced personal AI assistant with complete mastery of ALL fields:
NETWORKING: OSI model, TCP/IP, IPv4/IPv6, subnetting, routing (OSPF/BGP/EIGRP), switching (VLANs/STP), DNS/DHCP, VPN (IPSec/OpenVPN/WireGuard), firewalls, Wireshark, Cisco IOS, cloud networking.
CYBERSECURITY: Penetration testing, recon (OSINT/Shodan), Nmap, Metasploit, web attacks (SQLi/XSS/SSRF/IDOR), privilege escalation, AD attacks (Kerberoasting/Pass-the-Hash), forensics, SIEM, CTF. Educational/ethical only.
GED: Math (algebra/geometry/stats), Science, RLA (reading/grammar/writing), Social Studies. Step-by-step teaching.
ENGLISH: All grammar, vocabulary, idioms, writing, IELTS/TOEFL prep. Compare with Myanmar when helpful.
CODING: Python, Bash, C++, JavaScript, SQL, algorithms, data structures, Linux, git, docker.
GENERAL: Mathematics, physics, chemistry, biology, history, economics — everything.
LANGUAGE RULE: Auto-detect language. Myanmar input → Myanmar response. English input → English response. Be like a brilliant professor."""

HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<meta name="theme-color" content="#050a0e">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="NEXUS AI">
<link rel="manifest" href="/manifest.json">
<title>NEXUS AI</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
:root{--bg:#050a0e;--bg2:#0a1520;--accent:#00d4ff;--accent2:#00ff9d;--text:#c8dde8;--dim:#3a5a6a;--border:rgba(0,212,255,.18)}
body{background:var(--bg);color:var(--text);font-family:'Segoe UI',system-ui,sans-serif;height:100dvh;display:flex;flex-direction:column;overflow:hidden}
.header{background:var(--bg2);border-bottom:1px solid var(--border);padding:12px 16px;display:flex;align-items:center;gap:12px;flex-shrink:0}
.logo{font-size:20px;font-weight:900;color:var(--accent);letter-spacing:3px;font-family:monospace}
.sub{font-size:10px;color:var(--dim);letter-spacing:1px;margin-top:2px}
.dot{width:8px;height:8px;border-radius:50%;background:var(--accent2);box-shadow:0 0 8px var(--accent2);animation:bl 1.5s infinite;margin-left:auto}
@keyframes bl{0%,100%{opacity:1}50%{opacity:.3}}
.msgs{flex:1;overflow-y:auto;padding:14px;display:flex;flex-direction:column;gap:12px;scroll-behavior:smooth}
.msgs::-webkit-scrollbar{width:3px}
.msgs::-webkit-scrollbar-thumb{background:var(--border);border-radius:2px}
.welcome{text-align:center;padding:30px 16px;color:var(--dim)}
.welcome .w-logo{font-size:48px;margin-bottom:12px;animation:fl 3s ease-in-out infinite}
@keyframes fl{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
.welcome h2{color:var(--accent);font-family:monospace;letter-spacing:3px;font-size:18px;margin-bottom:6px}
.welcome p{font-size:13px;line-height:1.7;color:var(--dim)}
.caps{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:16px}
.cap{background:rgba(0,212,255,.04);border:1px solid var(--border);border-radius:8px;padding:10px 8px;text-align:center}
.cap .ci{font-size:20px;margin-bottom:4px}
.cap .ct{font-size:10px;color:var(--accent);font-weight:600;letter-spacing:.5px}
.msg{display:flex;gap:8px;animation:fi .25s ease}
@keyframes fi{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}
.msg.user{flex-direction:row-reverse}
.av{width:32px;height:32px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:15px;flex-shrink:0}
.msg.user .av{background:rgba(255,107,53,.12);border:1px solid rgba(255,107,53,.25)}
.msg.assistant .av{background:rgba(0,212,255,.1);border:1px solid var(--border)}
.bub{max-width:82%;padding:10px 14px;border-radius:12px;font-size:14px;line-height:1.75;word-break:break-word}
.msg.user .bub{background:rgba(255,107,53,.08);border:1px solid rgba(255,107,53,.18);border-radius:12px 4px 12px 12px}
.msg.assistant .bub{background:rgba(0,212,255,.05);border:1px solid var(--border);border-radius:4px 12px 12px 12px}
.bub pre{background:rgba(0,0,0,.6);border:1px solid var(--border);border-radius:6px;padding:10px;overflow-x:auto;margin:8px 0;font-family:monospace;font-size:12px;color:var(--accent2);line-height:1.5;white-space:pre-wrap}
.bub code{font-family:monospace;background:rgba(0,0,0,.5);padding:1px 5px;border-radius:3px;color:var(--accent2);font-size:12px}
.td{display:flex;gap:4px;padding:6px}
.td span{width:6px;height:6px;border-radius:50%;background:var(--accent);animation:bo 1s infinite}
.td span:nth-child(2){animation-delay:.2s}
.td span:nth-child(3){animation-delay:.4s}
@keyframes bo{0%,60%,100%{transform:translateY(0);opacity:.4}30%{transform:translateY(-5px);opacity:1}}
.inp-area{background:var(--bg2);border-top:1px solid var(--border);padding:10px 12px;flex-shrink:0;padding-bottom:max(10px,env(safe-area-inset-bottom))}
.inp-row{display:flex;gap:8px;align-items:flex-end;background:var(--bg);border:1px solid var(--border);border-radius:24px;padding:8px 8px 8px 16px;transition:border-color .2s}
.inp-row:focus-within{border-color:rgba(0,212,255,.5)}
textarea{flex:1;background:transparent;border:none;outline:none;color:var(--text);font-size:15px;font-family:inherit;resize:none;max-height:100px;line-height:1.5;padding-top:2px}
textarea::placeholder{color:var(--dim)}
.send{width:36px;height:36px;background:linear-gradient(135deg,rgba(0,212,255,.3),rgba(0,255,157,.15));border:1px solid rgba(0,212,255,.4);border-radius:50%;color:var(--accent);cursor:pointer;font-size:16px;display:flex;align-items:center;justify-content:center;transition:all .2s;flex-shrink:0}
.send:active{transform:scale(.92)}
.send:disabled{opacity:.4;cursor:not-allowed}
@media(max-width:480px){.caps{grid-template-columns:repeat(2,1fr)}.bub{max-width:88%}}
</style>
</head>
<body>
<div class="header">
  <div>
    <div class="logo">⚡ NEXUS AI</div>
    <div class="sub">NETWORKING · CYBERSEC · GED · ENGLISH · CODING</div>
  </div>
  <div class="dot"></div>
</div>
<div class="msgs" id="msgs">
  <div class="welcome">
    <div class="w-logo">🤖</div>
    <h2>NEXUS AI ONLINE</h2>
    <p>မြန်မာ + English နှစ်ဘာသာ<br>မေးချင်တာ မေးပါ — အကုန်သိတဲ့ AI</p>
    <div class="caps">
      <div class="cap"><div class="ci">🌐</div><div class="ct">Network</div></div>
      <div class="cap"><div class="ci">🛡️</div><div class="ct">CyberSec</div></div>
      <div class="cap"><div class="ci">📚</div><div class="ct">GED</div></div>
      <div class="cap"><div class="ci">🔤</div><div class="ct">English</div></div>
      <div class="cap"><div class="ci">💻</div><div class="ct">Coding</div></div>
      <div class="cap"><div class="ci">🧠</div><div class="ct">General</div></div>
    </div>
  </div>
</div>
<div class="inp-area">
  <div class="inp-row">
    <textarea id="inp" rows="1" placeholder="မေးချင်တာ မေးပါ... / Ask anything..."
      onkeydown="hk(event)" oninput="rs(this)"></textarea>
    <button class="send" id="sb" onclick="send()">➤</button>
  </div>
</div>
<script>
let hist=[],busy=false;
function rs(el){el.style.height='auto';el.style.height=Math.min(el.scrollHeight,100)+'px'}
function hk(e){if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();send()}}
function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}
function fmt(t){
  t=esc(t);
  t=t.replace(/```[\w]*\n?([\s\S]*?)```/g,'<pre><code>$1</code></pre>');
  t=t.replace(/`([^`\n]+)`/g,'<code>$1</code>');
  t=t.replace(/\*\*(.*?)\*\*/g,'<strong>$1</strong>');
  t=t.replace(/\n/g,'<br>');
  return t;
}
function addMsg(role,text){
  document.querySelector('.welcome')?.remove();
  const m=document.getElementById('msgs');
  const d=document.createElement('div');
  d.className='msg '+role;
  const av=role==='user'?'👤':'🤖';
  d.innerHTML=`<div class="av">${av}</div><div class="bub">${fmt(text)}</div>`;
  m.appendChild(d);
  m.scrollTop=m.scrollHeight;
}
function addTyping(){
  document.querySelector('.welcome')?.remove();
  const m=document.getElementById('msgs');
  const d=document.createElement('div');
  d.id='td';d.className='msg assistant';
  d.innerHTML='<div class="av">🤖</div><div class="bub"><div class="td"><span></span><span></span><span></span></div></div>';
  m.appendChild(d);m.scrollTop=m.scrollHeight;
}
async function send(){
  if(busy)return;
  const inp=document.getElementById('inp');
  const txt=inp.value.trim();
  if(!txt)return;
  busy=true;document.getElementById('sb').disabled=true;
  inp.value='';inp.style.height='auto';
  addMsg('user',txt);
  hist.push({role:'user',content:txt});
  addTyping();
  try{
    const r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({history:hist})});
    const data=await r.json();
    document.getElementById('td')?.remove();
    if(data.error){hist.pop();addMsg('assistant','❌ Error: '+data.error);}
    else{addMsg('assistant',data.reply);hist.push({role:'assistant',content:data.reply});}
  }catch(e){document.getElementById('td')?.remove();hist.pop();addMsg('assistant','❌ Connection error');}
  busy=false;document.getElementById('sb').disabled=false;inp.focus();
}
if('serviceWorker' in navigator){navigator.serviceWorker.register('/sw.js');}
</script>
</body>
</html>'''

from flask import Response
import json

MANIFEST = {
    "name": "NEXUS AI",
    "short_name": "NEXUS AI",
    "description": "Advanced AI — Networking, Cybersec, GED, English, Coding",
    "start_url": "/",
    "display": "standalone",
    "background_color": "#050a0e",
    "theme_color": "#00d4ff",
    "orientation": "portrait-primary",
    "icons": [
        {"src": "/icon.png", "sizes": "192x192", "type": "image/png"},
        {"src": "/icon.png", "sizes": "512x512", "type": "image/png"}
    ]
}

SW = """
self.addEventListener('fetch', e => {
  e.respondWith(fetch(e.request).catch(() => caches.match(e.request)));
});
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/manifest.json')
def manifest():
    return Response(json.dumps(MANIFEST), mimetype='application/json')

@app.route('/sw.js')
def sw():
    return Response(SW, mimetype='application/javascript')

@app.route('/icon.png')
def icon():
    # Simple PNG icon
    import base64
    png = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    return Response(base64.b64decode(png), mimetype='image/png')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    history = data.get('history', [])
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "system", "content": SYSTEM}] + history,
            max_tokens=2048,
            temperature=0.7,
        )
        return jsonify({"reply": resp.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
