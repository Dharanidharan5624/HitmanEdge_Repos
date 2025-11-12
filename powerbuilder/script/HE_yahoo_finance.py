import feedparser
from datetime import datetime
from urllib.parse import urlparse, parse_qs
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os
import traceback
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
        return {"compound": 0.0}

def sentiment_label(compound_score):
    if compound_score >= 0.05:
        return "Positive"
    elif compound_score <= -0.05:
        return "Negative"
    else:
        return "Neutral"

def fetch_feed(symbol):
    try:
        url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={symbol}&region=US&lang=en-US"
        return feedparser.parse(url), url
    except Exception:
        error_message = traceback.format_exc()
        log_error_to_db(
            file_name=os.path.basename(__file__),
            error_description=error_message,
            created_by=None,
            env="dev"
        )
        return None, None

def extract_tickers_from_url(url):
    try:
        parsed = urlparse(url)
        return parse_qs(parsed.query).get("s", ["Unknown"])[0].split(",")
    except Exception:
        error_message = traceback.format_exc()
        log_error_to_db(
            file_name=os.path.basename(__file__),
            error_description=error_message,
            created_by=None,
            env="dev"
        )
        return ["Unknown"]

def parse_articles(feed, symbols, limit=7):
    count = 0
    for entry in feed.entries:
        if count >= limit:
            break
        try:
            summary = entry.summary
            sentiment_scores = analyze_sentiment(summary)
            label = sentiment_label(sentiment_scores["compound"])
            print(f"Tickers: {', '.join(symbols)}")
            print(f"Published: {entry.published}")
            print(f"Title: {entry.title}")
            print(f"Summary: {summary}")
            print(f"Link: {entry.link}")
            print(f"Sentiment Score: {sentiment_scores}")
            print(f"Final Sentiment Label: {label}")
            print("-" * 60)
            count += 1
        except Exception:
            error_message = traceback.format_exc()
            log_error_to_db(
                file_name=os.path.basename(__file__),
                error_description=error_message,
                created_by=None,
                env="dev"
            )
            continue

def main():
    try:
        symbol = "HIMS"
        feed, url = fetch_feed(symbol)
        if not feed or not feed.entries:
            error_message = f"No feed or entries found for {symbol}"
            log_error_to_db(
                file_name=os.path.basename(__file__),
                error_description=error_message,
                created_by=None,
                env="dev"
            )
            print(f"No articles found for {symbol}")
            return
        symbols = extract_tickers_from_url(url)
        print(f"Analyzing latest news for {symbol}...\n")
        parse_articles(feed, symbols, limit=7)
    except Exception:
        error_message = traceback.format_exc()
        log_error_to_db(
            file_name=os.path.basename(__file__),
            error_description=error_message,
            created_by=None,
            env="dev"
        )

if __name__ == "__main__":
    main()
