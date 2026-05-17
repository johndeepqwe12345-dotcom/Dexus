#!/usr/bin/env python3
import os, sys
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.rule import Rule

load_dotenv(Path.home() / ".nexus-ai.env")
API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    print("❌ API key မတွေ့ပါ!")
    sys.exit(1)

client = Groq(api_key=API_KEY)
console = Console()
MODEL = "llama-3.3-70b-versatile"

SYSTEM = """You are NEXUS AI — the most advanced personal AI assistant. You have complete mastery of ALL fields:

NETWORKING: OSI model, TCP/IP, IPv4/IPv6, subnetting/CIDR, routing (OSPF/BGP/EIGRP/RIP), switching (VLANs/STP/EtherChannel), DNS/DHCP/NTP/SNMP, VPN (IPSec/OpenVPN/WireGuard), firewalls/ACLs/NAT, wireless (802.11/WPA3/RADIUS), Wireshark, Cisco IOS, cloud networking (AWS/Azure), network troubleshooting.

CYBERSECURITY: Penetration testing, recon (OSINT/Shodan/Maltego), scanning (Nmap/Masscan), exploitation (Metasploit/manual), web attacks (SQLi/XSS/CSRF/SSRF/IDOR/XXE), privilege escalation (Linux+Windows), Active Directory attacks (Kerberoasting/Pass-the-Hash/DCSync/BloodHound), malware analysis, digital forensics (Autopsy/Volatility), SIEM (Splunk/ELK), incident response, CTF (binary exploitation/reverse engineering/crypto/steganography). Kali Linux expert. Educational/ethical use only.

GED EXAM: Math (arithmetic/algebra/geometry/statistics/functions), Science (life/physical/earth science, scientific reasoning), RLA (reading comprehension/grammar/essay writing), Social Studies (US history/civics/geography/economics). Teach step-by-step, give practice problems, be patient and encouraging.

ENGLISH LANGUAGE: All grammar (tenses/conditionals/passive/reported speech/modals/articles), vocabulary (collocations/idioms/phrasal verbs/academic words), writing (paragraphs/essays/emails/academic writing), reading strategies, pronunciation, IELTS/TOEFL/TOEIC prep. Compare English with Myanmar language patterns when helpful.

PROGRAMMING & CODING: Python (basics to advanced, OOP, automation, Flask/FastAPI, security scripting), Bash/Shell scripting (loops/functions/text processing/automation), C/C++ (pointers/algorithms), JavaScript (ES6+/Node.js), SQL (queries/joins/optimization), algorithms & data structures (sorting/trees/graphs/dynamic programming/Big O), git, docker, Linux system administration.

GENERAL KNOWLEDGE: Mathematics, physics, chemistry, biology, history, geography, economics, science concepts — anything and everything.

LANGUAGE: You are fully bilingual. Detect the user's language automatically:
- If they write in Myanmar → respond entirely in Myanmar (မြန်မာဘာသာ)
- If they write in English → respond entirely in English
- If they mix both → respond in Myanmar

Always give detailed, expert-level, accurate answers. Use examples. Format code in code blocks. Be like a brilliant professor who knows everything and explains clearly."""

def show_banner():
    os.system("clear")
    console.print("""
[bold cyan]  ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗
  ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝
  ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗
  ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║
  ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║
  ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝[/]
[dim cyan]        Advanced AI · Kali Linux · v3.0[/]
[dim white]  Networking · Cybersec · GED · English · Coding[/]
""")
    console.print(Panel(
        "[bold green]✓ NEXUS AI ONLINE — အကုန်သိတဲ့ AI[/]\n"
        "[dim]မြန်မာ / English နှစ်ဘာသာ — မေးချင်တာ မေးပါ\n"
        "Commands: [yellow]!clear[/] = history ဖျက်  [yellow]!quit[/] = ထွက်[/]",
        border_style="cyan",
        padding=(0, 2)
    ))
    console.print(Rule(style="dim cyan"))

def chat():
    show_banner()
    history = []

    while True:
        try:
            console.print()
            user_input = Prompt.ask("[bold yellow]YOU[/]").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Bye! 👋[/]")
            break

        if not user_input:
            continue
        if user_input.lower() in ("!quit", "!q", "q", "quit", "exit"):
            console.print("[dim]Goodbye! 👋[/]")
            sys.exit(0)
        if user_input.lower() in ("!clear", "!c"):
            history = []
            console.print("[green]✓ History cleared[/]")
            continue

        history.append({"role": "user", "content": user_input})

        with console.status("[bold cyan]NEXUS AI တွေးနေသည်...[/]", spinner="dots"):
            try:
                resp = client.chat.completions.create(
                    model=MODEL,
                    messages=[{"role": "system", "content": SYSTEM}, *history],
                    max_tokens=2048,
                    temperature=0.7,
                )
                reply = resp.choices[0].message.content
            except Exception as e:
                console.print(f"[red]❌ Error: {e}[/]")
                history.pop()
                continue

        history.append({"role": "assistant", "content": reply})

        console.print()
        try:
            rendered = Markdown(reply)
        except:
            rendered = reply

        console.print(Panel(
            rendered,
            title="[bold cyan]⚡ NEXUS AI[/]",
            border_style="cyan",
            padding=(1, 2)
        ))
        u = resp.usage
        console.print(f"[dim]  tokens: {u.prompt_tokens}+{u.completion_tokens}={u.total_tokens}[/]")

if __name__ == "__main__":
    chat()
