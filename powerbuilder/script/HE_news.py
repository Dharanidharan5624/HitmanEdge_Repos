import traceback
import requests
import time
import schedule
import mysql.connector
import datetime
import openai
import sys
import os


sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from HE_error_logs import log_error_to_db
from HE_database_connect import get_connection

# Your OpenAI API Key
openai.api_key = "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"

# List of stock symbols you want news for
stocks = ["AAPL", "TSLA", "SPY"]

# === REPLACED hard-coded connection with get_connection() ===
db_connection = get_connection()
cursor = db_connection.cursor()
db_connection.commit()

def fetch_stock_news(stock_symbol):
    url = f"https://query2.finance.yahoo.com/v1/finance/search"
    params = {
        "q": stock_symbol,
        "quotesCount": 0,
        "newsCount": 5,  # Fetch 5 news per stock
    }
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data.get("news", [])
        else:
            print(f"Failed to fetch news for {stock_symbol}: {response.status_code}")
    except Exception as e:
        error_message = traceback.format_exc()
        log_error_to_db(
            file_name=os.path.basename(__file__),
            error_description=error_message,
            created_by=None,
            env="dev"
        )
        print(f"Error fetching news for {stock_symbol}: {e}")
    return []

def generate_summary(title, link):
    prompt = f"""
You are a financial news summarizer.
Given the following news headline and link, create a short 2-3 line summary.

Title: {title}
Link: {link}

Summary:
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0.5,
        )
        summary = response['choices'][0]['message']['content'].strip()
        return summary
    except Exception as e:
        error_message = traceback.format_exc()
        log_error_to_db(
            file_name=os.path.basename(__file__),
            error_description=error_message,
            created_by=None,
            env="dev"
        )
        return "Summary not available."

def store_news_in_db(stock_symbol, title, summary, link, pub_time):
    try:
        cursor.execute("""
            INSERT INTO he_news_articles (stock_symbol, title, summary, link, pub_time)
            VALUES (%s, %s, %s, %s, %s)
        """, (stock_symbol, title, summary, link, pub_time))
        db_connection.commit()
    except Exception as e:
        error_message = traceback.format_exc()
        log_error_to_db(
            file_name=os.path.basename(__file__),
            error_description=error_message,
            created_by=None,
            env="dev"
        )

def job():
    print(f"\nFetching news at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    for stock in stocks:
        print(f"\nFetching news for {stock}")
        news_list = fetch_stock_news(stock)

        if news_list:
            for news in news_list:
                title = news.get('title', 'No Title')
                link = news.get('link', 'No Link')

                pub_time = news.get('providerPublishTime', None)
                if pub_time:
                    pub_time = datetime.datetime.utcfromtimestamp(pub_time).strftime('%Y-%m-%d %H:%M:%S')
                else:
                    pub_time = None

                # Generate summary using GPT
                summary = generate_summary(title, link)

                # Save to DB
                store_news_in_db(stock, title, summary, link, pub_time)

                # Print
                print(f"\nTitle: {title}")
                print(f"Summary: {summary}")
                print(f"Published at: {pub_time}")
                print(f"Link: {link}\n")
        else:
            print(f"No news found for {stock}")

# Schedule to run every 10 minutes
schedule.every(10).minutes.do(job)

# Run immediately at start
job()

# Keep running
while True:
    schedule.run_pending()
    time.sleep(1)



# import requests
# import time
# import schedule
# import datetime
# import openai
# import traceback
# import sys
# import os
# import mysql.connector

# sys.path.append(os.path.abspath(os.path.dirname(__file__)))
# from HE_database_connect import get_connection
# from HE_error_logs import log_error_to_db

# openai.api_key = "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"

# stocks = ["AAPL", "TSLA", "SPY"]

# def fetch_stock_news(stock_symbol):
#     url = "https://query2.finance.yahoo.com/v1/finance/search"
#     params = {"q": stock_symbol, "quotesCount": 0, "newsCount": 5}
#     headers = {"User-Agent": "Mozilla/5.0"}

#     try:
#         response = requests.get(url, params=params, headers=headers)
#         response.raise_for_status()
#         data = response.json()
#         return data.get("news", [])
#     except Exception as e:
#         error_message = traceback.format_exc()
#         log_error_to_db(
#             file_name=os.path.basename(__file__),
#             error_description=error_message,
#             created_by="news_module",
#             env="dev"
#         )
#         print(f"[ERROR] Error fetching news for {stock_symbol}: {e}")
#         return []


# def generate_summary(title, link):
#     prompt = f"""
# You are a financial news summarizer.
# Given the following news headline and link, create a short 2-3 line summary.

# Title: {title}
# Link: {link}

# Summary:
# """
#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[{"role": "user", "content": prompt}],
#             max_tokens=100,
#             temperature=0.5,
#         )
#         return response['choices'][0]['message']['content'].strip()
#     except Exception as e:
#         error_message = traceback.format_exc()
#         log_error_to_db(
#             file_name=os.path.basename(__file__),
#             error_description=error_message,
#             created_by="news_module",
#             env="dev"
#         )
#         print(f"[ERROR] Error generating summary: {e}")
#         return "Summary not available."


# def store_news_in_db(stock_symbol, title, summary, link, pub_time):
#     try:
#         conn = get_connection()
#         cursor = conn.cursor()
#         cursor.execute("""
#             INSERT INTO he_news_articles (stock_symbol, title, summary, link, pub_time)
#             VALUES (%s, %s, %s, %s, %s)
#         """, (stock_symbol, title, summary, link, pub_time))
#         conn.commit()
#     except mysql.connector.Error as err:
#         error_message = traceback.format_exc()
#         log_error_to_db(
#             file_name=os.path.basename(__file__),
#             error_description=error_message,
#             created_by="news_module",
#             env="dev"
#         )
#         print(f"[ERROR] Database insert error: {err}")
#         return None
#     except Exception as e:
#         error_message = traceback.format_exc()
#         log_error_to_db(
#             file_name=os.path.basename(__file__),
#             error_description=error_message,
#             created_by="news_module",
#             env="dev"
#         )
#         print(f"[ERROR] Unexpected database error: {e}")
#         return None
#     finally:
#         if 'cursor' in locals():
#             cursor.close()
#         if 'conn' in locals():
#             conn.close()


# def job():
#     print(f"\n[INFO] Fetching news at {time.strftime('%Y-%m-%d %H:%M:%S')}")
#     for stock in stocks:
#         print(f"\n[INFO] Fetching news for {stock}")
#         news_list = fetch_stock_news(stock)

#         if news_list:
#             for news in news_list:
#                 title = news.get('title', 'No Title')
#                 link = news.get('link', 'No Link')
#                 pub_time_ts = news.get('providerPublishTime')
#                 pub_time = datetime.datetime.utcfromtimestamp(pub_time_ts).strftime('%Y-%m-%d %H:%M:%S') if pub_time_ts else None

#                 summary = generate_summary(title, link)
#                 store_news_in_db(stock, title, summary, link, pub_time)

#                 print(f"\n Title       : {title}")
#                 print(f" Summary     : {summary}")
#                 print(f" Published at: {pub_time}")
#                 print(f" Link        : {link}\n")
#         else:
#             print(f"[INFO] No news found for {stock}")


# def main():
#     try:
#         job()
#         schedule.every(10).minutes.do(job)
#         while True:
#             schedule.run_pending()
#             time.sleep(1)
#     except Exception as e:
#         error_message = traceback.format_exc()
#         log_error_to_db(
#             file_name=os.path.basename(__file__),
#             error_description=error_message,
#             created_by="news_module",
#             env="dev"
#         )
#         print("[ERROR] Unhandled error occurred. Logged to database.")


# if __name__ == "__main__":
#     main()
