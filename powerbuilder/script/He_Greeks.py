import yfinance as yf
import numpy as np
from scipy.stats import norm
from datetime import datetime
import mysql.connector
import traceback
import sys
import os

# Ensure correct module import paths
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from HE_error_logs import log_error_to_db
from HE_database_connect import get_connection


def black_scholes_greeks(S, K, T, r, sigma, option_type='call'):
    """Calculate Black-Scholes Greeks for a call or put option."""
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == 'call':
        delta = norm.cdf(d1)
        theta = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T))
                 - r * K * np.exp(-r * T) * norm.cdf(d2))
        rho = K * T * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == 'put':
        delta = norm.cdf(d1) - 1
        theta = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T))
                 + r * K * np.exp(-r * T) * norm.cdf(-d2))
        rho = -K * T * np.exp(-r * T) * norm.cdf(-d2)
    else:
        raise ValueError("option_type must be 'call' or 'put'")

    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    vega = S * norm.pdf(d1) * np.sqrt(T)

    return {
        'Delta': delta,
        'Gamma': gamma,
        'Theta (per day)': theta / 365,
        'Vega (per 1% IV)': vega / 100,
        'Rho (per 1% rate)': rho / 100
    }


user_input = {
    'symbol': 'SPY',
    'expiry_input': '21.5.2026',   # Input format: DD.MM.YYYY
    'strike_price': 577.0,
    'option_type': 'call'
}

symbol = user_input['symbol'].upper()
expiry = datetime.strptime(user_input['expiry_input'], '%d.%m.%Y').date()
strike_price = user_input['strike_price']
option_type = user_input['option_type'].lower()


try:
    ticker = yf.Ticker(symbol)
    stock_price = ticker.history(period="1d")['Close'].iloc[-1]
except Exception:
    error_message = traceback.format_exc()
    log_error_to_db(
        file_name=os.path.basename(__file__),
        error_description=error_message,
        created_by=None,
        env="dev"
    )
    raise

today = datetime.today().date()
T = max((expiry - today).days / 365, 1 / 365)


try:
    rfr_data = yf.Ticker("^TNX").history(period="1d")
    risk_free_rate = rfr_data["Close"].iloc[-1] / 100
except Exception:
    error_message = traceback.format_exc()
    log_error_to_db(
        file_name=os.path.basename(__file__),
        error_description=error_message,
        created_by=None,
        env="dev"
    )
    risk_free_rate = 0.05  # Fallback to 5%


available_expirations = ticker.options
expiry_str = expiry.strftime('%Y-%m-%d')

if expiry_str not in available_expirations:
    # Automatically pick the nearest available expiry
    expiry_str = min(
        available_expirations,
        key=lambda d: abs((datetime.strptime(d, "%Y-%m-%d").date() - expiry).days)
    )
    print(f"[INFO] Requested expiry not found. Using closest available: {expiry_str}")
    expiry = datetime.strptime(expiry_str, "%Y-%m-%d").date()


try:
    option_chain = ticker.option_chain(expiry_str)
    option_table = option_chain.calls if option_type == 'call' else option_chain.puts
    option_row = option_table[option_table['strike'] == strike_price]

    if not option_row.empty:
        implied_volatility = option_row['impliedVolatility'].values[0]
        print(f"[INFO] IV for {symbol} {strike_price} {option_type.upper()} "
              f"(Exp: {expiry_str}) = {implied_volatility * 100:.2f}%")
    else:
        print(f"[WARN] Strike {strike_price} not found. Using fallback IV=20%.")
        implied_volatility = 0.20
except Exception:
    error_message = traceback.format_exc()
    log_error_to_db(
        file_name=os.path.basename(__file__),
        error_description=error_message,
        created_by=None,
        env="dev"
    )
    print(f"[ERROR] Could not fetch option chain. Using fallback IV=20%.")
    implied_volatility = 0.20


try:
    greeks = black_scholes_greeks(
        S=stock_price,
        K=strike_price,
        T=T,
        r=risk_free_rate,
        sigma=implied_volatility,
        option_type=option_type
    )
except Exception:
    error_message = traceback.format_exc()
    log_error_to_db(
        file_name=os.path.basename(__file__),
        error_description=error_message,
        created_by=None,
        env="dev"
    )
    raise

print(f"\nOption Greeks for {symbol}")
print(f"Spot Price     : ${stock_price:.2f}")
print(f"Strike Price   : {strike_price:.2f}")
print(f"Option Type    : {option_type.upper()}")
print(f"Expiry Date    : {expiry}")
print(f"IV             : {implied_volatility * 100:.2f}%")
print(f"Risk-Free Rate : {risk_free_rate * 100:.2f}%\n")

for greek, value in greeks.items():
    print(f"{greek:<20}: {value:.10f}")

try:
    conn = get_connection()
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO he_option_greeks (
        symbol, option_type, stock_price, strike_price,
        implied_volatility, risk_free_rate, expiry_date, today_date, time_to_expiry,
        delta, gamma, theta, vega, rho
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        symbol,
        option_type,
        float(stock_price),
        float(strike_price),
        float(implied_volatility),
        float(risk_free_rate),
        expiry.strftime('%Y-%m-%d'),
        today.strftime('%Y-%m-%d'),
        float(T),
        float(greeks['Delta']),
        float(greeks['Gamma']),
        float(greeks['Theta (per day)']),
        float(greeks['Vega (per 1% IV)']),
        float(greeks['Rho (per 1% rate)'])
    )

    cursor.execute(insert_query, values)
    conn.commit()
    print("\n[INFO] Option Greeks stored in the database successfully.")

except mysql.connector.Error as err:
    error_message = traceback.format_exc()
    log_error_to_db(
        file_name=os.path.basename(__file__),
        error_description=error_message,
        created_by=None,
        env="dev"
    )
    print(f"[ERROR] Database insert error: {err}")

finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()
