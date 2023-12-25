import yfinance as yf
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import warnings
import pandas as pd
import openpyxl

warnings.simplefilter(action='ignore', category=FutureWarning)
pd.options.mode.chained_assignment = None


def get_date_x_days_before(date_string, num_days_before):
    date_object = dt.datetime.strptime(date_string, "%Y-%m-%d")
    new_date = date_object - dt.timedelta(days=num_days_before)
    new_date_string = new_date.strftime("%Y-%m-%d")
    return new_date_string


def export_plots(ticker, stock_data):

    stock_data = stock_data[start_date:]
    plt.figure(figsize=(16, 9))
    plt.title(ticker + ": Algorithmic Trading")
    plt.xlabel("Date")
    plt.ylabel("Stock Price ($USD)")
    plt.plot(stock_data["Close"], label='Close Price')
    plt.plot(stock_data["SMA_50"], label='SMA_50')
    plt.plot(stock_data["SMA_100"], label='SMA_100')
    plt.plot(stock_data['short_MA'], label='Short MA')
    plt.plot(stock_data['long_MA'], label='Long MA')
    plt.legend()
    name = str(ticker) + ".png"
    plt.savefig(name)
    plt.close()


dow_30_tickers = [
    "AAPL",  # Apple Inc.
    "AMGN",  # Amgen Inc.
    "AXP",   # American Express Company
    "BA",    # The Boeing Company
    "CAT",   # Caterpillar Inc.
    "CRM",   # Salesforce.com Inc.
    "CSCO",  # Cisco Systems Inc.
    "CVX",   # Chevron Corporation
    "DIS",   # The Walt Disney Company
    "DOW",   # Dow Inc.
    "GS",    # The Goldman Sachs Group Inc.
    "HD",    # The Home Depot Inc.
    "HON",   # Honeywell International Inc.
    "IBM",   # International Business Machines Corporation
    "INTC",  # Intel Corporation
    "JNJ",   # Johnson & Johnson
    "JPM",   # JPMorgan Chase & Co.
    "KO",    # The Coca-Cola Company
    "MCD",   # McDonald's Corporation
    "MMM",   # 3M Company
    "MRK",   # Merck & Co. Inc.
    "MSFT",  # Microsoft Corporation
    "NKE",   # NIKE Inc.
    "PG",    # Procter & Gamble Company
    "TRV",   # The Travelers Companies Inc.
    "UNH",   # UnitedHealth Group Incorporated
    "V",     # Visa Inc.
    "VZ",    # Verizon Communications Inc.
    "WBA",   # Walgreens Boots Alliance Inc.
    "WMT",   # Walmart Inc.
]

start_date = "2021-01-01"
end_date = "2023-12-24"
num_periods_50 = 50
num_periods_100 = 100
long_MA = 200
short_MA = 25

trigger = 0

for x in dow_30_tickers:
    start_date_x_days_before_50 = get_date_x_days_before(start_date, num_periods_50*2)
    start_date_x_days_before_100 = get_date_x_days_before(start_date, num_periods_100*2)
    stock_data = yf.download(x, start=start_date_x_days_before_50, end=end_date)
    stock_data["SMA_50"] = stock_data["Close"].rolling(window=num_periods_50).mean()
    stock_data["SMA_100"] = stock_data["Close"].rolling(window=num_periods_100).mean()
    stock_data['short_MA'] = stock_data['Close'].ewm(span=short_MA).mean()
    stock_data['long_MA'] = stock_data['Close'].ewm(span=long_MA).mean()

    stock_data['trigger'] = np.where(stock_data['SMA_50'] > stock_data['SMA_100'], 1, 0)
    stock_data['trigger'] = np.where(stock_data['SMA_100'] > stock_data['SMA_50'], 0, stock_data['trigger'])

    stock_data['crosszero'] = np.where(stock_data['short_MA'] < stock_data['long_MA'], 1.0, 0.0)
    stock_data['position'] = stock_data['crosszero'].diff()
    stock_data['position'].iloc[-1] = -1
    stock_data = pd.DataFrame(stock_data)
    print(x + " Complete")

    export_plots(x, stock_data)
    name = x + ".xlsx"
    stock_data.to_excel(name)

