from tabulate import tabulate
import ccxt
import numpy
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import datetime

# Define the tickers and time range
tickers = 'BTCUSDT'
start_time = datetime.time(1, 30)  # 09:30 AM
end_time = datetime.time(23 , 0)  # 03:00 PM

def fetch_and_calculate_ema(ticker):
    # Fetching 5min interval data for the current day, suppress progress bar
    data = yf.download(ticker, interval='5m', period='3d', progress=False)
    
    # Calculating 10 and 20 EMA
    data['EMA10'] = ta.ema(data['Close'], length=10)
    data['EMA20'] = ta.ema(data['Close'], length=20)
    
    return data

def check_crossover(data, ticker):
    crossover_events = pd.DataFrame()
    for i in range(1, len(data)):
        current_time = data.index[i].time()
        if start_time <= current_time <= end_time:
            # Check for positive crossover
            if (data['EMA10'][i] > data['EMA20'][i]) and (data['EMA10'][i-1] < data['EMA20'][i-1]):
                event = pd.DataFrame([{
                    "DateTime": data.index[i],
                    "Ticker": ticker,
                    "Crossover Type": "Positive EMA Crossover",
                    "Close": data['Close'][i],
                    "EMA10": data['EMA10'][i],
                    "EMA20": data['EMA20'][i]
                }])
                crossover_events = pd.concat([crossover_events, event])
            
            # Check for negative crossover
            elif (data['EMA10'][i] < data['EMA20'][i]) and (data['EMA10'][i-1] > data['EMA20'][i-1]):
                event = pd.DataFrame([{
                    "DateTime": data.index[i],
                    "Ticker": ticker,
                    "Crossover Type": "Negative EMA Crossover",
                    "Close": data['Close'][i],
                    "EMA10": data['EMA10'][i],
                    "EMA20": data['EMA20'][i]
                }])
                crossover_events = pd.concat([crossover_events, event])
                
    return crossover_events



# ANSI color codes
RED = '\033[31m'
GREEN = '\033[32m'
RESET = '\033[0m'


def scan_tickers():
    all_crossovers = pd.DataFrame()
    for ticker in tickers:
        data = fetch_and_calculate_ema(ticker)
        crossover_events = check_crossover(data, ticker)
        all_crossovers = pd.concat([all_crossovers, crossover_events])
    
    if not all_crossovers.empty:
        # Convert 'DateTime' to a datetime object if it's not already
        all_crossovers['DateTime'] = pd.to_datetime(all_crossovers['DateTime'])
        
        # Round off the values to two decimal places
        all_crossovers['Close'] = all_crossovers['Close'].round(2)
        all_crossovers['EMA10'] = all_crossovers['EMA10'].round(2)
        all_crossovers['EMA20'] = all_crossovers['EMA20'].round(2)
        
        # Sort by DateTime
        all_crossovers.sort_values(by='DateTime', inplace=True)

        # Apply color coding to the 'Crossover Type'
        all_crossovers['Crossover Type'] = all_crossovers['Crossover Type'].apply(
            lambda x: f"{GREEN}{x}{RESET}" if "Positive" in x else f"{RED}{x}{RESET}"
        )

        # Tabulate and print
        tabulated_data = tabulate(all_crossovers, headers='keys', tablefmt='fancy_grid', showindex=False)
        print(tabulated_data)
        return True

# Run the scan
scan_tickers()

