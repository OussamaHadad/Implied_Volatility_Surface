from src.data.fetch_data import fetch_option_data
from src.solvers.root_finders import *
from src.plotting.vol_surface_plot import generate_iv_surface
from src.volatility.implied_vol import compute_data_iv

import datetime as dt
import sys
import os

# Add the project root to sys.path (one level up from notebooks/)
project_root = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(project_root)

ticker = "AAPL"

# Default values: today and one month later
default_start = dt.date.today()
default_end = default_start + dt.timedelta(days=30)

start_date = default_start.strftime("%Y-%m-%d")
end_date = default_end.strftime("%Y-%m-%d")

r = 0.045
q = 0.005

options_df, spot_price = fetch_option_data(ticker, start_date, end_date)

data_with_iv = compute_data_iv(options_df, spot_price, r, q, verbose = False)
generate_iv_surface(data_with_iv, ticker, plot = True)  # Graph displayed in the local browser
