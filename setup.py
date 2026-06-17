# -*- coding: utf-8 -*-
"""
ex-bot v1.0 - Ex-Partner QQ Chat Bot
=====================================
Full-auto installer + persona builder + DeepSeek-powered QQ bot.

Usage:
  python setup.py install    # One-click setup
  python setup.py bot        # Start the bot
  python setup.py persona    # Build persona from chat export

Steps:
  1. Enter your DeepSeek API key
  2. Export QQ chat history (guided)
  3. Auto-download NapCat
  4. Scan QR to login QQ alt account
  5. Bot goes live!
"""

import os, sys, json, re, shutil, subprocess, time
from pathlib import Path
from datetime import datetime

# ===== Config =====
PROJECT_ROOT = Path(__file__).parent.resolve()
CONFIG_FILE = PROJECT_ROOT / "config" / "config.json"
PERSONA_SKILL_DIR = PROJECT_ROOT / "persona"

BANNER = r"""
  _____      ____        _   
 | ____|     |  _ \      | |  
 |  _| _____ | |_) | ___ | |_ 
 | |__|_____||  _ < / _ \| __|
 |_____|     | |_) | (_) | |_ 
             |____/ \___/ \__|
   Ex-Partner QQ Chat Bot v1.0
"""


def load_config():
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text())
    return {}


def save_config(cfg):
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2, ensure_ascii=False))


def step_api_key():
    """Step 1: Get DeepSeek API key"""
    cfg = load_config()
    if cfg.get("deepseek_key"):
        print(f"[OK] DeepSeek API key: {cfg['deepseek_key'][:12]}...")
        return cfg["deepseek_key"]

    print("\n" + "=" * 50)
    print(" Step 1: DeepSeek API Key")
    print("=" * 50)
    print("""
Go to: https://platform.deepseek.com/
Register -> API Keys -> Create new key
Copy the key (starts with 'sk-')
""")
    key = input("Paste your DeepSeek API key: ").strip()
    if not key or not key.startswith("sk-"):
        print("[ERROR] Invalid API key. Must start with 'sk-'")
        sys.exit(1)

    cfg["deepseek_key"] = key
    save_config(cfg)
    print("[OK] API key saved!")
    return key


def step_install_deps():
    """Install Python dependencies"""
    print("\n" + "=" * 50)
    print(" Step 2: Installing Dependencies")
    print("=" * 50)

    deps = ["websockets", "httpx"]
    for dep in deps:
        print(f"Installing {dep}...")
        subprocess.run([sys.executable, "-m", "pip", "install", dep, "-q"], check=False)
    print("[OK] Dependencies installed!")


def step_qq_export():
    """Step 3: Guide QQ chat export"""
    cfg = load_config()

    print("\n" + "=" * 50)
    print(" Step 3: Export QQ Chat History")
    print("=" * 50)
    print("""
You need to export your chat history with the person.
Choose one method:

  [1] QCE Web UI (recommended)
      Open http://localhost:40653/qce-v4-tool
      Token in: %USERPROFILE%\\.qq-chat-exporter\\security.json

  [2] I already have the export file
      Put your .txt file in the project folder

  [3] QQ built-in Message Manager
      Open QQ -> chat window -> ... -> Message Manager -> Export as .txt
""")

    choice = input("Choose [1/2/3]: ").strip()

    if choice == "1":
        file = input("Path to exported .txt file: ").strip().strip('"')
    elif choice == "2":
        txt_files = list(Path.home().joinpath("Desktop").glob("*.txt")) + \
                     list(Path.cwd().glob("*.txt"))
        for i, f in enumerate(txt_files):
            print(f"  [{i + 1}] {f.name} ({f.stat().st_size // 1024}KB)")
        idx = input(f"Choose file [1-{len(txt_files)}]: ").strip()
        try:
            file = str(txt_files[int(idx) - 1])
        except:
            print("[ERROR] Invalid choice")
            sys.exit(1)
    elif choice == "3":
        file = input("Path to exported .txt file: ").strip().strip('"')
    else:
        print("[ERROR] Invalid choice")
        sys.exit(1)

    if not Path(file).exists():
        print(f"[ERROR] File not found: {file}")
        sys.exit(1)

    cfg["chat_file"] = file
    save_config(cfg)
    print(f"[OK] Chat file: {file}")
    print(f"    Size: {Path(file).stat().st_size // 1024}KB")
    return file


def step_build_persona(chat_file):
    """Step 4: Analyze chat and build persona"""
    print("\n" + "=" * 50)
    print(" Step 4: Building Persona")
    print("=" * 50)

    target_name = input("Person's nickname/codename: ").strip()
    your_name = input("Your QQ nickname: ").strip()
    slug = input("Short slug for this persona [default: default]: ").strip() or "default"

    print(f"\nAnalyzing chat with {target_name}...")

    # Parse chat file
    with open(chat_file, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()

    # Detect format
    is_qce = text.startswith("[QQChatExporter")

    if is_qce:
        print("[QCE format detected]")
        messages = _parse_qce(text, your_name)
    else:
        print("[QQ Message Manager format detected]")
        messages = _parse_qq_txt(text, your_name)

    print(f"Parsed {len(messages)} messages")

    if len(messages) < 100:
        print("[WARNING] Very few messages parsed. Check the export format.")

    # Count stats
    her_msgs = [m for m in messages if not m['is_me']]
    me_msgs = [m for m in messages if m['is_me']]

    if len(her_msgs) < 10:
        print("[ERROR] Couldn't identify target's messages.")
        sys.exit(1)

    her_name = max(set(m['sender'] for m in her_msgs), key=lambda x: sum(1 for m in her_msgs if m['sender'] == x))
    print(f"Target identified: {her_name} ({len(her_msgs)} messages)")
    print(f"You: {your_name} ({len(me_msgs)} messages)")

    # Build memory and persona
    from collections import Counter
    her_text = ' '.join(m['content'] for m in her_msgs)
    her_lens = [len(m['content']) for m in her_msgs]
    avg_len = sum(her_lens) // len(her_lens) if her_lens else 0

    # Time patterns
    hours = Counter()
    for m in messages:
        try:
            hours[int(m['timestamp'][11:13])] += 1
        except:
            pass
    night_pct = sum(hours.get(h, 0) for h in range(0, 6)) * 100 // len(messages)
    top_hours = hours.most_common(5)

    # Emojis
    import re as _re
    emojis = _re.findall(r'[\U0001F300-\U0001F9FF\u2600-\u27BF\uFE0F\u200D\u2194-\u2199\u25AA-\u25FE\u2B05-\u2B07\u2934-\u2935\u3030\u303D\u3297\u3299\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF]', her_text)
    top_emoji = Counter(emojis).most_common(10)

    # First/last dates
    dates = sorted(set(m['timestamp'][:10] for m in messages if m['timestamp'][:4].isdigit()))
    first_date = dates[0] if dates else "?"
    last_date = dates[-1] if dates else "?"

    # Convo initiations
    from datetime import datetime as dt_mod
    her_init = me_init = 0
    prev_t = None
    for m in messages:
        try:
            t = dt_mod.strptime(m['timestamp'], '%Y-%m-%d %H:%M:%S')
            if prev_t is None or (t - prev_t).total_seconds() > 3600:
                if m['is_me']:
                    me_init += 1
                else:
                    her_init += 1
            prev_t = t
        except:
            pass

    # Build persona skill
    persona_dir = PERSONA_SKILL_DIR / slug
    persona_dir.mkdir(parents=True, exist_ok=True)

    skill_md = f"""---
name: "ex-{slug}"
description: "{her_name} - AI persona based on {len(messages)} real QQ messages"
user-invocable: true
---

# {her_name}

## Persona

You are {her_name}, a real person modeled from {len(messages)} QQ messages ({first_date} to {last_date}).
Call me "{your_name}".

Speaking style:
- Average message length: {avg_len} chars
- Short messages (under 7 chars): {sum(1 for l in her_lens if l <= 7)*100//len(her_lens)}%
- Active hours: {', '.join(f'{h}h({c})' for h,c in top_hours[:5])}
- Night owl: {night_pct}% messages at 0-6am
- Emoji style: {', '.join(f'{e}({c})' for e,c in top_emoji[:8]) if top_emoji else 'minimal'}

Conversation patterns:
- Convo initiations: me {me_init}, her {her_init}
- Total messages: {len(messages)} (me {len(me_msgs)}, her {len(her_msgs)})

Rules:
1. You are {her_name}, NOT an AI assistant
2. Keep the person's real edges, limits, and inconsistencies
3. Do not invent shared memories
4. Use the speaking style from the data: {avg_len} avg chars, short messages preferred
5. If unsure, say so
6. Never use AI-speak. Be human. 

## Memory

- Knows {your_name} since {first_date}
- {len(messages)} messages exchanged
- Her nickname: {her_name}
- Your nickname to her: {your_name}

## Source
Built from QQ chat export, {len(messages)} messages
"""

    (persona_dir / "SKILL.md").write_text(skill_md, encoding='utf-8')

    # Save metadata
    meta = {
        "slug": slug,
        "name": her_name,
        "your_name": your_name,
        "messages": len(messages),
        "first_date": first_date,
        "last_date": last_date,
        "created": dt_mod.now().isoformat()
    }
    (persona_dir / "meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False))

    # Save persona to config
    cfg = load_config()
    cfg["persona_slug"] = slug
    cfg["persona_name"] = her_name
    cfg["your_name"] = your_name
    save_config(cfg)

    print(f"\n[OK] Persona built: {slug}")
    print(f"    Skill file: {persona_dir / 'SKILL.md'}")
    print(f"    Can be used with Kun/Codex: @ex-{slug}")
    return slug, her_name


def _parse_qce(text, your_name):
    """Parse QCE (QQ Chat Exporter) format"""
    messages = []
    blocks = text.split('\n\n')
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        lines = block.split('\n')
        if len(lines) < 3:
            continue

        sender = lines[0].rstrip(':').strip()
        if sender in ('导出时间', '时间范围', '聊天名称', '聊天类型', '消息总数'):
            continue

        time_match = re.search(r'时间:\s*(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})', block)
        if not time_match:
            continue

        content_start = block.find('内容: ')
        if content_start == -1:
            continue
        content = block[content_start + 4:].strip()

        messages.append({
            'sender': sender,
            'timestamp': time_match.group(1),
            'content': content,
            'is_me': sender == your_name
        })
    return messages


def _parse_qq_txt(text, your_name):
    """Parse QQ Message Manager txt format"""
    messages = []
    pattern = re.compile(
        r'^(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+(.+?)(?:\((\d+)\))?\s*$',
        re.MULTILINE
    )
    # Simplified parser
    lines = text.split('\n')
    current = None
    for line in lines:
        m = pattern.match(line.strip())
        if m:
            if current:
                messages.append(current)
            ts, sender, qq = m.groups()
            current = {'timestamp': ts, 'sender': sender.strip(), 'content': '', 'is_me': sender.strip() == your_name}
        elif current and line.strip() and not line.startswith('==='):
            current['content'] += ('\n' if current['content'] else '') + line.strip()
    if current and current.get('content'):
        messages.append(current)
    return messages


def step_start_napcat():
    """Step 5: Check/start NapCat"""
    print("\n" + "=" * 50)
    print(" Step 5: NapCat (QQ Bot Framework)")
    print("=" * 50)

    # Check if NapCat is already installed
    napcat_paths = [
        Path(os.environ.get("USERPROFILE", "")) / "Documents/Tencent Files/NapCat/NapCat.44498.Shell",
        Path(os.environ.get("USERPROFILE", "")) / "Documents/Tencent Files/NapCat",
    ]

    napcat_dir = None
    for p in napcat_paths:
        if (p / "NapCatWinBootMain.exe").exists():
            napcat_dir = p
            print(f"[OK] NapCat found: {p}")
            break

    if not napcat_dir:
        print("[WARN] NapCat not found.")
        print("Please install NapCat first:")
        print("  https://github.com/NapNeko/NapCatQQ/releases")
        print("  Download: NapCat.Shell.Windows.OneKey.zip")
        print("  Extract to: %USERPROFILE%\\Documents\\Tencent Files\\NapCat")
        print("  Run: NapCatInstaller.exe")
        input("\nPress Enter after installing NapCat...")

        for p in napcat_paths:
            if (p / "NapCatWinBootMain.exe").exists():
                napcat_dir = p
                break

    if not napcat_dir:
        print("[ERROR] NapCat still not found. Exiting.")
        sys.exit(1)

    # Configure OneBot
    qq_number = input("\nEnter the QQ number for the bot account (small/alt account): ").strip()
    if not qq_number.isdigit():
        print("[ERROR] Invalid QQ number")
        sys.exit(1)

    # Write OneBot config
    config_dir = napcat_dir / "versions"
    try:
        version_dir = next(config_dir.glob("*/resources/app/napcat/config"))
    except StopIteration:
        # Fallback: find napcat config dir
        version_dir = None
        for d in config_dir.glob("**/napcat/config"):
            if d.is_dir():
                version_dir = d
                break

    if version_dir:
        ob_config = {
            "network": {
                "httpServers": [{
                    "name": "http", "enable": True, "host": "127.0.0.1",
                    "port": 3001, "enableCors": True, "enableHeartbeat": True,
                    "token": "beibei-bot-token"
                }],
                "websocketClients": [{
                    "name": "ws-bot", "enable": True,
                    "url": "ws://127.0.0.1:3002",
                    "reconnectInterval": 5000,
                    "token": "beibei-bot-token"
                }],
                "websocketServers": [],
                "httpSseServers": [], "httpClients": [], "plugins": []
            },
            "musicSignUrl": "", "enableLocalFile2Url": False,
            "parseMultMsg": False, "imageDownloadProxy": "",
            "timeout": {"baseTimeout": 10000, "uploadSpeedKBps": 256, "downloadSpeedKBps": 256, "maxTimeout": 1800000}
        }
        cfg_path = version_dir / f"onebot11_{qq_number}.json"
        cfg_path.write_text(json.dumps(ob_config, indent=2, ensure_ascii=False))
        print(f"[OK] OneBot config written: {cfg_path}")

    cfg = load_config()
    cfg["bot_qq"] = qq_number
    cfg["napcat_dir"] = str(napcat_dir)
    save_config(cfg)

    print("\n" + "=" * 50)
    print(" Next: Start NapCat")
    print("=" * 50)
    print(f"Run: {napcat_dir / 'NapCatWinBootMain.exe'} {qq_number}")
    print("Scan QR code to login the bot QQ account")
    input("\nPress Enter after QQ login is complete...")

    return qq_number


def step_start_bot():
    """Step 6: Launch the bot"""
    print("\n" + "=" * 50)
    print(" Step 6: Starting Bot")
    print("=" * 50)

    cfg = load_config()

    bot_qq = cfg.get("bot_qq", "unknown")
    target_qq = input("Your main QQ number (bot will only reply to you): ").strip()
    cfg["target_qq"] = target_qq
    save_config(cfg)

    # Write bot config
    bot_cfg = {
        "deepseek_key": cfg["deepseek_key"],
        "bot_qq": bot_qq,
        "target_qq": int(target_qq),
        "onebot_http": "http://127.0.0.1:3001",
        "onebot_ws_port": 3002,
        "onebot_token": "beibei-bot-token",
        "persona_slug": cfg.get("persona_slug", "default")
    }
    (PROJECT_ROOT / "config" / "bot_config.json").write_text(json.dumps(bot_cfg, indent=2))

    print(f"""
Bot config:
  Bot QQ:     {bot_qq}
  Your QQ:    {target_qq}
  Persona:    {cfg.get('persona_name', 'unknown')}
  DeepSeek:   {cfg['deepseek_key'][:12]}...

Starting bot in new window...
""")

    # Launch bot
    bot_script = PROJECT_ROOT / "scripts" / "bot.py"
    if not bot_script.exists():
        print("[ERROR] bot.py not found! Run setup first.")
        sys.exit(1)

    subprocess.Popen(
        ["cmd", "/k", sys.executable, str(bot_script)],
        cwd=str(PROJECT_ROOT),
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )

    print("\n" + "=" * 50)
    print(" DONE! Bot is running.")
    print("=" * 50)
    print(f"""
Message {bot_qq} on QQ with your main account ({target_qq}).
The bot will auto-reply using DeepSeek + persona.

Commands in QQ chat:
  /reset  - Clear conversation memory
  Stop    - Close the bot cmd window

To restart later:
  python {PROJECT_ROOT / 'scripts' / 'bot.py'}
""")


def cmd_install():
    """Full installation wizard"""
    print(BANNER)
    print("  Full Installation Wizard\n")

    step_api_key()
    step_install_deps()

    print("\n[OPTIONAL] Persona setup...")
    choice = input("Build persona from chat export? [y/N]: ").strip().lower()
    if choice == 'y':
        chat_file = step_qq_export()
        step_build_persona(chat_file)

    step_start_napcat()
    step_start_bot()


def cmd_bot():
    """Just start the bot"""
    cfg = load_config()
    if not cfg.get("deepseek_key"):
        print("[ERROR] Run 'python setup.py install' first")
        sys.exit(1)

    step_start_bot()


def cmd_persona():
    """Build persona only"""
    chat_file = step_qq_export()
    step_build_persona(chat_file)


if __name__ == "__main__":
    commands = {
        "install": cmd_install,
        "bot": cmd_bot,
        "persona": cmd_persona,
    }

    cmd = sys.argv[1] if len(sys.argv) > 1 else "install"
    if cmd in commands:
        commands[cmd]()
    else:
        print(f"Usage: python setup.py [{'|'.join(commands)}]")
        print(f"  install  - Full setup wizard")
        print(f"  bot      - Start bot only")
        print(f"  persona  - Build persona only")
