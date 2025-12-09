import yfinance as yf
import json
import numpy as np
import pandas as pd

def annualized_return(series):
    return (1 + series.mean()) ** 252 - 1

def annualized_volatility(series):
    return series.std() * np.sqrt(252)

def sharpe(series):
    vol = annualized_volatility(series)
    return annualized_return(series) / vol if vol != 0 else 0

def run_benchmark(ticker="SPY"):
    data = yf.download(ticker, period="5y")
    data["Returns"] = data["Close"].pct_change().dropna()

    bench = {
        "annual_return": float(annualized_return(data["Returns"])),
        "annual_volatility": float(annualized_volatility(data["Returns"])),
        "sharpe_ratio": float(sharpe(data["Returns"])),
        "max_drawdown": float((data["Close"] / data["Close"].cummax() - 1).min())
    }

    with open("results/benchmark.json", "w") as f:
        json.dump(bench, f, indent=4)

    print("Benchmark results saved to results/benchmark.json")

run_benchmark()
