import json
import pandas as pd

metrics = json.load(open("results/metrics.json"))
bench   = json.load(open("results/benchmark.json"))
opt     = json.load(open("results/optimization.json"))

html = f"""
<html>
<head><title>Backtest Report</title></head>
<body>
<h1>📈 Trading Strategy Performance Report</h1>

<h2>Strategy Metrics</h2>
<pre>{json.dumps(metrics, indent=4)}</pre>

<h2>Benchmark (SPY) Comparison</h2>
<pre>{json.dumps(bench, indent=4)}</pre>

<h2>Optimization Results</h2>
<pre>{json.dumps(opt, indent=4)}</pre>

<h2>Equity Curve</h2>
<img src="equity_curve.png" width="600"/>

<h2>Buy/Sell Signals</h2>
<img src="signals.png" width="600"/>
</body>
</html>
"""

open("results/report.html", "w").write(html)

print("HTML report saved → results/report.html")
