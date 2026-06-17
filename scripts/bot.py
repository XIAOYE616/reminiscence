# Bot as WS SERVER - NapCat connects to us
import asyncio, json, httpx
from pathlib import Path
from datetime import datetime
import websockets
from websockets.asyncio.server import serve

ONEBOT_HTTP = "http://127.0.0.1:3001"
ONEBOT_TOKEN = "beibei-bot-token"
DEEPSEEK_KEY = ""  # Will be loaded from persona or config
TARGET_QQ = 477556020
LISTEN_HOST = "127.0.0.1"
LISTEN_PORT = 3002

# Load persona/few-shot prompt
def load_persona():
    paths = [
        Path(__file__).parent.parent / "persona" / "default" / "few_shot_prompt.txt",
        Path(__file__).parent.parent / "persona" / "default" / "SKILL.md",
    ]
    for p in paths:
        if p.exists():
            return p.read_text(encoding="utf-8")
    return "You are a helpful assistant."

PERSONA = load_persona()
SYSTEM_PROMPT = PERSONA

# Load config for deepseek key if present
cfg_file = Path(__file__).parent.parent / "config" / "config.json"
if cfg_file.exists():
    cfg = json.loads(cfg_file.read_text(encoding="utf-8-sig", errors="ignore"))
    DEEPSEEK_KEY = cfg.get("deepseek_key", DEEPSEEK_KEY)
    TARGET_QQ = int(cfg.get("target_qq", TARGET_QQ))

conversation_history = {}
MAX_HISTORY = 10

def get_history(uid):
    if uid not in conversation_history:
        conversation_history[uid] = []
    return conversation_history[uid]

async def call_deepseek(uid, user_msg):
    if not DEEPSEEK_KEY:
        return "(no API key configured)"
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
    print(f"Beibei Bot on {LISTEN_HOST}:{LISTEN_PORT}")
    print(f"Target QQ: {TARGET_QQ}")
    print(f"Persona loaded: {len(SYSTEM_PROMPT)} chars")
    while True:
        try:
            async with serve(ws_handler, LISTEN_HOST, LISTEN_PORT):
                print("Server ready!")
                await asyncio.Future()
        except Exception as e:
            print(f"Server error: {e}, retry in 5s...")
            await asyncio.sleep(5)

asyncio.run(main())
