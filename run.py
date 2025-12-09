import argparse
import subprocess

parser = argparse.ArgumentParser(description="Backtester CLI")

parser.add_argument("--strategy", type=str, default="sma", help="Strategy name")
parser.add_argument("--ticker", type=str, default="AAPL", help="Ticker symbol")
parser.add_argument("--optimize", action="store_true", help="Run optimization")
parser.add_argument("--benchmark", action="store_true", help="Run SPY benchmark")
parser.add_argument("--report", action="store_true", help="Generate HTML report")

args = parser.parse_args()

if args.optimize:
    subprocess.run(["python", "optimize.py", args.ticker])

elif args.benchmark:
    subprocess.run(["python", "benchmark.py", args.ticker])

elif args.report:
    subprocess.run(["python", "report.py"])

else:
    subprocess.run(["python", "backtest.py", args.strategy, args.ticker])
