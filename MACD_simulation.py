import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

def fetch_data(db_name='stock_data.db'):
    conn = sqlite3.connect(db_name)
    query = 'SELECT * FROM stock_prices ORDER BY Date'
    data = pd.read_sql_query(query, conn)
    conn.close()
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)
    return data

def calculate_macd(data):
    # MACD Calculation
    ema_short = data['SPY_Close'].ewm(span=12, adjust=False).mean()
    ema_long = data['SPY_Close'].ewm(span=26, adjust=False).mean()
    macd = ema_short - ema_long
    signal_line = macd.ewm(span=9, adjust=False).mean()
    return macd, signal_line

def run_macd_simulation(data):
    initial_capital = data['SPY_Close'].iloc[0]  # Set initial capital to SPY's initial price
    capital = initial_capital
    position = 0
    capital_history = []
    dates = []
    drawdown_history = []
    return_history = []

    peak_value = initial_capital
    max_drawdown = 0

    # Calculate MACD and Signal Line
    data['MACD'], data['Signal_Line'] = calculate_macd(data)

    for i, row in data.iterrows():
        if pd.notna(row['MACD']) and pd.notna(row['Signal_Line']):
            if row['MACD'] > row['Signal_Line'] and position == 0:  # Buy Signal
                position = capital / row['SPY_Close']
                capital = 0
            elif row['MACD'] < row['Signal_Line'] and position > 0:  # Sell Signal
                capital = position * row['SPY_Close']
                position = 0

        # Track capital and date
        current_capital = capital if position == 0 else position * row['SPY_Close']
        capital_history.append(current_capital)
        dates.append(i)

        # Update peak value and calculate drawdown
        if current_capital > peak_value:
            peak_value = current_capital
        
        drawdown = (peak_value - current_capital) / peak_value if peak_value > 0 else 0
        max_drawdown = max(max_drawdown, drawdown)
        return_percentage = (current_capital - initial_capital) / initial_capital * 100

        drawdown_history.append(drawdown)
        return_history.append(return_percentage)

    # Convert to DataFrame for plotting
    capital_df = pd.DataFrame({
        'Date': dates,
        'Capital': capital_history,
        'Drawdown': drawdown_history,
        'Return': return_history
    })
    capital_df.set_index('Date', inplace=True)

    # Calculate SPY performance
    initial_spy_price = data['SPY_Close'].iloc[0]
    final_spy_price = data['SPY_Close'].iloc[-1]
    spy_return = (final_spy_price - initial_spy_price) / initial_spy_price * 100

    # Calculate Maximum Drawdown for SPY
    peak_spy = data['SPY_Close'].iloc[0]
    max_drawdown_spy = 0
    for price in data['SPY_Close']:
        if price > peak_spy:
            peak_spy = price
        drawdown_spy = (peak_spy - price) / peak_spy if peak_spy > 0 else 0
        max_drawdown_spy = max(max_drawdown_spy, drawdown_spy)

    # Plotting
    plt.figure(figsize=(14, 8))

    # Plot SPY Close Price and Trading Capital
    plt.plot(data.index, data['SPY_Close'], label='SPY Close Price', color='blue')
    plt.plot(capital_df.index, capital_df['Capital'], label='Trading Capital', color='orange')
    plt.title('SPY Closing Price vs. Trading Capital (MACD Strategy)')
    plt.xlabel('Date')
    plt.ylabel('Price / Capital')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.figtext(0.2, 0.9, f'SPY Return: {spy_return:.2f}%', fontsize=12, color='blue')
    plt.figtext(0.2, 0.85, f'SPY Drawdown: {max_drawdown_spy * 100:.2f}%', fontsize=12, color='blue')
    plt.figtext(0.2, 0.8, f'MACD Return: {capital_df["Return"].iloc[-1]:.2f}%', fontsize=12, color='orange')
    plt.figtext(0.2, 0.75, f'MACD Drawdown: {capital_df["Drawdown"].max() * 100:.2f}%', fontsize=12, color='orange')

    plt.show()

if __name__ == "__main__":
    data = fetch_data()
    run_macd_simulation(data)
