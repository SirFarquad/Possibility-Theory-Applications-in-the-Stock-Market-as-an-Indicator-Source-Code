import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3

# Fetch data from the database
def fetch_data(db_name='stock_data.db'):
    conn = sqlite3.connect(db_name)
    query = 'SELECT * FROM stock_prices ORDER BY Date'
    data = pd.read_sql_query(query, conn)
    conn.close()
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)
    
    # Drop rows where either SPY_Close or Leverage_Close is missing
    data = data.dropna(subset=['SPY_Close', 'Leverage_Close'])
    
    return data

# MACD calculation
def calculate_macd(data):
    ema_short = data['SPY_Close'].ewm(span=12, adjust=False).mean()
    ema_long = data['SPY_Close'].ewm(span=26, adjust=False).mean()
    macd = ema_short - ema_long
    signal_line = macd.ewm(span=9, adjust=False).mean()

    # Standardizing MACD such that the signal line corresponds to 0.5
    macd_diff = macd - signal_line
    data['MACD'] = (macd_diff - macd_diff.min()) / (macd_diff.max() - macd_diff.min())

    return data

# Moving Average Crossover (MAC) calculation
def calculate_mac(data):
    data['MA_Short'] = data['SPY_Close'].rolling(window=50).mean()
    data['MA_Long'] = data['SPY_Close'].rolling(window=200).mean()

    mac_diff = data['MA_Short'] - data['MA_Long']
    data['MAC'] = (mac_diff - mac_diff.min()) / (mac_diff.max() - mac_diff.min())

    return data

# Running the possibility simulation
def run_possibility_simulation(data):
    initial_capital = data['SPY_Close'].iloc[0]
    capital = initial_capital
    position = 0
    capital_history = []
    dates = []
    drawdown_history = []
    return_history = []

    leverage_capital = initial_capital
    leverage_position = 0
    leverage_capital_history = []
    leverage_drawdown_history = []
    leverage_return_history = []

    peak_value = initial_capital
    max_drawdown = 0
    max_leverage_drawdown = 0
    final_return = 0
    final_leverage_return = 0

    # Calculate RSI, MACD, and MAC
    data = calculate_macd(data)
    data = calculate_mac(data)

    # Calculate Possibility Theory Indicator (Max of RSI, MACD, and MAC)
    data['Possibility'] = data[['MACD', 'MAC']].max(axis=1)

    # Peak and drawdown tracking for SPY
    peak_spy = data['SPY_Close'].iloc[0]
    max_drawdown_spy = 0
    leverage_peak_value = initial_capital  # Separate peak for leveraged strategy

    for i, row in data.iterrows():
        if pd.notna(row['Possibility']):
            # Buy signal: Possibility > 0.5
            if row['Possibility'] > 0.5 and position == 0:
                position = capital / row['SPY_Close']
                leverage_position = leverage_capital / row['Leverage_Close']
                capital = 0
                leverage_capital = 0
            # Sell signal: Possibility < 0.5
            elif row['Possibility'] < 0.5 and position > 0:
                capital = position * row['SPY_Close']
                leverage_capital = leverage_position * row['Leverage_Close']
                position = 0
                leverage_position = 0

        current_capital = capital if position == 0 else position * row['SPY_Close']
        current_leverage_capital = leverage_capital if leverage_position == 0 else leverage_position * row['Leverage_Close']
        capital_history.append(current_capital)
        leverage_capital_history.append(current_leverage_capital)
        dates.append(i)

        # Update the peak value for unleveraged capital
        if current_capital > peak_value:
            peak_value = current_capital
        
        # Update the peak value for leveraged capital separately
        if current_leverage_capital > leverage_peak_value:
            leverage_peak_value = current_leverage_capital

        drawdown = (peak_value - current_capital) / peak_value if peak_value > 0 else 0
        max_drawdown = max(max_drawdown, drawdown)
        return_percentage = (current_capital - initial_capital) / initial_capital * 100

        drawdown_history.append(drawdown)
        return_history.append(return_percentage)

        # Calculate drawdown for leveraged capital
        leverage_drawdown = (leverage_peak_value - current_leverage_capital) / leverage_peak_value if leverage_peak_value > 0 else 0
        max_leverage_drawdown = max(max_leverage_drawdown, leverage_drawdown)
        leverage_return_percentage = (current_leverage_capital - initial_capital) / initial_capital * 100

        leverage_drawdown_history.append(leverage_drawdown)
        leverage_return_history.append(leverage_return_percentage)

        final_return = return_percentage
        final_leverage_return = leverage_return_percentage

        # Update SPY peak and calculate SPY drawdown
        if row['SPY_Close'] > peak_spy:
            peak_spy = row['SPY_Close']
        drawdown_spy = (peak_spy - row['SPY_Close']) / peak_spy
        max_drawdown_spy = max(max_drawdown_spy, drawdown_spy)

    capital_df = pd.DataFrame({
        'Date': dates,
        'Capital': capital_history,
        'Drawdown': drawdown_history,
        'Return': return_history
    })
    capital_df.set_index('Date', inplace=True)

    leverage_capital_df = pd.DataFrame({
        'Date': dates,
        'Capital': leverage_capital_history,
        'Drawdown': leverage_drawdown_history,
        'Return': leverage_return_history
    })
    leverage_capital_df.set_index('Date', inplace=True)

    # SPY performance
    initial_spy_price = data['SPY_Close'].iloc[0]
    final_spy_price = data['SPY_Close'].iloc[-1]
    spy_return = (final_spy_price - initial_spy_price) / initial_spy_price * 100

    # Plotting
    plt.figure(figsize=(14, 8))

    plt.plot(data.index, data['SPY_Close'], label='SPY Close Price', color='blue')
    plt.plot(capital_df.index, capital_df['Capital'], label='Trading Capital', color='orange')
    plt.plot(leverage_capital_df.index, leverage_capital_df['Capital'], label='Leverage Capital', color='red')
    plt.title('SPY Closing Price vs. Trading Capital vs. Leveraged Capital')
    plt.xlabel('Date')
    plt.ylabel('Price / Capital')

    # Display Max Drawdown and Return Percentages as text
    plt.figtext(0.2, 0.9, f'SPY Return: {spy_return:.2f}%', fontsize=12, color='blue')
    plt.figtext(0.2, 0.85, f'SPY Max Drawdown: {max_drawdown_spy * 100:.2f}%', fontsize=12, color='blue')
    plt.figtext(0.2, 0.8, f'Possibility Return: {final_return:.2f}%', fontsize=12, color='orange')
    plt.figtext(0.2, 0.75, f'Possibility Max Drawdown: {max_drawdown * 100:.2f}%', fontsize=12, color='orange')
    plt.figtext(0.2, 0.7, f'Leverage Return: {final_leverage_return:.2f}%', fontsize=12, color='red')
    plt.figtext(0.2, 0.65, f'Leverage Max Drawdown: {max_leverage_drawdown * 100:.2f}%', fontsize=12, color='red')

    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    data = fetch_data()
    run_possibility_simulation(data)
