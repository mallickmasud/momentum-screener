
# Smart Momentum Screener Web App for NSE/BSE Stocks
# Note: This script uses yfinance and Streamlit for interactive UI
# Required libraries: pip install yfinance pandas numpy streamlit

import yfinance as yf
import pandas as pd
import numpy as np
import streamlit as st

# RSI Calculation Function
def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

# Streamlit UI Setup
st.title("📈 Smart Momentum Screener for NSE/BSE Stocks")
st.markdown("This app analyzes momentum indicators (RSI, SMA) to find bullish stocks.")

# Stock list input (multi-select)
def get_stock_list():
    return [
        'TATAMOTORS', 'INFY', 'RELIANCE', 'SBIN', 'HDFCBANK', 'ICICIBANK', 'AXISBANK', 'KOTAKBANK', 'LT', 'TCS',
        'ITC', 'HINDUNILVR', 'MARUTI', 'BAJAJ-AUTO', 'ULTRACEMCO', 'NESTLEIND', 'ASIANPAINT', 'SUNPHARMA', 'CIPLA', 'DRREDDY',
        'ADANIPORTS', 'ADANIENT', 'COFORGE', 'TATAELXSI', 'IEX', 'NHPC', 'PFC', 'BEL', 'IRFC', 'TRIDENT', 'BHEL',
        'RVNL', 'NBCC', 'HFCL', 'IRCTC', 'LICHSGFIN', 'JINDALSTEL', 'TATACOMM', 'ZEEL', 'IDFCFIRSTB', 'TVSMOTOR',
        'SYNGENE', 'BALRAMCHIN', 'CESC', 'CANFINHOME', 'GICRE', 'DALBHARAT', 'MPHASIS', 'INDIGO', 'CLEAN', 'HINDCOPPER'
    ]

stock_choices = get_stock_list()
selected_stocks = st.multiselect("Select stocks to analyze:", stock_choices, default=stock_choices[:20])

# Main screener logic
def run_screener(stocks):
    results = []
    for symbol in stocks:
        try:
            data = yf.download(symbol + ".NS", period='1mo', interval='1d', progress=False)
            if data is None or data.empty or len(data) < 20:
                continue
            data['RSI'] = calculate_rsi(data['Close'])
            data['SMA_10'] = data['Close'].rolling(window=10).mean()

            if data['RSI'].iloc[-1] > 60 and data['Close'].iloc[-1] > data['SMA_10'].iloc[-1]:
                score = data['RSI'].iloc[-1] + (data['Close'].iloc[-1] - data['SMA_10'].iloc[-1])
                results.append({
                    'Stock': symbol,
                    'RSI': round(data['RSI'].iloc[-1], 2),
                    'SMA_10': round(data['SMA_10'].iloc[-1], 2),
                    'Close': round(data['Close'].iloc[-1], 2),
                    'Score': round(score, 2)
                })
        except Exception as e:
            st.warning(f"Error processing {symbol}: {e}")

    return pd.DataFrame(results)

# Run Screener Button
if st.button("Run Screener"):
    df = run_screener(selected_stocks)
    if not df.empty:
        df = df.sort_values(by='Score', ascending=False)
        st.dataframe(df)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Results as CSV", csv, "momentum_screener_results.csv", "text/csv")
    else:
        st.info("No stocks met the criteria.")
