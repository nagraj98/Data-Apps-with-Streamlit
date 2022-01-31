import streamlit as st
import yfinance as yf
import pandas as pd

st.write("""
# Simple Stock Price App.

##### Shows the Stock closing price and volume for TCS on the NSE exchange.

""")

# The ticker symbol for any company can be checked at yahoo finance website.
# https://finance.yahoo.com/
tickerSymbol = "TCS.NS"
tickerData = yf.Ticker(tickerSymbol)

# returns a pandas dataframe
tickerDf = tickerData.history(period='max')

st.line_chart(tickerDf.Close)
st.line_chart(tickerDf.Volume)




