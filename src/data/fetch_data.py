from typing import Tuple
from datetime import datetime
import yfinance as yf
import pandas as pd

def fetch_option_data(ticker: str, start_date: str, end_date: str) -> Tuple[pd.DataFrame, float]:
  """
  Fetch option chain data between given expiration date range.
  """
  stock = yf.Ticker(ticker)

  options_data = []

  # 1. Get the spot price
  spot_price = stock.history(period = "1d")["Close"].iloc[0] # period = "1d" => Pick previous day's data

  # 2. Get the option data
  start_dt = datetime.strptime(start_date, "%Y-%m-%d").date()
  end_dt = datetime.strptime(end_date, "%Y-%m-%d").date()
  today = datetime.now().date()

  if end_dt < today:
    print(f"Warning: end_date ({end_dt}) is in the past. Only future expirations will be considered.")
    return pd.DataFrame(), spot_price

  expiration_dates = []

  for expiration in stock.options:
    expiration_dt = datetime.strptime(expiration, "%Y-%m-%d").date()

    if not (start_dt <= expiration_dt <= end_dt):
      continue
    expiration_dates.append(expiration_dt)

    T = (expiration_dt - today).days / 365
    if T <= 0:
      continue

    try:
      chain = stock.option_chain(expiration)
      calls = chain.calls
      calls = calls[(calls['bid'] > 0) & (calls['ask'] > 0)]
      calls['midPrice'] = 0.5 * (calls['bid'] + calls['ask'])
      calls['timeToMaturity'] = T
      options_data.append(calls[['strike', 'midPrice', 'timeToMaturity']])
    except Exception:
      continue

  if not options_data:
    raise ValueError("No option data found for the given date range.")

  options_df = pd.concat(options_data, ignore_index = True)

  print(f"Fetched {len(options_df)} options between {expiration_dates[0]} and {expiration_dates[-1]}.")

  return options_df, spot_price

