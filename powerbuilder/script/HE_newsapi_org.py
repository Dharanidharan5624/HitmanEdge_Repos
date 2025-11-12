import requests
from textblob import TextBlob
from datetime import date, timedelta
import time
import sys
import os
import traceback
import mysql.connector

# === Ensure local module imports work ===
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# === Import error logger and DB connector ===
from HE_error_logs import log_error_to_db
from HE_database_connect import get_connection

# === API Key & Settings ===
API_KEY = '6a2e7b8388724ec7b7420c74d3bb2844'
SYMBOLS = ['AAPL', 'MSFT', 'SPY', 'NVDA']  # Add more symbols if needed
FETCH_DAYS = 3   # Fetch news for the past N days
INTERVAL_MINUTES = 10
INTERVAL_SECONDS = INTERVAL_MINUTES * 60



def get_sentiment(text):
    """Analyze sentiment polarity using TextBlob."""
    try:
        blob = TextBlob(text or "")
        polarity = blob.sentiment.polarity
        if polarity > 0.1:
            return "Positive"
        elif polarity < -0.1:
            return "Negative"
        else:
            return "Neutral"
    except Exception:
        error_msg = traceback.format_exc()
        error_message = traceback.format_exc()
        log_error_to_db(
            file_name=os.path.basename(__file__),
            error_description=error_message,
            created_by=None,
            env="dev"
        )
        return "Neutral"



def fetch_news(symbol):
    """Fetch recent news for a given symbol and return article list."""
    try:
        today = date.today()
        start_date = today - timedelta(days=FETCH_DAYS)
        url = (
            f"https://newsapi.org/v2/everything?"
            f"q={symbol}&from={start_date.isoformat()}&to={today.isoformat()}"
            f"&apiKey={API_KEY}&language=en&sortBy=publishedAt"
        )

        response = requests.get(url, timeout=15)
        data = response.json()

        if response.status_code != 200:
            error_detail = data.get("message", "Unknown API error")
            log_error_to_db(
                file_name=os.path.basename(__file__),
                error_description=f"NewsAPI error {response.status_code}: {error_detail}",
                created_by=None,
                env="dev"
            )
            print(f"[API ERROR] {response.status_code}: {error_detail}")
            return []

        return data.get("articles", [])

    except Exception:
        error_msg = traceback.format_exc()
        error_message = traceback.format_exc()
        log_error_to_db(
            file_name=os.path.basename(__file__),
            error_description=error_message,
            created_by=None,
            env="dev"
        )
        print(f"[ERROR] Failed to fetch news for {symbol}")
        return []


def store_in_db(symbol, title, description, published_at, url_link, sentiment):
    """Insert article sentiment record into MySQL table."""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO he_news_sentiment 
        (symbol, title, description, published_at, url, sentiment, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, NOW())
        """

        values = (symbol, title, description, published_at, url_link, sentiment)
        cursor.execute(insert_query, values)
        conn.commit()
        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        error_msg = traceback.format_exc()
        error_message = traceback.format_exc()
        log_error_to_db(
            file_name=os.path.basename(__file__),
            error_description=error_message,
            created_by=None,
            env="dev"
        )
        print(f"[DB ERROR] Could not insert record for {symbol}: {err}")


while True:
    try:
        
        print(f"[INFO] Fetching latest news at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        

        for symbol in SYMBOLS:
            print(f"\n🔍 Processing symbol: {symbol}")
            articles = fetch_news(symbol)

            if not articles:
                print(f"[WARN] No news found for {symbol}")
                continue

            for article in articles[:5]:  # Only top 5 recent articles
                title = article.get("title", "")
                description = article.get("description", "")
                published_at = article.get("publishedAt", "")
                url_link = article.get("url", "")

                combined_text = f"{title} {description}"
                sentiment = get_sentiment(combined_text)

                print(f"Title       : {title}")
                print(f"Published At: {published_at}")
                print(f"Sentiment   : {sentiment}")
                print(f"URL         : {url_link}")
                print("-" * 100)

                store_in_db(symbol, title, description, published_at, url_link, sentiment)

        print(f"\n✅ Completed news cycle. Waiting {INTERVAL_MINUTES} minutes...\n")

    except Exception:
        error_msg = traceback.format_exc()
        print("[FATAL ERROR] Script encountered an error.")
        error_message = traceback.format_exc()
        log_error_to_db(
            file_name=os.path.basename(__file__),
            error_description=error_message,
            created_by=None,
            env="dev"
        )

    time.sleep(INTERVAL_SECONDS)
