import streamlit as st
import pandas as pd
import yfinance as yf
import ta

# ---------------------------------------
# Function: Get historical data from Yahoo Finance
# ---------------------------------------
def get_historical_data(stock_symbol, period='1y'):
    ticker = f"{stock_symbol.upper()}.NS"
    df = yf.download(ticker, period=period)
    return df

# ---------------------------------------
# Function: Analyze and recommend
# ---------------------------------------
def analyze_stock(hist_df):
    if hist_df.empty:
        return "Data Unavailable"

    # RSI & MACD Calculation
    hist_df['RSI'] = ta.momentum.RSIIndicator(hist_df['Close']).rsi()
    macd = ta.trend.MACD(hist_df['Close'])
    hist_df['MACD'] = macd.macd()
    hist_df['Signal'] = macd.macd_signal()

    latest_rsi = hist_df['RSI'].iloc[-1]
    latest_macd = hist_df['MACD'].iloc[-1]
    latest_signal = hist_df['Signal'].iloc[-1]

    # Simple logic for recommendation
    if latest_rsi < 30 and latest_macd > latest_signal:
        return "BUY"
    elif latest_rsi > 70 or latest_macd < latest_signal:
        return "SELL"
    else:
        return "HOLD"

# ---------------------------------------
# Streamlit UI
# ---------------------------------------
st.title("📈 Indian Stock Recommender (Stable Version)")
st.markdown("*Educational purposes only. Not financial advice.*")

stock = st.text_input("Enter NSE Stock Symbol (e.g., RELIANCE)", value="RELIANCE")

if st.button("Get Recommendation"):
    with st.spinner("Fetching and analyzing data..."):
        hist_df = get_historical_data(stock)
        
        if not hist_df.empty:
            latest_price = hist_df['Close'].iloc[-1]
            rec = analyze_stock(hist_df)
            st.success(f"Recommendation: **{rec}**")
            st.write(f"Latest Price (Yahoo Finance): ₹{latest_price:.2f}")
            st.line_chart(hist_df['Close'])
        else:
            st.error("Failed to fetch data. Please check the stock symbol or try again.")
