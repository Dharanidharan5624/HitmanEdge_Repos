from tabulate import tabulate
from HE_database_connect import get_connection
from HE_error_logs import log_error_to_db
import pandas as pd
from collections import deque
import traceback
import os


def fetch_all_stock_data():
    """Fetch all stock data from he_stock_transaction table."""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM he_stock_transaction ORDER BY date ASC"
        cursor.execute(query)

        columns = [desc[0] for desc in cursor.description]
        result = cursor.fetchall()

        cursor.close()
        conn.close()

        if not result:
            print("[INFO] No records found in he_stock_transaction.")
        return columns, result

    except Exception:
        error_message = traceback.format_exc()
        log_error_to_db(
            file_name=os.path.basename(__file__),
            error_description=error_message,
            created_by=None,
            env="dev"
        )
        print("[DB ERROR] Failed to fetch stock data. See logs for details.")
        return None, None


if __name__ == "__main__":
    columns, data = fetch_all_stock_data()
    if data:
        print("\n=== STOCK TRANSACTIONS CHECK ===\n")
        print(tabulate(data, headers=columns, tablefmt="grid"))
    else:
        print("No data found in he_stock_transaction.\n")


class InvestmentCalculator:
    """Calculates total investment, quantity, and average price for each ticker."""

    def __init__(self):
        self.transactions = {}
        try:
            self.fetch_stock_transactions()
        except Exception:
            error_message = traceback.format_exc()
            log_error_to_db(
                file_name=os.path.basename(__file__),
                error_description=error_message,
                created_by=None,
                env="dev"
            )

    def fetch_stock_transactions(self):
        """Fetch and organize stock transactions grouped by ticker."""
        try:
            conn = get_connection()
            cursor = conn.cursor()

            query = """
            SELECT LOWER(ticker), trade_type, quantity, price, date
            FROM he_stock_transaction
            ORDER BY date ASC
            """
            cursor.execute(query)

            rows = cursor.fetchall()
            if not rows:
                print("[INFO] No transactions found in he_stock_transaction.")
                return

            for ticker, trade_type, qty, price, date in rows:
                if ticker not in self.transactions:
                    self.transactions[ticker] = {"buy": deque(), "sell": []}

                if trade_type.lower() == "buy":
                    self.transactions[ticker]["buy"].append((qty, price, date))
                elif trade_type.lower() == "sell":
                    self.transactions[ticker]["sell"].append((qty, price, date))

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
            print("[Fetch Transactions Error] Failed to load stock data from DB.")

    def calculate(self):
        """Calculate investment summary for all tickers."""
        table_data = []

        try:
            if not self.transactions:
                print("[INFO] No transactions available to calculate summary.")
                return pd.DataFrame(columns=["Ticker", "Total Investment", "Total Quantity", "Average Price"])

            for ticker, data in self.transactions.items():
                buy_queue = data["buy"]
                total_qty = 0
                total_investment = 0

                # Adjust for sold shares (FIFO)
                for sell_qty, _, _ in data["sell"]:
                    while sell_qty > 0 and buy_queue:
                        buy_qty, buy_price, _ = buy_queue.popleft()
                        if buy_qty <= sell_qty:
                            sell_qty -= buy_qty
                        else:
                            buy_queue.appendleft((buy_qty - sell_qty, buy_price, _))
                            sell_qty = 0

                # Remaining unsold shares
                for qty, price, _ in buy_queue:
                    total_qty += qty
                    total_investment += qty * price

                avg_price = total_investment / total_qty if total_qty > 0 else 0
                table_data.append([
                    ticker.upper(),
                    round(total_investment, 2),
                    total_qty,
                    round(avg_price, 2)
                ])

            df = pd.DataFrame(table_data, columns=["Ticker", "Total Investment", "Total Quantity", "Average Price"])
            df["Average Price"] = df["Average Price"].fillna(0)

            self.insert_data_into_db(df)
            return df

        except Exception:
            error_message = traceback.format_exc()
            log_error_to_db(
                file_name=os.path.basename(__file__),
                error_description=error_message,
                created_by=None,
                env="dev"
            )
            print("[Calculation Error] Failed to calculate summary.")
            return pd.DataFrame(columns=["Ticker", "Total Investment", "Total Quantity", "Average Price"])

    def insert_data_into_db(self, df):
        """Store calculated summary into he_summary table."""
        try:
            conn = get_connection()
            cursor = conn.cursor()

            for _, row in df.iterrows():
                query = """
                INSERT INTO he_summary (instrument, total_investment, total_quantity, average_price)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    total_investment = VALUES(total_investment),
                    total_quantity = VALUES(total_quantity),
                    average_price = VALUES(average_price)
                """
                cursor.execute(query, (
                    row["Ticker"],
                    row["Total Investment"],
                    row["Total Quantity"],
                    row["Average Price"]
                ))

            conn.commit()
            cursor.close()
            conn.close()
            print("\n✅ Summary data stored successfully.\n")

        except Exception:
            error_message = traceback.format_exc()
            log_error_to_db(
                file_name=os.path.basename(__file__),
                error_description=error_message,
                created_by=None,
                env="dev"
            )
            print("[Insert DB Error] Failed to insert summary into DB.")


if __name__ == "__main__":
    try:
        print("\n=== INVESTMENT SUMMARY ===\n")
        calculator = InvestmentCalculator()
        result_df = calculator.calculate()

        if not result_df.empty:
            print(tabulate(result_df, headers="keys", tablefmt="grid", showindex=False))
        else:
            print("No investment data to summarize.")
    except Exception:
        error_message = traceback.format_exc()
        log_error_to_db(
            file_name=os.path.basename(__file__),
            error_description=error_message,
            created_by=None,
            env="dev"
        )
        print("[Main Error] Program failed to execute.")
