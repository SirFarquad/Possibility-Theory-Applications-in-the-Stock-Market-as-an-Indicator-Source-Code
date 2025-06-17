# Possibility Theory: Applications in the Stock Market as an Indicator Source Code


Welcome to the souce code for my paper: Possibility Theory: Applications in the Stock Market as an Indicator! This paper applies possibility theory, an alternative to probability theory, to combine multiple well-known stock indicators (Moving Average Crossover, Moving Average Convergence Divergence, and Relative Strength Index), resulting in a more effective outcome. This project was advised by Professor Daniel Schwarz from FSU, much thanks to him for mentoring me. A full detailed explanation of the logic behind the code can be found in the full paper linked below. There are some leverage simulations included here that I didn't end up using in the paper, but there are here as well. Here’s a quick rundown of what you’ll find in this project and how to get started.

## What’s in This Project

- **data_collection.py**: This script grabs stock data of SPY from January 1st 2000-2024 from Yahoo Finance in and saves it into a SQLite database it creates named stock_data.db.
- **MAC_simulation.py**: This script calculates the moving average crossover indicator and simulates its performance.
- **MACD_simulation.py**: This script calculates the moving average convergence divergence and simulates its performance.
- **RSI_simulation.py**: This script calculates the relative strength index and simulates its performance.
- **possibility_simulation1.py**: This script combines all three indicators by using possibility theory and simulates its performance.
- **possibility_simulation2.py**: This script combines RSI and MACD by using possibility theory and simulates its performance.
- **possibility_simulation3.py**: This script combines MAC and MACD by using possibility theory and simulates its performance.
- **possibility_simulation4.py**: This script combines RSI and MAC by using possibility theory and simulates its performance.
- **leverage_simulation1.py**: This script combines all three indicators by using possibility theory and simulates its performance both normally and using a 2x leverage.
- **leverage_simulation2.py**: This script combines RSI and MACD by using possibility theory and simulates its performance both normally and using a 2x leverage.
- **leverage_simulation3.py**: This script combines MAC and MACD by using possibility theory and simulates its performance both normally and using a 2x leverage.
- **leverage_simulation2.py**: This script combines RSI and MAC by using possibility theory and simulates its performance both normally and using a 2x leverage.


## How to Get Started

1. **Set Up Your Environment**
   - Make sure you have Python 3.7 or higher.
   - Install the necessary packages by running:
     ```bash
     pip install yfinance pandas numpy matplotlib
     ```

2. **Collect the Data**
   - Run the `data_collection.py` script to download stock data and save it to an SQLite database named `stock_data.db`.
     ```bash
     python data_collection.py
     ```

3. **Run Simulations**
   - After collecting the data, you can run any of the simulation scripts. For example, to see the performance of the combined indicators using all three, run:
     ```bash
     python possibility_simulation1.py
     ```
    - To explore other combinations or individual indicator performances, simply run the respective .py file


## TechRxiv Paper

- URL: https://www.techrxiv.org/users/835937/articles/1228030-possibility-theory-applications-in-the-stock-market-as-an-indicator#
- DOI: https://doi.org/10.36227/techrxiv.172792857.72461875/v1

## Contributing

Contributions are welcome! If you have suggestions for improving the code or the simulations, feel free to open an issue or submit a pull request.

## License

This project is open source and available under the MIT License.