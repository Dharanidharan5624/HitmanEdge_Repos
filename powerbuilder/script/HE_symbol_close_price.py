import yfinance as yf
import numpy as np
import traceback
import os
from HE_database_connect import get_connection
from HE_error_logs import log_error_to_db


indices = {
    "Dow Jones": "^DJI",
    "Russell 2000": "^RUT",
    "S&P 500": "^GSPC",
    "CBOE Volatility Index": "^VIX"
}


def fetch_index_data(symbol):
    """Fetch latest close and percent change for a given market index."""
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="2d")
        data = data.dropna(subset=["Open", "Close"])

        if data.empty:
            print(f"📭 No valid data returned for {symbol}")
            return None, None

        open_price = data['Open'].iloc[-1]
        close_price = data['Close'].iloc[-1]

        if open_price == 0:
            print(f"⚠️ Open price is zero for {symbol}")
            return None, None

        percent_change = ((close_price - open_price) / open_price) * 100

        if np.isnan(percent_change) or np.isinf(percent_change):
            print(f"⚠️ Invalid percent change for {symbol}")
            return None, None

        return float(round(close_price, 2)), float(round(percent_change, 2))

    except Exception:
        error_message = traceback.format_exc()
        log_error_to_db(
            file_name=os.path.basename(__file__),
            error_description=error_message,
            created_by=None,
            env="dev"
        )
        print(f"[ERROR] Failed to fetch data for {symbol}. See logs for details.")
        return None, None


def create_table_if_not_exists(cursor):
    """Ensure he_index_data table exists before inserting."""
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS he_index_data (
                symbol VARCHAR(10) PRIMARY KEY,
                index_name VARCHAR(50),
                close_price DECIMAL(10,2),
                percent_change DECIMAL(6,2)
            )
        """)
    except Exception:
        error_message = traceback.format_exc()
        log_error_to_db(
            file_name=os.path.basename(__file__),
            error_description=error_message,
            created_by=None,
            env="dev"
        )
        print("[ERROR] Failed to create or verify table he_index_data.")


def store_index_data():
    """Fetch and store index data into the database."""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        create_table_if_not_exists(cursor)

        for name, symbol in indices.items():
            close_price, percent_change = fetch_index_data(symbol)

            if close_price is not None:
                try:
                    cursor.execute("""
                        INSERT INTO he_index_data (index_name, symbol, close_price, percent_change)
                        VALUES (%s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                            index_name = VALUES(index_name),
                            close_price = VALUES(close_price),
                            percent_change = VALUES(percent_change)
                    """, (name, symbol, close_price, percent_change))

                    print(f"✅ Inserted: {name} ({symbol}) → Close: {close_price}, Change: {percent_change}%")

                except Exception:
                    error_message = traceback.format_exc()
                    log_error_to_db(
                        file_name=os.path.basename(__file__),
                        error_description=error_message,
                        created_by=None,
                        env="dev"
                    )
                    print(f"[Insert Error] Failed to insert {symbol}. Check logs for details.")
            else:
                print(f"⚠️ Skipped: {name} ({symbol}) – Invalid or missing data")

        conn.commit()
        print("💾 All data committed to the database successfully.")

    except Exception:
        error_message = traceback.format_exc()
        log_error_to_db(
            file_name=os.path.basename(__file__),
            error_description=error_message,
            created_by=None,
            env="dev"
        )
        print("[ERROR] Failed to store index data. See logs for details.")

    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()


if __name__ == "__main__":
    store_index_data()
