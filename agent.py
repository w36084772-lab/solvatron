#!/usr/bin/env python3
import os, time, requests, random, json, re

TELEGRAM_TOKEN = "8886129807:AAGkQ5aJs8glm42xyubOWCiwa9EbHO-izrI"
CHAT_ID = "8632875840"

def send_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg}, timeout=5)
    except Exception as e:
        print(f"[Telegram error] {e}")

def clean_text(text):
    text = re.sub(r'<!\[CDATA\[(.*?)\]\]>', r'\1', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def scrape_news():
    news_items = []
    sources = [
        {"name": "BBC", "url": "https://feeds.bbci.co.uk/news/rss.xml"},
        {"name": "Reuters", "url": "https://www.reutersagency.com/feed/?best-topics=world-news&post_type=best"},
        {"name": "Al Jazeera", "url": "https://www.aljazeera.com/xml/rss/all.xml"},
        {"name": "CNN", "url": "http://rss.cnn.com/rss/cnn_topstories.rss"}
    ]
    for s in sources:
        try:
            r = requests.get(s["url"], timeout=10)
            if r.status_code == 200:
                titles = re.findall(r"<title>(.*?)</title>", r.text)
                for t in titles[:3]:
                    if len(t) > 10 and not "BBC" in t and not "Reuters" in t and not "CNN" in t:
                        clean = clean_text(t)
                        if len(clean) > 10:
                            news_items.append({"source": s["name"], "title": clean})
                            break
        except:
            pass
    return news_items

def analyze(news):
    pos = ["growth","profit","peace","agreement","deal","success"]
    neg = ["war","sanction","crisis","attack","conflict","kill","death"]
    p = sum(1 for i in news for w in pos if w in i["title"].lower())
    n = sum(1 for i in news for w in neg if w in i["title"].lower())
    return {"positive": p, "negative": n}

print("Solvatron starting with REAL news...")
send_telegram("Solvatron is alive! Real news mode ON.")

balance = 20.0
cycle = 0

while True:
    cycle += 1
    news = scrape_news()
    analysis = analyze(news)
    
    if news:
        first = news[0]
        msg = f"CYCLE {cycle}\n{first['source']}: {first['title'][:70]}\nSentiment: {analysis['positive']}P / {analysis['negative']}N\nBalance: ${balance:.2f}"
    else:
        msg = f"Cycle {cycle} | No news. Balance: ${balance:.2f}"
    
    send_telegram(msg)
    print(msg)
    
    earned = random.choice([0,0,2,0,0,3,0,5,0])
    if earned:
        balance += earned
        send_telegram(f"+${earned}. New balance: ${balance:.2f}")
    
    if balance < 1:
        send_telegram("Balance below $1. Solvatron dies.")
        break
    
    time.sleep(30)
