import requests
import time

TELEGRAM_TOKEN = "8886129807:AAGkQ5aJs8glm42xyubOWCiwa9EbHO-izrI"
GROQ_API_KEY = "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"
CHAT_ID = "8632875840"
WALLET_ADDRESS = "2xbwAdX7cHR3a5ohfTW6HUZieeJzmuJ8Ykex6yWV3q6n"

def send(msg):
    try:
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                     data={"chat_id": CHAT_ID, "text": msg}, timeout=5)
    except Exception as e:
        print(f"Send error: {e}")

def ask_groq(q):
    try:
        r = requests.post("https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
            json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": q}]},
            timeout=10)
        return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {e}"

def get_updates(offset=None):
    try:
        r = requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates",
                        params={"timeout": 30, "offset": offset}, timeout=35)
        return r.json().get("result", [])
    except Exception as e:
        print(f"Get updates error: {e}")
        return []

send("Solvatron is ALIVE")
last_id = 0

while True:
    try:
        updates = get_updates(last_id + 1)
        for u in updates:
            if "message" in u and "text" in u["message"]:
                t = u["message"]["text"]
                print(f"Received: {t}")
                if t == "/ping":
                    reply = "Pong"
                elif t == "/balance":
                    reply = f"Wallet: {WALLET_ADDRESS}"
                elif t == "/start" or t == "/status":
                    reply = "Solvatron is alive"
                else:
                    send("Thinking...")
                    reply = ask_groq(t)
                send(reply)
                last_id = u["update_id"]
        time.sleep(1)
    except Exception as e:
        send(f"ERROR: {e}")
        time.sleep(10)
