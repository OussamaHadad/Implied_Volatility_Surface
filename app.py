# streamlit_app/app.py
import streamlit as st
import datetime as dt

from src.data.fetch_data import fetch_option_data
from src.volatility.implied_vol import compute_data_iv
from src.plotting.vol_surface_plot import generate_iv_surface

# ------------------- Page Configuration -------------------
st.set_page_config(page_title="Implied Volatility Surface Explorer", layout="wide")
st.title("📈 Implied Volatility Surface Explorer")

# ------------------- Sidebar Inputs -------------------
st.sidebar.header("Input Parameters")

# Ticker
ticker = st.sidebar.text_input("Ticker", value="AAPL")

# Default values: today and one month later
default_start = dt.date.today()
default_end = default_start + dt.timedelta(days=30)

# Sidebar date inputs
start_date = st.sidebar.date_input("Start Date", value=default_start)
end_date = st.sidebar.date_input("End Date", value=default_end)

# Interest rate and dividend yield
r = st.sidebar.number_input("Risk-free rate (r)", value=0.045, step=0.001, format="%.4f")
q = st.sidebar.number_input("Dividend yield (q)", value=0.005, step=0.001, format="%.4f")

# Interploation method
interpolation_method = st.sidebar.selectbox("Interpolation Method", ["linear", "cubic", "nearest"], index=0)

compute_button = st.sidebar.button("Compute IV Surface 🚀")

# ------------------- Main App Logic -------------------
if compute_button:
    with st.spinner(f"Fetching option data for {ticker} ..."):
        # Convert dates to string
        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date_str = end_date.strftime("%Y-%m-%d")
        try:
            options_df, spot_price = fetch_option_data(ticker, start_date_str, end_date_str)
        except Exception as e:
            st.error(f"❌ Error fetching data: {e}")
            st.stop()
    st.success(f"✅ Data fetched successfully! Spot price = {spot_price:.2f}")
    st.write("Preview of option data:")
    st.dataframe(options_df.head())


    with st.spinner("Computing implied volatilities..."):
        try:
            data_with_iv = compute_data_iv(options_df, spot_price, r, q, verbose=False)
        except Exception as e:
            st.error(f"❌ Error computing implied volatilities: {e}")
            st.stop()
    st.success("✅ Implied volatilities computed!")
    st.write("Preview with computed IVs:")
    st.dataframe(data_with_iv.head())


    with st.spinner("Generating implied volatility surface..."):
        try:
            fig_plotly = generate_iv_surface(data_with_iv, ticker, interpolation_method)
            st.success("✅ IV Surface generated successfully!")
            st.plotly_chart(fig_plotly, use_container_width=True)
        except Exception as e:
            st.error(f"❌ Error generating IV surface: {e}")
