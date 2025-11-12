

import sys
from ib_insync import *
import mysql.connector
from collections import defaultdict
import yfinance as yf

# ===============================
# IBKR CONNECTION SETTINGS
# ===============================
IB_HOST = '127.0.0.1'
IB_PORT = 4002      # Paper trading port
CLIENT_ID = 1       # Any unique integer

# Connect to IBKR
ib = IB()
try:
    ib.connect(IB_HOST, IB_PORT, clientId=CLIENT_ID)
    print("✅ Connected to IBKR")
except Exception as e:
    print(f"❌ IBKR connection failed: {e}")
    sys.exit(1)

# ===============================
# Database config
# ===============================
DB_CONFIG = {
    "host": "localhost",
    "user": "Hitman",
    "password": "Hitman@123",
    "database": "hitman_edge_dev"
}

# ===============================
# Fetch transactions
# ===============================
def fetch_transactions():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT ticker, trade_type, quantity, price, created_by
            FROM he_portfolio_master;
        """)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except mysql.connector.Error as err:
        print(f"⚠️ Database error: {err}")
        return []

# ===============================
# Calculate average cost
# ===============================
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

# ===============================
# Fetch stock price from Yahoo Finance
# ===============================
def get_stock_price(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period="1d")
    if not data.empty:
        return float(data['Close'].iloc[-1])
    return None

# ===============================
# Store order in database
# ===============================
def store_order_in_db(ticker, order_id, quantity, avg_cost, Stock_Price, Buy_Qty, Sell_Qty, created_by):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        sql = """
            INSERT INTO he_stocks_ibkr
            (ticker, order_id, quantity, avg_cost, Stock_Price, Buy_Qty, Sell_Qty, created_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (ticker, order_id, quantity, avg_cost, Stock_Price, Buy_Qty, Sell_Qty, created_by))
        conn.commit()
        print(f"💾 Order saved in database (Order ID: {order_id}, Stock Price: {Stock_Price})")
    except mysql.connector.Error as err:
        print(f"⚠️ Failed to save order: {err}")
    finally:
        cursor.close()
        conn.close()

# ===============================
# Place order on IBKR
# ===============================
def place_order(symbol, qty, side, created_by, avg_cost_dict):
    contract = Stock(symbol, 'SMART', 'USD')  # Modify for NSE/INR if needed
    order_type = MarketOrder(side.upper(), qty)

    try:
        trade = ib.placeOrder(contract, order_type)
        ib.sleep(1)  # Give IBKR some time to process
        order_id = trade.order.permId
        print(f"✅ Order submitted: {side.upper()} {qty} of {symbol} (Order ID: {order_id})")

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
        store_order_in_db(symbol, order_id, qty, avg_cost, stock_price, Buy_Qty, Sell_Qty, created_by)

        # Print stock price
        print(f"💹 Current Stock Price for {symbol}: {stock_price}")

    except Exception as e:
        print(f"❌ Order failed: {e}")
        sys.exit(1)

# ===============================
# Main
# ===============================
def main():
    if len(sys.argv) != 5:
        print("❌ Usage: python ibkr_order.py <ticker> <buy_qty> <sell_qty> <created_by>")
        sys.exit(1)

    ticker = sys.argv[1].upper()
    try:
        buy_qty = int(sys.argv[2])
        sell_qty = int(sys.argv[3])
        created_by = int(sys.argv[4])
    # ticker = "TSLA"
    # try:
    #     buy_qty = 10
    #     sell_qty = 0
    #     created_by = 1
    except ValueError:
        print("❌ Buy/Sell quantities and created_by must be integers.")
        sys.exit(1)

    if buy_qty > 0 and sell_qty > 0:
        print("❌ Either Buy Qty or Sell Qty, not both.")
        sys.exit(1)
    if buy_qty == 0 and sell_qty == 0:
        print("❌ Both Buy and Sell quantities are zero.")
        sys.exit(1)

    side = 'buy' if buy_qty > 0 else 'sell'
    qty = buy_qty if buy_qty > 0 else sell_qty

    print(f"▶️ Processing: {ticker} {side.upper()} {qty}")

    transactions = fetch_transactions()
    avg_cost_dict = calculate_avg_cost(transactions) if transactions else {}

    place_order(ticker, qty, side, created_by, avg_cost_dict)


if __name__ == "__main__":
    main()
