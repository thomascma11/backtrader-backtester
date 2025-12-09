import json
import numpy as np
import subprocess

short_values = [5, 10, 20]
long_values  = [30, 50, 100]

best = {"sharpe": -999, "short": None, "long": None}

for short in short_values:
    for long in long_values:
        print(f"Running SMA {short}/{long}")

        subprocess.run(["python", "backtest.py", "sma", f"{short}", f"{long}"])

        with open("results/metrics.json", "r") as f:
            m = json.load(f)

        if m["sharpe_ratio"] > best["sharpe"]:
            best["sharpe"] = m["sharpe_ratio"]
            best["short"] = short
            best["long"] = long

with open("results/optimization.json", "w") as f:
    json.dump(best, f, indent=4)

print("Optimization complete:", best)
