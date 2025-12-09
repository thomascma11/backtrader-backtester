import pandas as pd
import matplotlib.pyplot as plt
import json

def plot_signals(metrics_path="results/metrics.json", data_path="data/AAPL.csv"):
    with open(metrics_path, "r") as f:
        metrics = json.load(f)

    buy_signals = metrics.get("buy_signals", [])
    sell_signals = metrics.get("sell_signals", [])

    df = pd.read_csv(data_path)
    df["Date"] = pd.to_datetime(df["Date"])

    plt.figure(figsize=(14, 7))
    plt.plot(df["Date"], df["Close"], label="Close Price", color="black")

    # plot buy signals
    for b in buy_signals:
        plt.scatter(df["Date"].iloc[b], df["Close"].iloc[b], color="green", marker="^", s=80)

    # plot sell signals
    for s in sell_signals:
        plt.scatter(df["Date"].iloc[s], df["Close"].iloc[s], color="red", marker="v", s=80)

    plt.title("📊 Buy & Sell Trading Signals")
    plt.xlabel("Date")
    plt.ylabel("Price ($)")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plot_signals()
