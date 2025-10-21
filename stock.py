def analyze_stock(hist_df):
    if hist_df.empty or 'Close' not in hist_df.columns:
        return "Data Unavailable"

    # Drop any rows with missing Close values
    hist_df = hist_df.dropna(subset=['Close'])
    if hist_df.empty:
        return "Data Unavailable"

    # Ensure Close column is numeric
    hist_df['Close'] = pd.to_numeric(hist_df['Close'], errors='coerce')
    hist_df = hist_df.dropna(subset=['Close'])
    if hist_df.empty:
        return "Data Unavailable"

    # RSI & MACD Calculation
    try:
        hist_df['RSI'] = ta.momentum.RSIIndicator(hist_df['Close']).rsi()
        macd = ta.trend.MACD(hist_df['Close'])
        hist_df['MACD'] = macd.macd()
        hist_df['Signal'] = macd.macd_signal()
    except Exception as e:
        print("Error computing indicators:", e)
        return "Analysis Error"

    latest_rsi = hist_df['RSI'].iloc[-1]
    latest_macd = hist_df['MACD'].iloc[-1]
    latest_signal = hist_df['Signal'].iloc[-1]

    if pd.isna(latest_rsi) or pd.isna(latest_macd) or pd.isna(latest_signal):
        return "Insufficient Data"

    # Simple logic for recommendation
    if latest_rsi < 30 and latest_macd > latest_signal:
        return "BUY"
    elif latest_rsi > 70 or latest_macd < latest_signal:
        return "SELL"
    else:
        return "HOLD"
