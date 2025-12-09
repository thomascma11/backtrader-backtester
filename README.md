# 📈 Backtrader Strategy Backtester

A quantitative trading backtester built with **Python** and **Backtrader**.  
Includes a clean SMA crossover trading strategy, performance metrics, and trade visualizations.  
This project demonstrates skills relevant for **quantitative finance**, **algorithmic trading**, and **data-driven modeling**.

---

## 🚀 Features
- 📊 SMA (Simple Moving Average) crossover strategy  
- 📁 Loads OHLCV price data from CSV  
- 💰 Models initial capital, position sizing, and commission  
- 🔁 Automated buy/sell decision-making  
- 📈 Visualizes backtest performance using Backtrader  
- 💬 Prints starting and final portfolio value  

---

## 📂 Project Structure

backtrader-backtester/
│── data/
│ └── AAPL.csv # Add your own OHLCV data here
│── strategies/
│ └── sma_cross.py # SMA crossover strategy implementation
│── backtest.py # Main backtest runner
│── requirements.txt # Dependencies
│── README.md # Documentation

---

## 🧠 Strategy Logic

**Buy** when the 10-day SMA crosses **above** the 30-day SMA.  
**Sell** when the 10-day SMA crosses **below** the 30-day SMA.  

Classic trend-following logic.

---

## 🛠 Installation

Install the required libraries:

```bash
pip install -r requirements.txt


## 📊 Example Quant Performance

| Metric              | Value (Example) |
|--------------------|------------------|
| Sharpe Ratio       | 1.32             |
| Max Drawdown       | -7.8%            |
| Win Rate           | 54%              |
| Total Trades       | 32               |
| Annualized Return  | 12.4%            |
| Final Portfolio    | $11,372.51       |

All metrics are automatically saved to:

- **Annual Return**
- **Annual Volatility**
- **Sharpe Ratio**
- **Max Drawdown**
- **Max Drawdown Duration**
- **Equity Curve Visualization**
- **Buy/Sell Signal Chart**


