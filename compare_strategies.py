import os
import json
from backtest import BacktestRunner, STRATEGIES

def run_all_strategies():
    print("\n🔥 Running Multi-Strategy Comparison Engine")

    results = {}

    for strat_name in STRATEGIES.keys():
        print(f"\n➡️ Testing Strategy: {strat_name.upper()}")

        # update config file dynamically
        with open("config.json", "r") as f:
            config = json.load(f)

        config["strategy"] = strat_name

        # write updated config
        with open("config.json", "w") as f:
            json.dump(config, f, indent=4)

        # run the backtest
        bt = BacktestRunner()
        bt.run()

        # load metrics output
        with open("results/metrics.json", "r") as f:
            metrics = json.load(f)

        results[strat_name] = metrics

        # save per-strategy JSON
        with open(f"results/{strat_name}_results.json", "w") as f:
            json.dump(metrics, f, indent=4)

    print("\n🏆 Strategy Comparison Complete!")
    return results


def display_leaderboard(results):
    print("\n📊 Strategy Leaderboard (Ranked by Ending Portfolio Value)")
    ranking = sorted(results.items(), key=lambda x: x[1]["ending_value"], reverse=True)

    for rank, (strat, metrics) in enumerate(ranking, 1):
        print(f"{rank}. {strat.upper()} — ${metrics['ending_value']:.2f}")


if __name__ == "__main__":
    results = run_all_strategies()
    display_leaderboard(results)
