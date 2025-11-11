import requests
import os
import traceback
from datetime import datetime
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from HE_error_logs import log_error_to_db

try:
    nltk.download('vader_lexicon', quiet=True)
    sid = SentimentIntensityAnalyzer()
except Exception:
    error_message = traceback.format_exc()
    log_error_to_db(
        file_name=os.path.basename(__file__),
        error_description=error_message,
        created_by=None,
        env="dev"
    )
    exit("NLTK setup failed.")

def analyze_sentiment(text):
    try:
        return sid.polarity_scores(text)
    except Exception:
        error_message = traceback.format_exc()
        log_error_to_db(
            file_name=os.path.basename(__file__),
            error_description=error_message,
            created_by=None,
            env="dev"
        )
        return {}

url = (
    "https://www.alphavantage.co/query?function=NEWS_SENTIMENT&"
    "apikey=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"
)

try:
    response = requests.get(url, timeout=10)
    data = response.json()
except Exception:
    error_message = traceback.format_exc()
    log_error_to_db(
        file_name=os.path.basename(__file__),
        error_description=error_message,
        created_by=None,
        env="dev"
    )
    exit("API request failed.")

if "feed" not in data:
    error_message = "Invalid API response structure: 'feed' missing."
    log_error_to_db(
        file_name=os.path.basename(__file__),
        error_description=error_message,
        created_by=None,
        env="dev"
    )
    print("No news feed found. API response:", data)
    exit()

for article in data.get("feed", [])[:6]:
    try:
        raw_time = article.get("time_published", "")
        try:
            dt = datetime.strptime(raw_time, "%Y%m%dT%H%M%S")
            formatted_date = dt.strftime("%Y/%m/%d")
        except Exception:
            formatted_date = "Invalid Date"
            error_message = traceback.format_exc()
            log_error_to_db(
                file_name=os.path.basename(__file__),
                error_description=error_message,
                created_by=None,
                env="dev"
            )

        summary = article.get("summary", "")
        ticker_data = article.get("ticker_sentiment", [])
        if not ticker_data:
            continue

        for item in ticker_data:
            try:
                ticker = item.get('ticker', 'N/A')
                relevance_score = item.get('relevance_score', 'N/A')
                ticker_sentiment_score_str = item.get('ticker_sentiment_score', '0')
                score = float(ticker_sentiment_score_str)
                sentiment_label = "Positive" if score > 0 else "Negative" if score < 0 else "Neutral"
            except Exception:
                sentiment_label = "Unknown"

            sentiment = analyze_sentiment(summary)

            print(f"Ticker: {ticker}")
            print(f"Relevance Score: {relevance_score}")
            print(f"Ticker Sentiment Score: {ticker_sentiment_score_str}")
            print(f"Inferred Sentiment: {sentiment_label}")
            print("Source:", article.get("source", "N/A"))
            print("Title:", article.get("title", "N/A"))
            print("Summary:", summary)
            print("Published At:", formatted_date)
            print("URL:", article.get("url", "N/A"))
            print(f"NLTK Sentiment (VADER): {sentiment}")
            print()

    except Exception:
        error_message = traceback.format_exc()
        log_error_to_db(
            file_name=os.path.basename(__file__),
            error_description=error_message,
            created_by=None,
            env="dev"
        )
        continue
