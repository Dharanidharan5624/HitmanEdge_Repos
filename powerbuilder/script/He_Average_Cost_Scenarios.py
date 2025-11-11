from collections import deque
from tabulate import tabulate
import mysql.connector
import traceback
import os
import sys
from decimal import Decimal, InvalidOperation

# Add the script's directory for imports
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from HE_error_logs import log_error_to_db
from HE_database_connect import get_connection


def safe_float(value, default=0.0):
    """Safely convert Decimal or None to float."""
    if value is None:
        return default
    if isinstance(value, Decimal):
        return float(value)
    try:
        return float(value)
    except (TypeError, ValueError, InvalidOperation):
        return default


def process_buy(holdings, cumulative_buy_cost, one, balance_qty, date, ticker, buy_qty, price):
    buy_qty = safe_float(buy_qty)
    price = safe_float(price)

    total_cost = buy_qty * price
    holdings.append([buy_qty, price, buy_qty])

    cumulative_buy_cost += total_cost
    one += buy_qty
    balance_qty += buy_qty

    avg_cost = cumulative_buy_cost / balance_qty if balance_qty > 0 else 0

    return holdings, cumulative_buy_cost, one, balance_qty, [
        date, ticker, "Buy", buy_qty, None,
        price, None, None, total_cost, None,
        cumulative_buy_cost, balance_qty, round(avg_cost, 2)
    ]


def process_sell(holdings, cumulative_buy_cost, one, balance_qty, date, ticker, sell_qty, price, sale_price):
    sell_qty = safe_float(sell_qty)
    price = safe_float(price)
    sale_price = safe_float(sale_price)

    if not holdings or sell_qty <= 0:
        print(f"[WARN] No holdings or invalid sell quantity for {ticker}.")
        return holdings, cumulative_buy_cost, one, balance_qty, []

    realized_cost = 0
    total_sell_value = 0
    sell_profit = 0
    qty_to_sell = sell_qty

    while qty_to_sell > 0 and holdings:
        buy_qty, buy_price, bal_qty = holdings[0]
        buy_price = safe_float(buy_price)
        qty_sold = min(qty_to_sell, bal_qty)

        realized_cost += qty_sold * buy_price
        sell_profit += (sale_price - buy_price) * qty_sold
        total_sell_value += qty_sold * sale_price

        if qty_sold == bal_qty:
            holdings.popleft()
        else:
            holdings[0][2] -= qty_sold

        qty_to_sell -= qty_sold

    cumulative_buy_cost -= realized_cost
    one -= sell_qty
    balance_qty -= sell_qty
    avg_cost = cumulative_buy_cost / balance_qty if balance_qty > 0 else 0

    return holdings, cumulative_buy_cost, one, balance_qty, [
        date, ticker, "Sell", sell_qty, one, price, sale_price, round(sell_profit, 2),
        realized_cost, round(total_sell_value, 2),
        cumulative_buy_cost, balance_qty, round(avg_cost, 2)
    ]


def fifo_tracker(transactions, cursor, db):
    holdings = deque()
    balance_qty = 0
    cumulative_buy_cost = 0
    one = 0
    transaction_results = []
    insert_queries = []

    for date, ticker, action, qty, price, *sale_price in transactions:
        action = str(action).strip().capitalize()
        if action not in ["Buy", "Sell"]:
            print(f"[WARN] Skipping unknown action: {action}")
            continue

        if action == "Buy":
            holdings, cumulative_buy_cost, one, balance_qty, result = process_buy(
                holdings, cumulative_buy_cost, one, balance_qty, date, ticker, qty, price
            )
        else:
            sale_price_val = sale_price[0] if sale_price and sale_price[0] is not None else price
            holdings, cumulative_buy_cost, one, balance_qty, result = process_sell(
                holdings, cumulative_buy_cost, one, balance_qty, date, ticker, qty, price, sale_price_val
            )

        if result:
            cleaned_result = [safe_float(v) if isinstance(v, (int, float, Decimal, type(None))) else v for v in result]
            transaction_results.append(cleaned_result)
            insert_queries.append(tuple(cleaned_result))

    if insert_queries:
        cursor.executemany("""
            INSERT INTO he_avgs (
                date, ticker, action, qty, balance_qty, price, sale_price, sell_profit,
                total_cost, sell_total_profit, cumulative_buy_cost, cumulative_total_qty, avg_cost
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, insert_queries)
        db.commit()

    return tabulate(transaction_results, headers=[
        "Date", "Ticker", "Buy/Sell", "Qty", "Balance Qty", "Price", "Sale Price",
        "Sell Profit", "Total Cost", "Sell Total Profit", "Cumulative Total Cost",
        "Cumulative Total Qty", "Average Cost"
    ], tablefmt="grid")


def store_data_in_db(data):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        result_table = fifo_tracker(data, cursor, conn)
        cursor.close()
        conn.close()
        print("[INFO] FIFO data stored successfully.")
        return result_table

    except mysql.connector.Error:
        error_message = traceback.format_exc()
        log_error_to_db(os.path.basename(__file__), error_message, created_by=None, env="dev")
        print(f"[ERROR] Database insert error:\n{error_message}")
        return None

    except Exception:
        error_message = traceback.format_exc()
        log_error_to_db(os.path.basename(__file__), error_message, created_by=None, env="dev")
        print(f"[ERROR] Unexpected error:\n{error_message}")
        return None


def fetch_fifo_data():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT date, ticker, trade_type, quantity, price
            FROM he_stock_transaction
            WHERE ticker IS NOT NULL
            ORDER BY ticker ASC;
        """)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        print("[INFO] Fetched Transactions:")
        print(tabulate(rows, headers=["Date", "Ticker", "Action", "Qty", "Price"], tablefmt="grid"))

        # Add placeholder for sale_price (None)
        return [tuple(list(row) + [None]) for row in rows]

    except mysql.connector.Error:
        error_message = traceback.format_exc()
        log_error_to_db(os.path.basename(__file__), error_message, created_by=None, env="dev")
        print(f"[ERROR] Error fetching stock data:\n{error_message}")
        return []

    except Exception:
        error_message = traceback.format_exc()
        log_error_to_db(os.path.basename(__file__), error_message, created_by=None, env="dev")
        print(f"[ERROR] Unexpected error fetching FIFO data:\n{error_message}")
        return []


def main():
    try:
        transactions = fetch_fifo_data()
        if transactions:
            output_table = store_data_in_db(transactions)
            if output_table:
                print("\n[INFO] FIFO Calculation Result:")
                print(output_table)
        else:
            print("[WARNING] No transactions found to process.")
    except Exception:
        error_message = traceback.format_exc()
        log_error_to_db(os.path.basename(__file__), error_message, created_by=None, env="dev")
        print(f"[ERROR] Unexpected failure in main():\n{error_message}")


if __name__ == "__main__":
    main()
