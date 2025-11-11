import os
import time
import socket
import traceback
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from datetime import datetime
from pytz import timezone
import matplotlib.dates as mdates
from decimal import Decimal, ROUND_HALF_UP
from ib_insync import IB, Stock, MarketOrder
from HE_error_logs import log_error_to_db


us_eastern = timezone("US/Eastern")
BUY_LEVELS = ['61.8%', '78.6%']
SELL_LEVELS = ['38.2%', '23.6%']
SYMBOLS = ['AAPL', 'MSFT', 'GOOGL', 'SPY', 'META', 'NVDA', 'AMZN', 'PLTR']
QUANTITY = 10
REFRESH_INTERVAL = 150  # seconds between refreshes (used by plt.pause and retry waits)
MAX_CONNECT_RETRIES = 4
IB_CLIENT_ID = 2
IB_PORT_CANDIDATES = [7497, 4002, 7496, 4001]  # try typical TWS/Gateway ports

# state
selected_symbol = 'PLTR'
buttons = []
contract = None
bought = False
sold = False


def safe_log_exception(file_name=None, created_by=None):
    """Capture traceback and write to DB through your log_error_to_db wrapper."""
    try:
        error_message = traceback.format_exc()
        log_error_to_db(
            file_name=file_name or os.path.basename(__file__),
            error_description=error_message,
            created_by=None,
            env="dev"
        )
    except Exception:
        # avoid infinite loop if logging fails
        print("Failed to write error to DB log.")
        print(traceback.format_exc())

def to_decimal(value, places=2):
    try:
        # handle pandas Series safely
        if hasattr(value, "iloc"):
            value = value.iloc[0]
        return float(Decimal(float(value)).quantize(Decimal(f'1.{"0"*places}'), rounding=ROUND_HALF_UP))
    except Exception:
        try:
            return float(round(float(value), places))
        except Exception:
            return 0.0


def port_is_open(host: str, port: int, timeout: float = 1.0) -> bool:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            return s.connect_ex((host, port)) == 0
    except Exception:
        return False


ib = IB()
ib_connected = False
for port in IB_PORT_CANDIDATES:
    for attempt in range(1, MAX_CONNECT_RETRIES + 1):
        try:
            print(f"[IB] Trying to connect to 127.0.0.1:{port} (attempt {attempt}/{MAX_CONNECT_RETRIES})...")
            # quick local port check to avoid waiting long on connect
            if not port_is_open('127.0.0.1', port, timeout=1.0):
                print(f"[IB] port {port} not open - skipping this port attempt.")
                break
            ib.connect('127.0.0.1', port, clientId=IB_CLIENT_ID)
            ib.reqMarketDataType(1)  # real-time
            print(f"✅ Connected to IBKR on port {port}")
            ib_connected = True
            break
        except Exception:
            print(f"⚠️ Connection attempt {attempt} failed on port {port}.")
            safe_log_exception(created_by=None)
            time.sleep(2)
    if ib_connected:
        break

if not ib_connected:
    error_message = "IBKR connection could not be established on candidate ports."
    print("❌", error_message)
    safe_log_exception(created_by=None)
    # Decide: continue in dry-run mode (visual only) or exit. We'll continue but disable live orders.
    print("⚠️ Continuing in dry-run/visual-only mode (will not place live orders).")



def get_live_price_from_yf(symbol: str):
    try:
        ticker = yf.Ticker(symbol)
        live_data = ticker.history(period="1d", interval="1m")
        if live_data.empty:
            print(f"[YF] No live price data for {symbol}")
            return None
        price = float(live_data['Close'].iloc[-1])
        return price
    except Exception:
        safe_log_exception(created_by=None)
        return None

def place_order(action: str, quantity: int, price: float):
    global contract, ib_connected, ib
    try:
        if not ib_connected:
            print(f"[DRY RUN] Would place {action} {quantity} @ {price:.2f} (IB not connected).")
            return
        if contract is None:
            print("[ORDER] No qualified contract, cannot place order.")
            return
        order = MarketOrder(action, int(quantity))
        trade = ib.placeOrder(contract, order)
        print(f"[ORDER] Placed {action} for {quantity} shares (order status: {trade.orderStatus.status})")
        ib.sleep(1)
    except Exception:
        safe_log_exception(created_by=None)
        print("[ORDER] Failed to place order; see log.")


plt.ion()
fig, ax = plt.subplots(figsize=(11, 8))
plt.subplots_adjust(left=0.06, right=0.88, bottom=0.10)

def plot_fib_chart(symbol: str):
    global selected_symbol, contract
    selected_symbol = symbol
    ax.clear()
    try:
        now_est = datetime.now(us_eastern)
        # download intraday data
        df = yf.download(symbol, period='1d', interval='1m', auto_adjust=True, progress=False)
        if df.empty:
            ax.set_title(f"[{symbol}] No data")
            plt.draw()
            return {}

        # timezone safe: attempt to tz_localize then convert if required
        try:
            if df.index.tzinfo is None or df.index.tz is None:
                df.index = df.index.tz_localize('UTC').tz_convert('America/New_York')
            else:
                df.index = df.index.tz_convert('America/New_York')
        except Exception:
            # sometimes yfinance returns tz-aware index already — ignore errors
            pass

        try:
            df = df.between_time("09:30", "16:00")
        except Exception:
            # if not possible, keep full df
            pass

        if df.empty or len(df) < 10:
            ax.set_title(f"[{symbol}] Not enough data")
            plt.draw()
            return {}

        swing_high = to_decimal(df['High'].max())
        swing_low = to_decimal(df['Low'].min())
        latest_price = to_decimal(df['Close'].iloc[-1])
        diff = max(swing_high - swing_low, 0.0)

        fib_levels = {
            '23.6%': to_decimal(swing_high - 0.236 * diff),
            '38.2%': to_decimal(swing_high - 0.382 * diff),
            '61.8%': to_decimal(swing_high - 0.618 * diff),
            '78.6%': to_decimal(swing_high - 0.786 * diff),
        }

        ax.plot(df.index, df['Close'], label=f'{symbol} Close', color='skyblue')
        ax.axhline(latest_price, color='blue', linestyle='--', linewidth=1.5,
                   label=f'Current Price: ${latest_price:.2f}')

        for level, price in fib_levels.items():
            color = 'green' if level in BUY_LEVELS else 'red' if level in SELL_LEVELS else 'gray'
            ax.axhline(price, linestyle='--', linewidth=1.2, color=color, alpha=0.8)
            # place text slightly to the right of the last x index
            try:
                ax.text(df.index[-1], price, f' {level} ${price:.2f}', va='bottom', ha='right', fontsize=9)
            except Exception:
                pass

        ax.set_title(f'{symbol} Intraday Fibonacci Levels (ET: {now_est.strftime("%H:%M:%S")})')
        ax.set_xlabel('Time (Eastern)')
        ax.set_ylabel('Price (USD)')
        ax.legend(loc='best', fontsize=8)
        ax.grid(True)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('[%m/%d]\n%I:%M', tz=us_eastern))
        ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=60))
        fig.autofmt_xdate()
        plt.draw()

        # prepare IB contract
        contract = Stock(symbol, 'SMART', 'USD')
        if ib_connected:
            try:
                ib.qualifyContracts(contract)
            except Exception:
                safe_log_exception(created_by=None)
                print(f"[IB] Contract qualification failed for {symbol} (will run in dry-run mode for orders).")

        return fib_levels

    except Exception:
        safe_log_exception(created_by=None)
        ax.set_title(f"[{symbol}] Error while plotting")
        plt.draw()
        return {}



visible_buttons = 12
current_page = [0]
button_w = 0.10
button_h = 0.05
spacing = 0.01
start_x = 0.89
start_y = 0.82
buttons = []

def render_buttons(page: int):
    try:
        for b in buttons:
            b.ax.remove()
        buttons.clear()
        start_index = page * visible_buttons
        end_index = start_index + visible_buttons
        visible = SYMBOLS[start_index:end_index]
        for i, sym in enumerate(visible):
            y = start_y - i * (button_h + spacing)
            ax_button = plt.axes([start_x, y, button_w, button_h])
            b = Button(ax_button, sym)
            b.on_clicked(lambda evt, s=sym: plot_fib_chart(s))
            buttons.append(b)
        plt.draw()
    except Exception:
        safe_log_exception(created_by=None)

def scroll_up(evt):
    if current_page[0] > 0:
        current_page[0] -= 1
        render_buttons(current_page[0])

def scroll_down(evt):
    if (current_page[0] + 1) * visible_buttons < len(SYMBOLS):
        current_page[0] += 1
        render_buttons(current_page[0])

ax_up = plt.axes([start_x, start_y + 0.07, button_w, button_h])
btn_up = Button(ax_up, "↑")
btn_up.on_clicked(scroll_up)

ax_down = plt.axes([start_x, start_y - visible_buttons * (button_h + spacing) - 0.06, button_w, button_h])
btn_down = Button(ax_down, "↓")
btn_down.on_clicked(scroll_down)

render_buttons(current_page[0])
fib_levels = plot_fib_chart(selected_symbol)

try:
    while True:
        try:
            fib_levels = plot_fib_chart(selected_symbol)
            live_price = get_live_price_from_yf(selected_symbol)

            if live_price is None:
                print("⚠️ Could not fetch live price. Waiting and retrying...")
                time.sleep(min(30, REFRESH_INTERVAL))
                continue

            print(f"\n📈 Live Price ({selected_symbol}): ${live_price:.2f}")

            # BUY
            if not bought:
                triggered = False
                for level in BUY_LEVELS:
                    lvl_price = fib_levels.get(level)
                    if lvl_price is not None and live_price <= lvl_price:
                        print(f"💰 Buy triggered at {level} — Price: ${live_price:.2f}")
                        place_order('BUY', QUANTITY, live_price)
                        bought = True
                        triggered = True
                        break
                if not triggered:
                    print("⌛ Waiting for buy signal...")

            # SELL
            elif bought and not sold:
                triggered = False
                for level in SELL_LEVELS:
                    lvl_price = fib_levels.get(level)
                    if lvl_price is not None and live_price >= lvl_price:
                        print(f"💸 Sell triggered at {level} — Price: ${live_price:.2f}")
                        place_order('SELL', QUANTITY, live_price)
                        sold = True
                        triggered = True
                        break
                if not triggered:
                    print("⏳ Waiting for sell signal...")

            if bought and sold:
                print("✅ Trade completed: bought and sold.")
                break

            plt.pause(REFRESH_INTERVAL)

        except KeyboardInterrupt:
            print("\n🛑 Stopped by user")
            break
        except Exception:
            safe_log_exception(created_by=None)
            print("❌ Unexpected error in main loop; see logs. Retrying shortly...")
            time.sleep(5)
            continue

except Exception:
    safe_log_exception(created_by=None)
    print("❌ Fatal error — exiting.")
finally:
    try:
        if ib and ib.isConnected():
            ib.disconnect()
            print("🔌 IBKR disconnected.")
    except Exception:
        safe_log_exception(created_by=None)
