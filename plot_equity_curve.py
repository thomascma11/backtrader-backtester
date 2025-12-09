import json
import matplotlib.pyplot as plt
import pandas as pd

def plot_equity_curve(metrics_path="results/metrics.json"):
    with open(metrics_path, "r") as f:
        data = json.load(f)

    equity_curve = data.get("equity_curve", [])

    if not equity_curve:
        print("❌ No equity curve data found. Run backtest.py again.")
        return

    df = pd.DataFrame(equity_curve, columns=["date", "value"])
    df["date"] = pd.to_datetime(df["date"])

    plt.figure(figsize=(12, 6))
    plt.plot(df["date"], df["value"], label="Portfolio Value", linewidth=2)

    plt.title("📈 Portfolio Equity Curve", fontsize=16)
    plt.xlabel("Date")
    plt.ylabel("Portfolio Value ($)")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plot_equity_curve()
