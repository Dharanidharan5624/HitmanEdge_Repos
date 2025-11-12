import sys
import os
import time
import json
import requests
import traceback
import nltk
from datetime import datetime, timezone

# Ensure imports work from the same directory
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from HE_database_connect import get_connection
from HE_error_logs import log_error_to_db

#  Initialize Sentiment Analyzer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon', quiet=True)
sid = SentimentIntensityAnalyzer()


# Convert API datetime → MySQL compatible format
def clean_datetime(pub_time_str):
    """
    Convert ISO 8601 (e.g., 2025-10-30T08:21:00-04:00) → MySQL DATETIME (2025-10-30 12:21:00)
    Automatically converts to UTC.
    """
    try:
        # Handle timezone and convert to UTC
        dt = datetime.fromisoformat(pub_time_str.replace("Z", "+00:00"))
        dt_utc = dt.astimezone(timezone.utc)
        return dt_utc.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        # Fallback: remove timezone manually if malformed
        try:
            parts = pub_time_str.split("T")
            date_part = parts[0]
            time_part = parts[1].split("+")[0].split("-")[0]
            return f"{date_part} {time_part}"
        except Exception:
            return None


#Sentiment Analysis
def analyze_sentiment(text):
    try:
        scores = sid.polarity_scores(text)
        return scores
    except Exception:
        error_message = traceback.format_exc()
        log_error_to_db(
            file_name=os.path.basename(__file__),
            error_description=error_message,
            created_by=None,
            env="dev"
        )
        print("[ERROR] Sentiment analysis failed.")
        return {}


# Store article in MySQL
def store_article(symbols, title, summary, pub_time, link, sentiment_dict):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM he_news_articles WHERE link = %s", (link,))
        article_count = cursor.fetchone()[0]

        if article_count == 0:
            sentiment_json = json.dumps(sentiment_dict)
            insert_query = """
                INSERT INTO he_news_articles 
                (stock_symbol, title, summary, pub_time, link, sentiment)
                VALUES (%s, %s, %s, %s, %s, %s)
            """

            pub_time_clean = clean_datetime(pub_time)
            symbols_str = ','.join(symbols)

            try:
                cursor.execute(insert_query, (symbols_str, title, summary, pub_time_clean, link, sentiment_json))
                conn.commit()
                print(f"✅ Stored: {title[:60]}")
            except Exception as db_err:
                print(f"[DB ERROR DETAIL] {db_err}")   # 👈 See actual MySQL error
                raise

        else:
            print(f"⚠️ Skipped (duplicate): {title[:60]}")

        cursor.close()
        conn.close()

    except Exception:
        error_message = traceback.format_exc()
        log_error_to_db(
            file_name=os.path.basename(__file__),
            error_description=error_message,
            created_by=None,
            env="dev"
        )
        print("[ERROR] Database insert failed.")



# Fetch article details (full info)
def fetch_article_details(article_id):
    try:
        url = f"https://seekingalpha.com/api/v3/news/{article_id}"
        headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}

        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            data = res.json()
            attributes = data.get("data", {}).get("attributes", {})
            page = data.get("meta", {}).get("page", {})
            title = attributes.get("title", "No title")
            summary = page.get("description", "No summary")
            pub_time = attributes.get("publishOn", "Unknown")
            link = f"https://seekingalpha.com/news/{article_id}"

            relationships = data.get("data", {}).get("relationships", {})
            symbols_data = relationships.get("primaryTickers", {}).get("data", [])
            symbols = [s.get("id", "UNKNOWN") for s in symbols_data]

            sentiment = analyze_sentiment(summary)

            print(f"\nSymbols      : {symbols}")
            print(f"Title        : {title}")
            print(f"Summary      : {summary}")
            print(f"Published At : {pub_time}")
            print(f"Link         : {link}")
            print(f"Sentiment    : {sentiment}")
            print("-" * 80)

            store_article(symbols, title, summary, pub_time, link, sentiment)

        else:
            msg = f"Failed to fetch article {article_id}. Status code: {res.status_code}"
            print(f"[WARNING] {msg}")
            log_error_to_db(
                file_name=os.path.basename(__file__),
                error_description=msg,
                created_by=None,
                env="dev"
            )

    except Exception:
        error_message = traceback.format_exc()
        log_error_to_db(
            file_name=os.path.basename(__file__),
            error_description=error_message,
            created_by=None,
            env="dev"
        )
        print("[ERROR] fetch_article_details failed.")


# Fetch latest news list
def fetch_latest_news(limit=5):
    try:
        url = "https://seekingalpha.com/api/v3/news?filter[category]=market-news&page[size]=5&page[number]=1"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.9"
        }

        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            try:
                articles = res.json().get("data", [])[:limit]
                if not articles:
                    print("⚠️ No articles found.")
                    return

                for article in articles:
                    article_id = article.get("id")
                    if article_id:
                        fetch_article_details(article_id)

            except ValueError:
                error_message = traceback.format_exc()
                log_error_to_db(
                    file_name=os.path.basename(__file__),
                    error_description=error_message,
                    created_by=None,
                    env="dev"
                )
                print("[ERROR] JSON parsing error.")
        else:
            msg = f"Failed to fetch article list. Status code: {res.status_code}"
            print(f"[WARNING] {msg}")
            log_error_to_db(
                file_name=os.path.basename(__file__),
                error_description=msg,
                created_by=None,
                env="dev"
            )

    except Exception:
        error_message = traceback.format_exc()
        log_error_to_db(
            file_name=os.path.basename(__file__),
            error_description=error_message,
            created_by=None,
            env="dev"
        )
        print("[ERROR] fetch_latest_news failed.")


# Main Loop
if __name__ == "__main__":
    while True:
        try:
            print("\n📰 Fetching latest news...\n")
            fetch_latest_news(limit=5)
            print("Sleeping for 10 minutes...\n")
            time.sleep(600)

        except Exception:
            error_message = traceback.format_exc()
            log_error_to_db(
                file_name=os.path.basename(__file__),
                error_description=error_message,
                created_by=None,
                env="dev"
            )
            print("[ERROR] Unexpected runtime error.")
            time.sleep(600)
