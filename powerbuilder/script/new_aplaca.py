# import sys
# import mysql.connector
# from decimal import Decimal
# from collections import defaultdict
# import alpaca_trade_api as tradeapi

# # ===== Alpaca API credentials =====
# API_KEY = 'PKN1L7U3BZEVGUKGWJDZ'
# API_SECRET = 'rsH97z6DuBMBXbhoFtmILPlEmU8S94Wrln1WShH2'
# BASE_URL = 'https://paper-api.alpaca.markets'

# # Initialize Alpaca API
# api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

# # ===== Fetch transactions (optional) =====
# def fetch_transactions():
#     try:
#         conn = mysql.connector.connect(
#             host="localhost",
#             user="Hitman",
#             password="Hitman@123",
#             database="hitman_edge_dev"
#         )
#         cursor = conn.cursor()
#         cursor.execute("""
#             SELECT ticker, trade_type, quantity, price, created_by
#             FROM he_stock_transaction;
#         """)
#         rows = cursor.fetchall()
#         cursor.close()
#         conn.close()
#         return rows
#     except mysql.connector.Error as err:
#         print(f"⚠️ Database error: {err}")
#         return []

# # ===== Calculate average cost (optional) =====
# def calculate_avg_cost(transactions):
#     total_cost = defaultdict(float)
#     total_qty = defaultdict(float)
#     for ticker, trade_type, qty, price, created_by in transactions:
#         if trade_type.lower() == 'buy':
#             qty_f = float(qty)
#             price_f = float(price) if price is not None else 0.0
#             total_cost[(ticker, created_by)] += qty_f * price_f
#             total_qty[(ticker, created_by)] += qty_f
#     avg_cost = {}
#     for key in total_cost:
#         avg_cost[key] = total_cost[key] / total_qty[key] if total_qty[key] != 0 else 0.0
#     return avg_cost

# # ===== Place order on Alpaca =====
# def place_order(symbol, qty, side):
#     try:
#         order = api.submit_order(
#             symbol=symbol,
#             qty=qty,
#             side=side,
#             type='market',
#             time_in_force='gtc'
#         )
#         print(f"✅ Order submitted: {side.upper()} {qty} of {symbol} (Order ID: {order.id})")
#     except Exception as e:
#         print(f"❌ Order failed: {e}")
#         sys.exit(1)  # Exit with error for PowerBuilder detection

# # ===== Main =====
# def main():
#     # Must have exactly 3 args: ticker, buy_qty, sell_qty
#     if len(sys.argv) != 4:
#         print("❌ Usage: new_aplaca.py <ticker> <buy_qty> <sell_qty>")
#         sys.exit(1)

#         ticker = sys.argv[1].upper()
# #ticker = "AAPL"
#     print(f" Processing order for ticker: {ticker}")
#     try:
#         buy_qty = int(sys.argv[2])
#         # buy_qty = 100
#         print(f" Buy Quantity: {buy_qty}")
#         sell_qty = int(sys.argv[3])
#         # sell_qty = 0
#         print(f" Sell Quantity: {sell_qty}")
#     except ValueError:
#         print("❌ Buy/Sell quantities must be integers")
#         sys.exit(1)

#     # Validate quantities
#     if buy_qty > 0 and sell_qty > 0:
#         print("❌ Error: Enter either Buy Qty or Sell Qty, not both.")
#         sys.exit(1)
#     if buy_qty == 0 and sell_qty == 0:
#         print("❌ Error: Both Buy and Sell quantities are zero.")
#         sys.exit(1)

#     # Determine side
#     if buy_qty > 0:
#         side = 'buy'
#         qty = buy_qty
#     else:
#         side = 'sell'
#         qty = sell_qty

#     print(f"▶️ Received from PowerBuilder: {ticker} {side.upper()} {qty}")

#     # Optional: fetch transactions
#     transactions = fetch_transactions()
#     if transactions:
#         avg_cost = calculate_avg_cost(transactions)
#         print("ℹ️Average cost per user calculated.")

#     # Place the order
#     place_order(ticker, qty, side)

#     # Exit successfully
#     sys.exit(0)

# # ===== Entry point =====
# if __name__ == "__main__":
#     main()


<<<<<<< HEAD
import sys, os, traceback
import alpaca_trade_api as tradeapi
import yfinance as yf
from collections import defaultdict
from HE_database_connect import get_connection
from HE_error_logs import log_error_to_db

API_KEY = 'PKN1L7U3BZEVGUKGWJDZ'
API_SECRET = 'rsH97z6DuBMBXbhoFtmILPlEmU8S94Wrln1WShH2'
BASE_URL = 'https://paper-api.alpaca.markets'
api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')


def fetch_transactions():
    try:
        conn = get_connection("dev")
        cursor = conn.cursor()
        cursor.execute("SELECT ticker, trade_type, quantity, price, created_by FROM he_stock_transaction;")
=======
import sys
import mysql.connector
from collections import defaultdict
import alpaca_trade_api as tradeapi
import yfinance as yf
import time

# ===== Alpaca API credentials =====
API_KEY = 'PKN1L7U3BZEVGUKGWJDZ'
API_SECRET = 'rsH97z6DuBMBXbhoFtmILPlEmU8S94Wrln1WShH2'
BASE_URL = 'https://paper-api.alpaca.markets'

# Initialize Alpaca API
api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

# ===== Database config =====
DB_CONFIG = {
    "host": "localhost",
    "user": "Hitman",
    "password": "Hitman@123",
    "database": "hitman_edge_dev"
}

# ===== Fetch transactions =====
def fetch_transactions():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT ticker, trade_type, quantity, price, created_by
            FROM he_stock_transaction;
        """)
>>>>>>> a9ff66d5af73e6700e760620d89ca5cc37d6d42c
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
<<<<<<< HEAD
    except Exception:
        error_message = traceback.format_exc()
        log_error_to_db(
            file_name=os.path.basename(__file__),
            error_description=error_message,
            created_by=None,
            env="dev"
        )
        return []


def calculate_avg_cost(transactions):
    total_cost, total_qty = defaultdict(float), defaultdict(float)
    for ticker, trade_type, qty, price, created_by in transactions:
        if trade_type.lower() == 'buy':
            qty, price = float(qty), float(price or 0)
            total_cost[(ticker, created_by)] += qty * price
            total_qty[(ticker, created_by)] += qty
    return {key: total_cost[key] / total_qty[key] if total_qty[key] else 0.0 for key in total_cost}


def get_stock_price(ticker):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d")
        return float(data['Close'].iloc[-1]) if not data.empty else None
    except Exception:
        error_message = traceback.format_exc()
        log_error_to_db(
            file_name=os.path.basename(__file__),
            error_description=error_message,
            created_by=None,
            env="dev"
        )
        return None


def store_order_in_db(ticker, order_id, quantity, avg_cost, stock_price, buy_qty, sell_qty, created_by):
    try:
        conn = get_connection("dev")
=======
    except mysql.connector.Error as err:
        print(f"⚠️ Database error: {err}")
        return []

# ===== Calculate average cost =====
def calculate_avg_cost(transactions):
    total_cost = defaultdict(float)
    total_qty = defaultdict(float)
    for ticker, trade_type, qty, price, created_by in transactions:
        if trade_type.lower() == 'buy':
            qty_f = float(qty)
            price_f = float(price) if price is not None else 0.0
            total_cost[(ticker, created_by)] += qty_f * price_f
            total_qty[(ticker, created_by)] += qty_f
    avg_cost = {}
    for key in total_cost:
        avg_cost[key] = total_cost[key] / total_qty[key] if total_qty[key] != 0 else 0.0
    return avg_cost

# ===== Fetch stock price from Yahoo Finance =====
def get_stock_price(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period="1d")
    if not data.empty:
        return float(data['Close'].iloc[-1])
    return None

# ===== Store order in database =====
def store_order_in_db(ticker, order_id, quantity, avg_cost, Stock_Price, Buy_Qty, Sell_Qty, created_by):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
>>>>>>> a9ff66d5af73e6700e760620d89ca5cc37d6d42c
        cursor = conn.cursor()
        sql = """
            INSERT INTO he_stocks_ibkr
            (ticker, order_id, quantity, avg_cost, Stock_Price, Buy_Qty, Sell_Qty, created_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
<<<<<<< HEAD
        cursor.execute(sql, (ticker, order_id, quantity, avg_cost, stock_price, buy_qty, sell_qty, created_by))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"💾 Order saved (Order ID: {order_id}, Price: {stock_price})")
    except Exception:
        error_message = traceback.format_exc()
        log_error_to_db(
            file_name=os.path.basename(__file__),
            error_description=error_message,
            created_by=None,
            env="dev"
        )


=======
        cursor.execute(sql, (ticker, order_id, quantity, avg_cost, Stock_Price, Buy_Qty, Sell_Qty, created_by))
        conn.commit()
        print(f"💾 Order saved in database (Order ID: {order_id}, Stock Price: {Stock_Price})")
    except mysql.connector.Error as err:
        print(f"⚠️ Failed to save order: {err}")
    finally:
        cursor.close()
        conn.close()

# ===== Place order on Alpaca =====
>>>>>>> a9ff66d5af73e6700e760620d89ca5cc37d6d42c
def place_order(symbol, qty, side, created_by, avg_cost_dict):
    try:
        order = api.submit_order(
            symbol=symbol,
            qty=qty,
            side=side,
            type='market',
            time_in_force='gtc'
        )
<<<<<<< HEAD
        print(f"✅ Order submitted: {side.upper()} {qty} {symbol} (Order ID: {order.id})")
        buy_qty, sell_qty = (qty, 0) if side == 'buy' else (0, qty)
        avg_cost = avg_cost_dict.get((symbol, created_by), 0.0)
        stock_price = get_stock_price(symbol) or 0.0
        store_order_in_db(symbol, order.id, qty, avg_cost, stock_price, buy_qty, sell_qty, created_by)
        print(f"💹 {symbol} price: {stock_price}")
    except Exception:
        error_message = traceback.format_exc()
        log_error_to_db(
            file_name=os.path.basename(__file__),
            error_description=error_message,
            created_by=None,
            env="dev"
        )
        print("❌ Order failed")
        sys.exit(1)


def main():
    if len(sys.argv) != 5:
        print("Usage: python new_alpaca.py <ticker> <buy_qty> <sell_qty> <created_by>")
        sys.exit(1)

    ticker = sys.argv[1].upper()
    try:
        buy_qty, sell_qty, created_by = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
=======
        print(f"✅ Order submitted: {side.upper()} {qty} of {symbol} (Order ID: {order.id})")

        # Determine Buy/Sell quantities
        Buy_Qty = qty if side == 'buy' else 0
        Sell_Qty = qty if side == 'sell' else 0

        # Get avg cost from previous transactions if available
        avg_cost = avg_cost_dict.get((symbol, created_by), 0.0)

        # Fetch current stock price from Yahoo Finance
        stock_price = get_stock_price(symbol)
        if stock_price is None:
            print(f"❌ Failed to fetch stock price for {symbol}")
            stock_price = 0.0

        # Store order in DB
        store_order_in_db(symbol, order.id, qty, avg_cost, stock_price, Buy_Qty, Sell_Qty, created_by)

        # Print stock price
        print(f"💹 Current Stock Price for {symbol}: {stock_price}")

    except Exception as e:
        print(f"❌ Order failed: {e}")
        sys.exit(1)

# ===== Main =====
def main():
    # Must have exactly 4 args: ticker, buy_qty, sell_qty, created_by
    if len(sys.argv) != 5:
        print("❌ Usage: python new_alpaca.py <ticker> <buy_qty> <sell_qty> <created_by>")
        sys.exit(1)

    # Parse arguments
    ticker = sys.argv[1].upper()
    try:
        buy_qty = int(sys.argv[2])
        sell_qty = int(sys.argv[3])
        created_by = int(sys.argv[4])
>>>>>>> a9ff66d5af73e6700e760620d89ca5cc37d6d42c
    except ValueError:
        print("❌ Buy/Sell quantities and created_by must be integers.")
        sys.exit(1)

<<<<<<< HEAD
    if (buy_qty > 0 and sell_qty > 0) or (buy_qty == 0 and sell_qty == 0):
        print("❌ Invalid buy/sell quantities.")
        sys.exit(1)

    side = 'buy' if buy_qty > 0 else 'sell'
    qty = buy_qty or sell_qty
    print(f"▶️ Processing: {ticker} {side.upper()} {qty}")

    transactions = fetch_transactions()
    avg_cost_dict = calculate_avg_cost(transactions) if transactions else {}
    place_order(ticker, qty, side, created_by, avg_cost_dict)

=======
    # Validate quantities
    if buy_qty > 0 and sell_qty > 0:
        print("❌ Either Buy Qty or Sell Qty, not both.")
        sys.exit(1)
    if buy_qty == 0 and sell_qty == 0:
        print("❌ Both Buy and Sell quantities are zero.")
        sys.exit(1)

    side = 'buy' if buy_qty > 0 else 'sell'
    qty = buy_qty if buy_qty > 0 else sell_qty

    print(f"▶️ Processing: {ticker} {side.upper()} {qty}")

    # Fetch transactions and calculate avg cost
    transactions = fetch_transactions()
    avg_cost_dict = calculate_avg_cost(transactions) if transactions else {}

    # Place order
    place_order(ticker, qty, side, created_by, avg_cost_dict)
>>>>>>> a9ff66d5af73e6700e760620d89ca5cc37d6d42c

if __name__ == "__main__":
    main()
