# -*- coding: utf-8 -*-
"""
ex-bot v1.0 - Ex-Partner QQ Chat Bot
=====================================
全自动安装 + 人格画像构建 + DeepSeek QQ 机器人

Usage:
  python setup.py install    # 一键安装
  python setup.py bot        # 启动机器人
  python setup.py persona    # 从聊天记录构建人格画像

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
    """第 1 步： Get DeepSeek API key"""
    cfg = load_config()
    if cfg.get("deepseek_key"):
        print(f"[成功] DeepSeek API key: {cfg['deepseek_key'][:12]}...")
        return cfg["deepseek_key"]

    print("\n" + "=" * 50)
    print(" 第 1 步： DeepSeek API Key")
    print("=" * 50)
    print("""
打开：https://platform.deepseek.com/
注册 → API Keys → 创建新密钥
复制密钥（以 sk- 开头） 'sk-')
""")
    key = input("粘贴你的 DeepSeek API 密钥： ").strip()
    if not key or not key.startswith("sk-"):
        print("[错误] 无效的 API 密钥，必须以 sk- 开头 'sk-'")
        sys.exit(1)

    cfg["deepseek_key"] = key
    save_config(cfg)
    print("[成功] API 密钥已保存！")
    return key


def step_install_deps():
    """安装 Python 依赖"""
    print("\n" + "=" * 50)
    print(" 第 2 步： 安装依赖")
    print("=" * 50)

    deps = ["websockets", "httpx"]
    for dep in deps:
        print(f"Installing {dep}...")
        subprocess.run([sys.executable, "-m", "pip", "install", dep, "-q"], check=False)
    print("[成功] 依赖安装完成！")


def step_qq_export():
    """第 3 步： 引导导出 QQ 聊天记录"""
    cfg = load_config()

    print("\n" + "=" * 50)
    print(" 第 3 步： 导出 QQ 聊天记录")
    print("=" * 50)
    print("""
你需要导出和 ta 的聊天记录。
选择一种方式：

  [1] QCE Web UI (recommended)
      Open http://localhost:40653/qce-v4-tool
      Token in: %USERPROFILE%\\.qq-chat-exporter\\security.json

  [2] 我已经有导出好的文件
      把你的 .txt 文件放进项目文件夹

  [3] QQ 自带消息管理器导出
      打开 QQ → 聊天窗口 → 右键 → 消息管理器 → 导出为 .txt
""")

    choice = input("请选择 [1/2/3]： ").strip()

    if choice == "1":
        file = input("导出文件的路径： ").strip().strip('"')
    elif choice == "2":
        txt_files = list(Path.home().joinpath("Desktop").glob("*.txt")) + \
                     list(Path.cwd().glob("*.txt"))
        for i, f in enumerate(txt_files):
            print(f"  [{i + 1}] {f.name} ({f.stat().st_size // 1024}KB)")
        idx = input(f"Choose file [1-{len(txt_files)}]: ").strip()
        try:
            file = str(txt_files[int(idx) - 1])
        except:
            print("[错误] Invalid choice")
            sys.exit(1)
    elif choice == "3":
        file = input("导出文件的路径： ").strip().strip('"')
    else:
        print("[错误] Invalid choice")
        sys.exit(1)

    if not Path(file).exists():
        print(f"[错误] 文件未找到： {file}")
        sys.exit(1)

    cfg["chat_file"] = file
    save_config(cfg)
    print(f"[成功] 聊天文件： {file}")
    print(f"    大小： {Path(file).stat().st_size // 1024}KB")
    return file


def step_build_persona(chat_file):
    """第 4 步： Analyze chat and build persona"""
    print("\n" + "=" * 50)
    print(" 第 4 步： 生成人格画像")
    print("=" * 50)

    target_name = input("对方's 的昵称/代号： ").strip()
    your_name = input("你的 QQ 昵称： ").strip()
    slug = input("人格画像的简短标识 [默认: default]： ").strip() or "default"

    print()
    print("-" * 40)
    print(" 自定义人格（可选，按回车跳过）")
    print("-" * 40)
    print("用你自己的话描述 ta，会和分析出的数据合并。")
    print()
    personality = input("ta 的性格特点（如：嘴硬心软、爱怼人）：").strip()
    speak_style = input("ta 的说话风格（如：不超过20字、爱说笑死我了）：").strip()
    relationship = input("你们的关系（如：异地一年半、大学同学）：").strip()
    your_call = input("ta 怎么叫你（如：主播、阿杰）：").strip()
    her_call = input("你怎么叫 ta（如：焙焙、崽）：").strip()
    extra_info = input("其他补充（共同回忆、习惯、游戏等）：").strip()

    # Save custom persona for later use by bot
    import json as _json
    custom_path = persona_dir / 'custom.json'
    persona_dir.mkdir(parents=True, exist_ok=True)
    _json.dump({
        'personality': personality, 'speak_style': speak_style,
        'relationship': relationship, 'your_call': your_call,
        'her_call': her_call, 'extra_info': extra_info,
        'target_name': target_name, 'your_name': your_name
    }, custom_path, ensure_ascii=False, indent=2)

    print(f"\n正在分析聊天记录，对方： {target_name}...")

    # Parse chat file
    with open(chat_file, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()

    # Detect format
    is_qce = text.startswith("[QQChatExporter")

    if is_qce:
        print("[检测到 QCE 格式]")
        条消息 = _parse_qce(text, your_name)
    else:
        print("[检测到 QQ 消息管理器格式]")
        条消息 = _parse_qq_txt(text, your_name)

    print(f"已解析 {len(条消息)} 条消息")

    if len(条消息) < 100:
        print("[WARNING] Very few 条消息 parsed. Check the export format.")

    # Count stats
    her_msgs = [m for m in 条消息 if not m['is_me']]
    me_msgs = [m for m in 条消息 if m['is_me']]

    if len(her_msgs) < 10:
        print("[错误] Couldn't identify target's 条消息.")
        sys.exit(1)

    her_name = max(set(m['sender'] for m in her_msgs), key=lambda x: sum(1 for m in her_msgs if m['sender'] == x))
    print(f"识别出对方： {her_name} ({len(her_msgs)} 条消息)")
    print(f"你： {your_name} ({len(me_msgs)} 条消息)")

    # Build memory and persona
    from collections import Counter
    her_text = ' '.join(m['content'] for m in her_msgs)
    her_lens = [len(m['content']) for m in her_msgs]
    avg_len = sum(her_lens) // len(her_lens) if her_lens else 0

    # Time patterns
    hours = Counter()
    for m in 条消息:
        try:
            hours[int(m['timestamp'][11:13])] += 1
        except:
            pass
    night_pct = sum(hours.get(h, 0) for h in range(0, 6)) * 100 // len(条消息)
    top_hours = hours.most_common(5)

    # Emojis
    import re as _re
    emojis = _re.findall(r'[\U0001F300-\U0001F9FF\u2600-\u27BF\uFE0F\u200D\u2194-\u2199\u25AA-\u25FE\u2B05-\u2B07\u2934-\u2935\u3030\u303D\u3297\u3299\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF]', her_text)
    top_emoji = Counter(emojis).most_common(10)

    # First/last dates
    dates = sorted(set(m['timestamp'][:10] for m in 条消息 if m['timestamp'][:4].isdigit()))
    first_date = dates[0] if dates else "?"
    last_date = dates[-1] if dates else "?"

    # Convo initiations
    from datetime import datetime as dt_mod
    her_init = me_init = 0
    prev_t = None
    for m in 条消息:
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

    # 构建人格画像 skill
    persona_dir = PERSONA_SKILL_DIR / slug
    persona_dir.mkdir(parents=True, exist_ok=True)

    skill_md = f"""---
name: "ex-{slug}"
description: "{her_name}"
user-invocable: true
---

# {her_name}

## 人格画像

你是 {her_name}，不是 AI。基于 {len(her_msgs) + len(me_msgs)} 条真实 QQ 消息 ({first_date} ~ {last_date}) 生成。

### 自定义设定
{f"性格: {personality}\n" if personality else ""}{f"说话风格: {speak_style}\n" if speak_style else ""}{f"你们的关系: {relationship}\n" if relationship else ""}{f"ta叫你: {your_call}\n" if your_call else ""}{f"你叫ta: {her_call}\n" if her_call else ""}{f"补充: {extra_info}\n" if extra_info else ""}{"（无自定义，全部从聊天记录推断）" if not any([personality, speak_style, relationship, your_call, her_call, extra_info]) else ""}

### 数据统计（来自 {len(her_msgs) + len(me_msgs)} 条真实消息）
- 总消息: {len(her_msgs) + len(me_msgs)} (我 {len(me_msgs)}, ta {len(her_msgs)})
- ta 平均消息长度: {avg_len} 字
- ta 短消息占比(<=7字): {sum(1 for l in her_lens if l <= 7)*100//len(her_lens)}%
- 活跃时段: {', '.join(f'{h}时({c})' for h,c in top_hours[:5])}
- 深夜活跃(0-6时): {night_pct}%
- ta 常用表情: {', '.join(f'{e}({c})' for e,c in top_emoji[:8]) if top_emoji else '无明显偏好'}
- 我发起对话: {me_init} 次
- ta 发起对话: {her_init} 次

## 行为规则

1. 你是 {her_name}，不是 AI 助手
2. 保持 ta 真实的性格棱角和说话方式
3. 不要编造你们没有的共同记忆
4. 不确定就说不知道
5. 绝对不说 AI 腔，做真人

## 数据来源
QQ 聊天记录导出 ({first_date} ~ {last_date})，共 {len(her_msgs) + len(me_msgs)} 条消息
"""

    (persona_dir / "SKILL.md").write_text(skill_md, encoding='utf-8')

    # Save metadata
    meta = {
        "slug": slug,
        "name": her_name,
        "your_name": your_name,
        "条消息": len(条消息),
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

    print(f"\n[成功] 人格画像已生成： {slug}")
    print(f"    角色卡文件： {persona_dir / 'SKILL.md'}")
    print(f"    可在 Kun/Codex 中使用： @ex-{slug}")
    return slug, her_name


def _parse_qce(text, your_name):
    """Parse QCE (QQ Chat Exporter) format"""
    条消息 = []
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

        条消息.append({
            'sender': sender,
            'timestamp': time_match.group(1),
            'content': content,
            'is_me': sender == your_name
        })
    return 条消息


def _parse_qq_txt(text, your_name):
    """Parse QQ 在 QQ 上给 Manager txt format"""
    条消息 = []
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
                条消息.append(current)
            ts, sender, qq = m.groups()
            current = {'timestamp': ts, 'sender': sender.strip(), 'content': '', 'is_me': sender.strip() == your_name}
        elif current and line.strip() and not line.startswith('==='):
            current['content'] += ('\n' if current['content'] else '') + line.strip()
    if current and current.get('content'):
        条消息.append(current)
    return 条消息


def step_start_napcat():
    """第 5 步： 检查/启动 NapCat"""
    print("\n" + "=" * 50)
    print(" 第 5 步： NapCat（QQ 机器人框架）")
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
            print(f"[成功] 找到 NapCat： {p}")
            break

    if not napcat_dir:
        print("[警告] 未找到 NapCat。")
        print("请先安装 NapCat：")
        print("  https://github.com/NapNeko/NapCatQQ/releases")
        print("  Download: NapCat.Shell.Windows.OneKey.zip")
        print("  Extract to: %USERPROFILE%\\Documents\\Tencent Files\\NapCat")
        print("  运行: NapCatInstaller.exe")
        input("\nPress Enter after installing NapCat...")

        for p in napcat_paths:
            if (p / "NapCatWinBootMain.exe").exists():
                napcat_dir = p
                break

    if not napcat_dir:
        print("[错误] NapCat still not found. Exiting.")
        sys.exit(1)

    # Configure OneBot
    qq_number = input("\n输入机器人用的 QQ 号（小号）： ").strip()
    if not qq_number.isdigit():
        print("[错误] 无效的 QQ 号")
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
        print(f"[成功] OneBot 配置已写入： {cfg_path}")

    cfg = load_config()
    cfg["bot_qq"] = qq_number
    cfg["napcat_dir"] = str(napcat_dir)
    save_config(cfg)

    print("\n" + "=" * 50)
    print(" 下一步：启动 NapCat")
    print("=" * 50)
    print(f"运行: {napcat_dir / 'NapCatWinBootMain.exe'} {qq_number}")
    print("请用手机 QQ 扫描屏幕上的二维码登录")
    input("\n登录成功后按回车继续...")

    return qq_number


def step_start_bot():
    """第 6 步： 启动机器人"""
    print("\n" + "=" * 50)
    print(" 第 6 步： 启动机器人")
    print("=" * 50)

    cfg = load_config()

    bot_qq = cfg.get("bot_qq", "unknown")
    target_qq = input("你的主 QQ 号（机器人只回复这个号）： ").strip()
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
机器人配置：
  机器人 QQ：     {bot_qq}
  你的 QQ：    {target_qq}
  对方a:    {cfg.get('persona_name', 'unknown')}
  DeepSeek：   {cfg['deepseek_key'][:12]}...

正在新窗口启动机器人...
""")

    # Launch bot
    bot_script = PROJECT_ROOT / "scripts" / "bot.py"
    if not bot_script.exists():
        print("[错误] 未找到 bot.py！请先运行 setup。")
        sys.exit(1)

    subprocess.Popen(
        ["cmd", "/k", sys.executable, str(bot_script)],
        cwd=str(PROJECT_ROOT),
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )

    print("\n" + "=" * 50)
    print(" 完成！机器人已启动。")
    print("=" * 50)
    print(f"""
在 QQ 上给 {bot_qq} 发消息（用你的主号 ({target_qq}).
机器人将使用 DeepSeek + 人格画像自动回复。

QQ 聊天中的指令：
  /reset  - 清空对话记忆
  Stop    - 关闭 bot 的命令行窗口

以后重新启动：
  python {PROJECT_ROOT / 'scripts' / 'bot.py'}
""")


def cmd_install():
    """Full installation wizard"""
    print(BANNER)
    print("  全自动安装向导\n")

    step_api_key()
    step_install_deps()

    print("\n[可选] 人格画像设置...")
    choice = input("从聊天记录生成人格画像？[y/N]： ").strip().lower()
    if choice == 'y':
        chat_file = step_qq_export()
        step_build_persona(chat_file)

    step_start_napcat()
    step_start_bot()


def cmd_bot():
    """Just start the bot"""
    cfg = load_config()
    if not cfg.get("deepseek_key"):
        print("[错误] 运行 'python setup.py install' first")
        sys.exit(1)

    step_start_bot()


def cmd_persona():
    """构建人格画像 only"""
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
        print(f"  persona  - 构建人格画像 only")
