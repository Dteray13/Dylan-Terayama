#!/usr/bin/env python
# coding: utf-8

# In[57]:


import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# List of stocks to process
tickers = [
    "TSLA",  # Tesla
    "PLTR",  # Palantir
    "META",  # Meta (Facebook)
    "GOOGL", # Alphabet (Google)
    "NVDA",  # Nvidia
    "AMD",   # AMD
    "AMZN",  # Amazon
    "KR",    # Kroger
    "KO",    # Coca-Cola
    "COST"   # Costco
]

# Function to calculate moving averages and generate signals
def calculate_signals(data):
    # Calculate short-term and long-term moving averages
    data['SMA20'] = data['Close'].rolling(window=20).mean()  # Short-term moving average (20 days)
    data['SMA50'] = data['Close'].rolling(window=50).mean()  # Long-term moving average (50 days)

    # Generate Buy and Sell signals based on moving averages
    data['Signal'] = 'Hold'  # Default signal is 'Hold'
    data.loc[data['SMA20'] > data['SMA50'], 'Signal'] = 'Buy'  # Buy signal when short-term MA > long-term MA
    data.loc[data['SMA20'] < data['SMA50'], 'Signal'] = 'Sell'  # Sell signal when short-term MA < long-term MA

    return data

# Function to visualize stock data and trading signals
def visualize_strategy(data, ticker):
    plt.figure(figsize=(12, 6))

    # Plot the stock closing price and moving averages
    plt.plot(data.index, data['Close'], label='Close Price', color='blue')
    plt.plot(data.index, data['SMA20'], label='20-Day SMA', linestyle='dashed', color='orange')
    plt.plot(data.index, data['SMA50'], label='50-Day SMA', linestyle='dashed', color='green')

    # Plot buy and sell signals
    buy_signals = data[data['Signal'] == 'Buy']
    sell_signals = data[data['Signal'] == 'Sell']
    plt.scatter(buy_signals.index, buy_signals['Close'], marker="^", color="green", label="Buy Signal", alpha=1)
    plt.scatter(sell_signals.index, sell_signals['Close'], marker="v", color="red", label="Sell Signal", alpha=1)

    # Add title and labels
    plt.title(f"Moving Average Crossover Strategy for {ticker}")
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.grid(True)
    plt.show()

# Process each stock
for ticker in tickers:
    print(f"Processing {ticker}...")

    # Fetch stock data (6 months of historical data)
    stock_data = yf.download(ticker, period="6mo")[["Close"]]

    # Ensure data is not empty
    if stock_data.empty:
        print(f"Skipping {ticker} due to empty data.")
        continue

    # Calculate signals based on moving averages
    stock_data = calculate_signals(stock_data)

    # Visualize the strategy
    visualize_strategy(stock_data, ticker)


# In[ ]:




