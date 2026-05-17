from flask import Flask, request, jsonify, render_template_string, Response
from groq import Groq
import os, json

app = Flask(__name__)
MODEL = "llama-3.3-70b-versatile"

SYSTEM = """You are NEXUS AI — advanced AI assistant. Fully bilingual Myanmar/English. Expert in: Networking (OSI/TCP/IP/subnetting/routing/VPN/Cisco), Cybersecurity (pentesting/Metasploit/web attacks/CTF/Kali tools - ethical only), GED (Math/Science/RLA/Social Studies), English (grammar/writing/IELTS), Coding (Python/Bash/C++/SQL/algorithms), General knowledge. Auto-detect language: Myanmar input = Myanmar reply, English input = English reply."""

HTML = open('/dev/stdin').read() if False else '''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>NEXUS AI</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#050a0e;color:#c8dde8;font-family:system-ui,sans-serif;height:100dvh;display:flex;flex-direction:column;overflow:hidden}
.hdr{background:#0a1520;border-bottom:1px solid rgba(0,212,255,.2);padding:12px 16px;display:flex;align-items:center;justify-content:space-between;flex-shrink:0}
.logo{font-size:18px;font-weight:900;color:#00d4ff;letter-spacing:3px;font-family:monospace}
.sub{font-size:9px;color:#3a5a6a;letter-spacing:1px;margin-top:2px}
.dot{width:8px;height:8px;border-radius:50%;background:#00ff9d;box-shadow:0 0 8px #00ff9d;animation:bl 1.5s infinite}
@keyframes bl{0%,100%{opacity:1}50%{opacity:.3}}
.msgs{flex:1;overflow-y:auto;padding:14px;display:flex;flex-direction:column;gap:12px}
.welcome{text-align:center;padding:40px 16px}
.wi{font-size:50px;animation:fl 3s ease-in-out infinite}
@keyframes fl{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
.wt{color:#00d4ff;font-family:monospace;letter-spacing:3px;font-size:18px;margin:12px 0 8px}
.ws{font-size:13px;color:#3a5a6a;line-height:1.7}
.caps{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:16px;max-width:400px;margin-left:auto;margin-right:auto}
.cap{background:rgba(0,212,255,.04);border:1px solid rgba(0,212,255,.15);border-radius:8px;padding:10px 6px;text-align:center;cursor:pointer;transition:all .2s}
.cap:hover{background:rgba(0,212,255,.1);border-color:#00d4ff}
.ci{font-size:20px;margin-bottom:4px}
.ct{font-size:10px;color:#00d4ff;font-weight:600}
.msg{display:flex;gap:8px;animation:fi .25s ease}
@keyframes fi{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}
.msg.user{flex-direction:row-reverse}
.av{width:32px;height:32px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:15px;flex-shrink:0}
.msg.user .av{background:rgba(255,107,53,.12);border:1px solid rgba(255,107,53,.25)}
.msg.assistant .av{background:rgba(0,212,255,.1);border:1px solid rgba(0,212,255,.25)}
.bub{max-width:82%;padding:10px 14px;border-radius:12px;font-size:14px;line-height:1.75;word-break:break-word;white-space:pre-wrap}
.msg.user .bub{background:rgba(255,107,53,.08);border:1px solid rgba(255,107,53,.18);border-radius:12px 4px 12px 12px}
.msg.assistant .bub{background:rgba(0,212,255,.05);border:1px solid rgba(0,212,255,.15);border-radius:4px 12px 12px 12px}
.bub pre{background:rgba(0,0,0,.6);border:1px solid rgba(0,212,255,.2);border-radius:6px;padding:10px;overflow-x:auto;margin:8px 0;font-family:monospace;font-size:12px;color:#00ff9d;line-height:1.5;white-space:pre-wrap}
.bub code{font-family:monospace;background:rgba(0,0,0,.5);padding:1px 5px;border-radius:3px;color:#00ff9d;font-size:12px}
.td{display:flex;gap:4px;padding:4px}
.td span{width:6px;height:6px;border-radius:50%;background:#00d4ff;animation:bo 1s infinite}
.td span:nth-child(2){animation-delay:.2s}
.td span:nth-child(3){animation-delay:.4s}
@keyframes bo{0%,60%,100%{transform:translateY(0);opacity:.4}30%{transform:translateY(-5px);opacity:1}}
.inp{background:#0a1520;border-top:1px solid rgba(0,212,255,.2);padding:10px 12px;flex-shrink:0;padding-bottom:max(10px,env(safe-area-inset-bottom))}
.irow{display:flex;gap:8px;align-items:flex-end;background:#050a0e;border:1px solid rgba(0,212,255,.2);border-radius:24px;padding:8px 8px 8px 16px;transition:border-color .2s}
.irow:focus-within{border-color:rgba(0,212,255,.5)}
textarea{flex:1;background:transparent;border:none;outline:none;color:#c8dde8;font-size:15px;font-family:inherit;resize:none;max-height:100px;line-height:1.5}
textarea::placeholder{color:#3a5a6a}
.sbtn{width:36px;height:36px;background:linear-gradient(135deg,rgba(0,212,255,.3),rgba(0,255,157,.15));border:1px solid rgba(0,212,255,.4);border-radius:50%;color:#00d4ff;cursor:pointer;font-size:16px;display:flex;align-items:center;justify-content:center;flex-shrink:0;transition:all .2s}
.sbtn:active{transform:scale(.92)}
.sbtn:disabled{opacity:.4;cursor:not-allowed}
</style></head>
<body>
<div class="hdr">
  <div><div class="logo">⚡ NEXUS AI</div><div class="sub">NETWORKING · CYBERSEC · GED · ENGLISH · CODING</div></div>
  <div class="dot"></div>
</div>
<div class="msgs" id="msgs">
  <div class="welcome">
    <div class="wi">🤖</div>
    <div class="wt">NEXUS AI ONLINE</div>
    <div class="ws">မြန်မာ + English နှစ်ဘာသာ<br>မေးချင်တာ မေးပါ — အကုန်သိတဲ့ AI</div>
    <div class="caps">
      <div class="cap" onclick="ask('Networking ဆိုတာ ဘာလဲ?')"><div class="ci">🌐</div><div class="ct">Network</div></div>
      <div class="cap" onclick="ask('Cybersecurity basics ရှင်းပြပါ')"><div class="ci">🛡️</div><div class="ct">CyberSec</div></div>
      <div class="cap" onclick="ask('GED Math ဘယ်လို ပြင်ဆင်မလဲ?')"><div class="ci">📚</div><div class="ct">GED</div></div>
      <div class="cap" onclick="ask('English grammar tips ပေးပါ')"><div class="ci">🔤</div><div class="ct">English</div></div>
      <div class="cap" onclick="ask('Python basics သင်ပေးပါ')"><div class="ci">💻</div><div class="ct">Coding</div></div>
      <div class="cap" onclick="ask('မင်းဘာတွေ သိသလဲ?')"><div class="ci">🧠</div><div class="ct">General</div></div>
    </div>
  </div>
</div>
<div class="inp">
  <div class="irow">
    <textarea id="inp" rows="1" placeholder="မေးချင်တာ မေးပါ... / Ask anything..." onkeydown="hk(event)" oninput="rs(this)"></textarea>
    <button class="sbtn" id="sb" onclick="send()">➤</button>
  </div>
</div>
<script>
let hist=[],busy=false;
function rs(el){el.style.height="auto";el.style.height=Math.min(el.scrollHeight,100)+"px"}
function hk(e){if(e.key==="Enter"&&!e.shiftKey){e.preventDefault();send()}}
function ask(t){document.getElementById("inp").value=t;send()}
function esc(s){return s.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;")}
function fmt(t){
  t=esc(t);
  t=t.replace(/```[\w]*\n?([\s\S]*?)```/g,"<pre><code>$1</code></pre>");
  t=t.replace(/`([^`\n]+)`/g,"<code>$1</code>");
  t=t.replace(/\*\*(.*?)\*\*/g,"<strong>$1</strong>");
  t=t.replace(/\n/g,"<br>");
  return t;
}
function addMsg(role,text){
  document.querySelector(".welcome")?.remove();
  const m=document.getElementById("msgs");
  const d=document.createElement("div");
  d.className="msg "+role;
  d.innerHTML=`<div class="av">${role==="user"?"👤":"🤖"}</div><div class="bub">${fmt(text)}</div>`;
  m.appendChild(d);
  m.scrollTop=m.scrollHeight;
}
function addTyping(){
  document.querySelector(".welcome")?.remove();
  const m=document.getElementById("msgs");
  const d=document.createElement("div");
  d.id="td";d.className="msg assistant";
  d.innerHTML='<div class="av">🤖</div><div class="bub"><div class="td"><span></span><span></span><span></span></div></div>';
  m.appendChild(d);m.scrollTop=m.scrollHeight;
}
async function send(){
  if(busy)return;
  const inp=document.getElementById("inp");
  const txt=inp.value.trim();
  if(!txt)return;
  busy=true;document.getElementById("sb").disabled=true;
  inp.value="";inp.style.height="auto";
  addMsg("user",txt);
  hist.push({role:"user",content:txt});
  addTyping();
  try{
    const r=await fetch("/chat",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({history:hist})});
    const data=await r.json();
    document.getElementById("td")?.remove();
    if(data.error){hist.pop();addMsg("assistant","❌ "+data.error);}
    else{addMsg("assistant",data.reply);hist.push({role:"assistant",content:data.reply});}
  }catch(e){
    document.getElementById("td")?.remove();
    hist.pop();
    addMsg("assistant","❌ Connection error: "+e.message);
  }
  busy=false;document.getElementById("sb").disabled=false;inp.focus();
}
</script>
</body></html>'''

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        api_key = os.environ.get("GROQ_API_KEY", "")
        if not api_key:
            return jsonify({"error": "GROQ_API_KEY not set in environment"})
        
        groq_client = Groq(api_key=api_key)
        data = request.json
        history = data.get("history", [])
        
        resp = groq_client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "system", "content": SYSTEM}] + history,
            max_tokens=2048,
            temperature=0.7,
        )
        return jsonify({"reply": resp.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/manifest.json")
def manifest():
    return Response(json.dumps({"name":"NEXUS AI","short_name":"NEXUS AI","start_url":"/","display":"standalone","background_color":"#050a0e","theme_color":"#00d4ff","icons":[{"src":"/icon.png","sizes":"192x192","type":"image/png"}]}), mimetype="application/json")

@app.route("/sw.js")
def sw():
    return Response("self.addEventListener('fetch',e=>e.respondWith(fetch(e.request)));", mimetype="application/javascript")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
