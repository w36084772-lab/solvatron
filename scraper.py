#!/usr/bin/env python3
import requests
import json
import time
import random

# ===== SCRAPE NEWS FROM RSS FEEDS =====
def scrape_news():
    """Scrape news from free RSS feeds and news APIs"""
    news_items = []
    
    # Free news sources (no API key required)
    sources = [
        {
            "name": "BBC News",
            "url": "https://feeds.bbci.co.uk/news/rss.xml"
        },
        {
            "name": "Reuters",
            "url": "https://www.reutersagency.com/feed/?best-topics=world-news&post_type=best"
        },
        {
            "name": "Al Jazeera",
            "url": "https://www.aljazeera.com/xml/rss/all.xml"
        },
        {
            "name": "CNN",
            "url": "http://rss.cnn.com/rss/cnn_topstories.rss"
        }
    ]
    
    # Try to fetch news from each source
    for source in sources:
        try:
            print(f"Fetching: {source['name']}")
            response = requests.get(source['url'], timeout=10)
            
            if response.status_code == 200:
                # Parse RSS (simple approach - just find titles)
                content = response.text
                titles = []
                # Look for <title> tags
                import re
                title_matches = re.findall(r'<title>(.*?)</title>', content)
                
                for title in title_matches[:5]:  # Top 5 titles
                    if "BBC" not in title and "Reuters" not in title and "Al Jazeera" not in title:
                        news_items.append({
                            "source": source['name'],
                            "title": title.strip(),
                            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                        })
        except Exception as e:
            print(f"Error fetching {source['name']}: {e}")
    
    return news_items

# ===== SIMPLE NEWS ANALYSIS (WITHOUT GROQ) =====
def analyze_news(news_items):
    """Basic analysis - can be replaced with Groq later"""
    if not news_items:
        return {"status": "no_news", "message": "No news found"}
    
    # Keywords for sentiment
    positive_keywords = ["growth", "profit", "success", "peace", "agreement", "deal"]
    negative_keywords = ["war", "sanction", "crisis", "attack", "conflict", "kill", "death"]
    
    positive_count = 0
    negative_count = 0
    
    for item in news_items:
        title = item['title'].lower()
        for word in positive_keywords:
            if word in title:
                positive_count += 1
        for word in negative_keywords:
            if word in title:
                negative_count += 1
    
    return {
        "status": "analyzed",
        "total_news": len(news_items),
        "positive": positive_count,
        "negative": negative_count,
        "ratio": f"{positive_count}/{negative_count}",
        "news_items": news_items
    }

# ===== MAIN =====
if __name__ == "__main__":
    print("🧠 Scraping news...")
    news = scrape_news()
    print(f"Found {len(news)} news items")
    
    analysis = analyze_news(news)
    print(json.dumps(analysis, indent=2))
