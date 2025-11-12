import requests
import time
import pandas as pd
import yfinance as yf
from tabulate import tabulate
import mysql.connector
from mysql.connector import Error
from email.message import EmailMessage
import smtplib
import traceback
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
from HE_database_connect import get_connection
from HE_error_logs import log_error_to_db

# === CONFIG ===
API_KEY = 'd0a8q79r01qnh1rh09v0d0a8q79r01qnh1rh09vg'
start_date = datetime.today()
end_date = start_date + relativedelta(months=1)

calendar_url = f'https://finnhub.io/api/v1/calendar/earnings?from={start_date}&to={end_date}&token={API_KEY}'
company_cache = {}
EXCLUDE_KEYWORDS = ["fund", "trust", "etf", "reit", "insurance", "life", "portfolio"]

sender_email = "ila@shravtek.com"
receiver_email = "dharanidharan@shravtek.com"
subject = "Earnings Calendar Report"
app_password = "evte bupb ivnq hsyh"


def convert_hour(hour_code):
    if not hour_code:
        return 'NULL'
    hour_code = hour_code.lower()
    return {
        'bmo': 'Before Market Open',
        'amc': 'After Market Close',
        'dmt': 'During Market Trading'
    }.get(hour_code, 'NULL')


def get_company_name(symbol):
    if symbol in company_cache:
        return company_cache[symbol]

    profile_url = f'https://finnhub.io/api/v1/stock/profile2?symbol={symbol}&token={API_KEY}'
    while True:
        try:
            response = requests.get(profile_url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                name = data.get('name', 'N/A')
                company_cache[symbol] = name
                return name
            elif response.status_code == 429:
                print(f"Rate limit hit for {symbol}. Retrying in 60 sec...")
                time.sleep(60)
                continue
            else:
                print(f"Failed to fetch profile for {symbol}: {response.status_code}")
                return 'N/A'
        except Exception:
            error_message = traceback.format_exc()
            log_error_to_db(
                file_name=os.path.basename(__file__),
                error_description=error_message,
                created_by=None,
                env="dev"
            )
            return 'N/A'


def get_actual_eps(symbol, earnings_date):
    earnings_url = f'https://finnhub.io/api/v1/stock/earnings?symbol={symbol}&token={API_KEY}'
    while True:
        try:
            response = requests.get(earnings_url, timeout=5)
            if response.status_code == 200:
                for record in response.json():
                    if record.get("period", "").startswith(earnings_date):
                        return record.get("actual", None)
                return None
            elif response.status_code == 429:
                print(f"Rate limit hit on earnings for {symbol}. Retrying in 60 sec...")
                time.sleep(60)
                continue
            else:
                print(f"Failed to fetch EPS for {symbol}: {response.status_code}")
                return None
        except Exception:
            error_message = traceback.format_exc()
            log_error_to_db(
                file_name=os.path.basename(__file__),
                error_description=error_message,
                created_by=None,
                env="dev"
            )
            return None


def get_last_year_eps(symbol, current_date):
    earnings_url = f'https://finnhub.io/api/v1/stock/earnings?symbol={symbol}&token={API_KEY}'
    current_year = int(current_date[:4])
    while True:
        try:
            response = requests.get(earnings_url, timeout=5)
            if response.status_code == 200:
                for record in response.json():
                    if record.get("period", "").startswith(str(current_year - 1)):
                        return record.get("actual", None)
                return None
            elif response.status_code == 429:
                print(f"Rate limit hit on earnings for {symbol}. Retrying in 60 sec...")
                time.sleep(60)
                continue
            else:
                print(f"Failed to fetch last year EPS for {symbol}: {response.status_code}")
                return None
        except Exception:
            error_message = traceback.format_exc()
            log_error_to_db(
                file_name=os.path.basename(__file__),
                error_description=error_message,
                created_by=None,
                env="dev"
            )
            return None


def create_mysql_connection():
    try:
        conn = get_connection()
        print("✅ Connected to MySQL database")
        return conn
    except Exception:
        error_message = traceback.format_exc()
        log_error_to_db(
            file_name=os.path.basename(__file__),
            error_description=error_message,
            created_by=None,
            env="dev"
        )
        return None


def format_market_cap(value):
    if value is None:
        return 'NULL'
    try:
        return f"${value / 1e9:.2f}B"
    except Exception:
        error_message = traceback.format_exc()
        log_error_to_db(
            file_name=os.path.basename(__file__),
            error_description=error_message,
            created_by=None,
            env="dev"
        )
        return 'NULL'


def main():
    try:
        response = requests.get(calendar_url, timeout=15)
        response.raise_for_status()
    except Exception:
        error_message = traceback.format_exc()
        log_error_to_db(
            file_name=os.path.basename(__file__),
            error_description=error_message,
            created_by=None,
            env="dev"
        )
        print("[ERROR] Failed to fetch earnings calendar.")
        return

    earnings = response.json().get('earningsCalendar', [])
    if not earnings:
        print("No earnings data found.")
        return

    results = []

    for e in earnings:
        symbol = e.get('symbol')
        if not symbol:
            continue

        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            market_cap = info.get("marketCap", 0)
            if not market_cap or market_cap < 1_000_000_000:
                continue
            formatted_cap = format_market_cap(market_cap)
        except Exception:
            error_message = traceback.format_exc()
            log_error_to_db(
                file_name=os.path.basename(__file__),
                error_description=error_message,
                created_by=None,
                env="dev"
            )
            continue

        earnings_date = e.get('date')
        eps_estimate = e.get('epsEstimate')
        time_str = convert_hour(e.get('hour'))
        company_name = get_company_name(symbol)

        if any(keyword in company_name.lower() for keyword in EXCLUDE_KEYWORDS):
            continue

        actual_eps = get_actual_eps(symbol, earnings_date)
        last_year_eps = get_last_year_eps(symbol, earnings_date)

        try:
            hist = ticker.history(period='1mo')
            current_price = hist['Close'].iloc[-1] if not hist.empty else None
            volatility = hist['Close'].pct_change().std() * (252**0.5) if not hist.empty else None
        except Exception:
            error_message = traceback.format_exc()
            log_error_to_db(
                file_name=os.path.basename(__file__),
                error_description=error_message,
                created_by=None,
                env="dev"
            )
            current_price = None
            volatility = None

        results.append({
            "Company Name": company_name,
            "Ticker Symbol": symbol,
            "Earnings Date": earnings_date,
            "Time": time_str,
            "EPS Estimate": eps_estimate,
            "Actual EPS": actual_eps,
            "Last Year EPS": last_year_eps,
            "Market Cap": formatted_cap,
            "Current Price": f"${current_price:.2f}" if current_price else "NULL",
            "Volatility": f"{volatility:.2%}" if volatility else "NULL"
        })

    if not results:
        print("No qualifying earnings found.")
        return

    df = pd.DataFrame(results)
    print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False))

    # === Store to DB ===
    conn = create_mysql_connection()
    if conn:
        try:
            cursor = conn.cursor()
            insert_sql = '''
                INSERT INTO he_upcoming_earning_report (
                    company_name, ticker_symbol, earnings_date, time, eps_estimate,
                    actual_eps, last_year_eps, market_cap, current_price, volatility
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            '''
            values = [
                (r["Company Name"], r["Ticker Symbol"], r["Earnings Date"], r["Time"],
                 r["EPS Estimate"], r["Actual EPS"], r["Last Year EPS"], r["Market Cap"],
                 r["Current Price"], r["Volatility"])
                for r in results
            ]
            cursor.executemany(insert_sql, values)
            conn.commit()
            print(f"✅ {cursor.rowcount} records inserted into MySQL.")
        except Exception:
            error_message = traceback.format_exc()
            log_error_to_db(
                file_name=os.path.basename(__file__),
                error_description=error_message,
                created_by=None,
                env="dev"
            )
        finally:
            conn.close()

    # === Send Email ===
    try:
        html_body = "<html><body><h2>Earnings Calendar Report</h2><table border='1'>"
        html_body += "".join([
            f"<tr><td>{r['Company Name']}</td><td>{r['Ticker Symbol']}</td><td>{r['Earnings Date']}</td>"
            f"<td>{r['Time']}</td><td>{r['EPS Estimate']}</td><td>{r['Actual EPS']}</td>"
            f"<td>{r['Last Year EPS']}</td><td>{r['Market Cap']}</td>"
            f"<td>{r['Current Price']}</td><td>{r['Volatility']}</td></tr>"
            for r in results
        ])
        html_body += "</table></body></html>"

        msg = EmailMessage()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg.set_content("This is an HTML email report.")
        msg.add_alternative(html_body, subtype='html')

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, app_password)
            smtp.send_message(msg)
        print("✅ Email sent successfully!")

    except Exception:
        error_message = traceback.format_exc()
        log_error_to_db(
            file_name=os.path.basename(__file__),
            error_description=error_message,
            created_by=None,
            env="dev"
        )
        print("[ERROR] Email sending failed.")


if __name__ == "__main__":
    main()
