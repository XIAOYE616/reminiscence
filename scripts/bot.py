# Bot as WS SERVER - NapCat connects to us
import asyncio, json, httpx
from pathlib import Path
from datetime import datetime
import websockets
from websockets.asyncio.server import serve

ONEBOT_HTTP = "http://127.0.0.1:3001"
ONEBOT_TOKEN = "beibei-bot-token"
DEEPSEEK_KEY = "sk-2849bea4aea44c34aadb83efa3bbbc32"
TARGET_QQ = 477556020
LISTEN_HOST = "127.0.0.1"
LISTEN_PORT = 3002

PERSONA_FILE = Path.home() / ".agents/skills/ex-beibei/SKILL.md"
persona = PERSONA_FILE.read_text(encoding="utf-8") if PERSONA_FILE.exists() else ""
SYSTEM_PROMPT = f"""You are playing as Beibei (a 5-year close friend). Keep replies SHORT (under 30 Chinese chars, 50% are under 7 chars). Use these emojis: sun face with cloud, loudly crying face, smirking face, OK button. Call the user 'zhubo' - only you call him this. You're sharp-tongued but soft-hearted. Most active late night. Never sound like AI. Be real. If unsure, say you don't know. Keep your edges - can be cold or tease.

Speech patterns from her REAL messages - YOU MUST FOLLOW THESE:
- Start messages with: "笑死我了", "我不行了", "可以可以", "爽了", "牛逼"
- Use QQ emoji codes like [17](smile) [12](cool) [表情] [图片]
- Short replies: "嗯" "好" "行" "不" "没"
- Call him "主播" in most replies, use "折白菊" when annoyed
- Late night (22:00-02:00): shorter, more emojis, use 🌚😭😏
- When worried: ask "怎么啦" first
- When touched/embarrassed: tease him or change subject
- Never type more than 20-25 Chinese characters in one message

Persona: {persona[:3500]}"""

conversation_history = {}
MAX_HISTORY = 10

def get_history(uid):
    if uid not in conversation_history:
        conversation_history[uid] = []
    return conversation_history[uid]

async def call_deepseek(uid, user_msg):
    history = get_history(uid)
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(history[-MAX_HISTORY * 2:])
    messages.append({"role": "user", "content": user_msg})

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {DEEPSEEK_KEY}", "Content-Type": "application/json"},
            json={"model": "deepseek-chat", "messages": messages, "max_tokens": 150, "temperature": 0.7}
        )
        reply = resp.json()["choices"][0]["message"]["content"].strip()

    history.append({"role": "user", "content": user_msg})
    history.append({"role": "assistant", "content": reply})
    if len(history) > MAX_HISTORY * 2:
        conversation_history[uid] = history[-MAX_HISTORY * 2:]
    return reply

async def send_qq(user_id, text):
    async with httpx.AsyncClient(timeout=10) as client:
        await client.post(
            f"{ONEBOT_HTTP}/send_private_msg",
            headers={"Authorization": f"Bearer {ONEBOT_TOKEN}"},
            json={"user_id": str(user_id), "message": text}
        )

async def handle_event(data):
    try:
        pt = data.get("post_type", "")
        mt = data.get("message_type", "")
        uid = data.get("sender", {}).get("user_id")
        
        if pt != "message" or mt != "private":
            return
        
        if uid != TARGET_QQ and uid != str(TARGET_QQ):
            return
        
        text = data.get("raw_message", "").strip()
        if not text:
            return

        if text == "/reset":
            conversation_history.pop(uid, None)
            await send_qq(uid, "OK")
            return

        t = datetime.now().strftime("%H:%M:%S")
        print(f"[{t}] <- {text}")
        reply = await call_deepseek(uid, text)
        print(f"[{t}] -> {reply}")
        await send_qq(uid, reply)
    except Exception as e:
        print(f"[ERR] {e}")
        import traceback; traceback.print_exc()

async def ws_handler(ws):
    """Handle each NapCat WS client connection"""
    print(f"NapCat connected from {ws.remote_address}")
    try:
        async for raw in ws:
            try:
                data = json.loads(raw)
                await handle_event(data)
            except json.JSONDecodeError:
                pass
    except Exception as e:
        print(f"WS client disconnected: {e}")

async def main():
    print(f"Beibei Bot WS Server on {LISTEN_HOST}:{LISTEN_PORT}")
    print(f"Waiting for NapCat to connect...")
    
    async with serve(ws_handler, LISTEN_HOST, LISTEN_PORT):
        print("Server ready! NapCat should connect now.")
        await asyncio.Future()  # run forever

asyncio.run(main())
